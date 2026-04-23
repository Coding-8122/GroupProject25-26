# start.ps1

$ErrorActionPreference = "Stop"

Write-Host "Starting local development environment..." -ForegroundColor Cyan

# 1. Check if uv is installed
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: 'uv' is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

# 2. Sync dependencies
Write-Host "`nSyncing Python packages..." -ForegroundColor Yellow
uv sync --all-extras --dev

# 3. Start Database
Write-Host "`nStarting PostgreSQL container..." -ForegroundColor Yellow
docker compose up -d db

# 4. Wait for Database to be healthy
Write-Host "Waiting for PostgreSQL to become healthy..." -ForegroundColor Yellow
$attempts = 0
$max_attempts = 15
$is_healthy = $false

while ($attempts -lt $max_attempts) {
    $containerId = docker compose ps -q db
    if ($containerId) {
        $health = docker inspect --format='{{json .State.Health.Status}}' $containerId
        if ($health -match "healthy") {
            $is_healthy = $true
            break
        }
    }

    Write-Host "Waiting... ($($attempts + 1)/$max_attempts)" -ForegroundColor DarkGray
    Start-Sleep -Seconds 2
    $attempts++
}

if (-not $is_healthy) {
    Write-Host "Error: Database failed to initialize in time." -ForegroundColor Red
    docker compose logs db
    exit 1
}
Write-Host "Database is ready!" -ForegroundColor Green

# 5. Handle Database Migrations
Write-Host "`nChecking database migrations..." -ForegroundColor Yellow
if (Test-Path "migrations") {
    Write-Host "Applying existing migrations..."
    uv run flask db upgrade
} else {
    Write-Host "Warning: 'migrations' folder not found. Falling back to create_all()." -ForegroundColor Magenta
    Write-Host "If this is a new project, you should run: uv run flask db init" -ForegroundColor DarkGray
    uv run python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
}

# 6. Start the Flask App
Write-Host "`nStarting Flask development server..." -ForegroundColor Green
$env:FLASK_DEBUG = "1"
uv run flask run