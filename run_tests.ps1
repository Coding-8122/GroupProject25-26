# run_tests.ps1
$ErrorActionPreference = "Stop"
Write-Host "--- RecoveryTracker Test Runner (with Coverage) ---" -ForegroundColor Cyan

# 1. Session Environment Configuration
$env:DATABASE_URL = "postgresql://user:password@127.0.0.1:5432/recovery_test"
$env:FLASK_ENV = "testing"
$env:PYTHONPATH = "."

# 2. Ensure Database Infrastructure
Write-Host "Checking database container..." -ForegroundColor Yellow
docker compose up -d db

# 3. Create Test Database (Safe Check)
# We check if the database exists before attempting to create it to avoid noisy errors
Write-Host "Preparing 'recovery_test' database..." -ForegroundColor DarkGray
$dbExists = docker exec $(docker compose ps -q db) psql -U user -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='recovery_test'"
if (-not $dbExists) {
    docker exec $(docker compose ps -q db) psql -U user -d postgres -c "CREATE DATABASE recovery_test;"
    Write-Host "Database created." -ForegroundColor Green
} else {
    Write-Host "Database already exists, skipping creation." -ForegroundColor Gray
}

# 4. Execute Pytest with Coverage
# --cov=app: Tracks coverage for the source code
# --cov-report=term-missing: Identifies exact lines not covered by tests
Write-Host "`nExecuting pytest suite..." -ForegroundColor Yellow
uv run pytest tests/ --cov=app --cov-report=term-missing --maxfail=1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSUCCESS: All tests passed! ✅" -ForegroundColor Green
} else {
    Write-Host "`nFAILURE: Tests failed. Check the logs above. ❌" -ForegroundColor Red
    exit 1
}