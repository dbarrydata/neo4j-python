Write-Host "Stopping Neo4j Docker database..." -ForegroundColor Cyan

Set-Location $PSScriptRoot

docker compose down

Write-Host ""
Write-Host "Neo4j stopped." -ForegroundColor Green