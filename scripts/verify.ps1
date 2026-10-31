# Verificación completa del proyecto AWEN (Windows / PowerShell)
# Uso: ./scripts/verify.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$script:failed = $false

function Invoke-Step {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$WorkDir,
        [Parameter(Mandatory)][scriptblock]$Command
    )

    Write-Host ""
    Write-Host "== $Name ==" -ForegroundColor Cyan
    Push-Location $WorkDir
    try {
        & $Command
        if ($LASTEXITCODE -ne 0) {
            Write-Host "FALLO: $Name (exit $LASTEXITCODE)" -ForegroundColor Red
            $script:failed = $true
        }
    }
    finally {
        Pop-Location
    }
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: python no esta instalado o no esta en PATH." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: npm no esta instalado o no esta en PATH." -ForegroundColor Red
    exit 1
}

$env:AWEN_SECRET_KEY = "test"

Invoke-Step -Name "Backend: pytest" -WorkDir (Join-Path $root "back-end") -Command {
    python -m pytest tests -q
}

$frontend = Join-Path $root "front-end"

if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
    Invoke-Step -Name "Frontend: npm ci" -WorkDir $frontend -Command { npm ci }
}

Invoke-Step -Name "Frontend: lint"  -WorkDir $frontend -Command { npm run lint }
Invoke-Step -Name "Frontend: tests" -WorkDir $frontend -Command { npm test }
Invoke-Step -Name "Frontend: build" -WorkDir $frontend -Command { npm run build }

Write-Host ""
if ($script:failed) {
    Write-Host "VERIFICACION FALLIDA" -ForegroundColor Red
    exit 1
}

Write-Host "VERIFICACION OK" -ForegroundColor Green
