$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::UTF8

Write-Host "== Health Check ==" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" | ConvertTo-Json

Write-Host "\n== Chat Demo ==" -ForegroundColor Cyan
$chat1 = @{ message = "When will my order be shipped?" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/chat" -ContentType "application/json" -Body $chat1 | ConvertTo-Json

$chat2 = @{ message = "How to fix ImportError in Python?" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/chat" -ContentType "application/json" -Body $chat2 | ConvertTo-Json

Write-Host "\n== Admin Stats ==" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/admin/stats" | ConvertTo-Json
