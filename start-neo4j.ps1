Write-Host "Starting Neo4j Docker database..." -ForegroundColor Cyan

# Move to the folder where this script lives
Set-Location $PSScriptRoot

# Check that .env exists
if (!(Test-Path ".env")) {
    Write-Host "ERROR: .env file not found." -ForegroundColor Red
    Write-Host "Create .env from .env.example before starting Neo4j."
    exit 1
}

# Start Neo4j
docker compose up -d

# Show running containers
Write-Host ""
Write-Host "Current Docker containers:" -ForegroundColor Cyan
docker ps

Write-Host ""
Write-Host "Neo4j should be available at:" -ForegroundColor Green
Write-Host "Browser: http://localhost:7474"
Write-Host "Driver:  neo4j://localhost:7687"

Write-Host ""
Write-Host "To stop Neo4j later, run:" -ForegroundColor Yellow
Write-Host "docker compose down"