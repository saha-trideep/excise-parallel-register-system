# PowerShell Import Script for December Data
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   IMPORTING DECEMBER DATA" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$csvPath = "C:\Users\Lenovo\Desktop\Daily Activity Database - Activity.csv"
$dbPath = "$PSScriptRoot\excise_registers.db"

# Check if CSV exists
if (-not (Test-Path $csvPath)) {
    Write-Host "ERROR: CSV file not found at: $csvPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

Write-Host "✓ Found CSV file" -ForegroundColor Green
Write-Host "✓ Running Python import script..." -ForegroundColor Green
Write-Host ""

# Change to project directory and run Python
Set-Location $PSScriptRoot

# Try different Python commands
$pythonCommands = @("python", "python3", "py")
$pythonFound = $false

foreach ($cmd in $pythonCommands) {
    try {
        $version = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Using: $cmd" -ForegroundColor Green
            & $cmd import_december_data.py
            $pythonFound = $true
            break
        }
    }
    catch {
        continue
    }
}

if (-not $pythonFound) {
    Write-Host ""
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run this command in Command Prompt:" -ForegroundColor Yellow
    Write-Host "cd [Your-Project-Folder]" -ForegroundColor White
    Write-Host "python import_december_data.py" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
}
