# start.ps1
$ErrorActionPreference = "Stop"
Write-Host "--- RecoveryTracker Local Dev Server ---" -ForegroundColor Cyan

# 1. Sync Python dependencies
Write-Host "`n[1/5] Syncing packages..." -ForegroundColor Yellow
uv sync --all-extras --dev

# 2. Start PostgreSQL via Docker
Write-Host "`n[2/5] Starting PostgreSQL container..." -ForegroundColor Yellow
docker compose up -d db

# 3. Wait for port 5432 to be available on localhost
Write-Host "[3/5] Waiting for PostgreSQL port exposure at 127.0.0.1:5432..." -ForegroundColor Yellow
$is_ready = $false
for ($i=1; $i -le 15; $i++) {
    $check = Test-NetConnection -ComputerName 127.0.0.1 -Port 5432 -InformationLevel Quiet
    if ($check) {
        $is_ready = $true
        Write-Host "Database port is reachable!" -ForegroundColor Green
        break
    }
    Write-Host "Waiting... ($i/15)" -ForegroundColor DarkGray
    Start-Sleep -Seconds 2
}

if (-not $is_ready) {
    Write-Host "`nERROR: Database port 5432 is not responding. Check your docker-compose.yml 'ports' section." -ForegroundColor Red
    exit 1
}

# 4. Set local environment variables (overrides .env for this session)
$env:DATABASE_URL = "postgresql://user:password@127.0.0.1:5432/recovery_db"
$env:FLASK_APP = "run.py"
$env:FLASK_DEBUG = "1"

# 5. Database schema management
Write-Host "`n[4/5] Syncing database schema..." -ForegroundColor Yellow
if (Test-Path "migrations") {
    uv run flask db upgrade
} else {
    Write-Host "No migrations found. Initializing database from models..." -ForegroundColor Magenta
    uv run python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
}

# 6. Launch Application
Write-Host "`n[5/5] Starting Flask development server..." -ForegroundColor Green
uv run flask run