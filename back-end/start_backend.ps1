<# 
.SYNOPSIS
    Inicia el backend AWEN en PowerShell.

.DESCRIPTION
    Script para arrancar el servidor FastAPI/Uvicorn en el puerto 8000.
    Funciona en Windows PowerShell 5.1+ y PowerShell Core 6+.

.USAGE
    .\start_backend.ps1
#>

# Detener en error
$ErrorActionPreference = "Stop"

# Cambiar al directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path $scriptDir

# Arrancar uvicorn
python -m uvicorn app.main:app --port 8000