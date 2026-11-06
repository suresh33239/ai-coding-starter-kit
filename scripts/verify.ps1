# Cross-platform PowerShell wrapper for the one Python verifier.
# Windows PowerShell 5.1 or PowerShell 7 can invoke this wrapper.
$ErrorActionPreference = 'Stop'
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$verifyScript = Join-Path $scriptRoot 'verify.py'

$pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($pythonLauncher) {
    & py -3 $verifyScript @args
    exit $LASTEXITCODE
}

$python3Launcher = Get-Command python3 -ErrorAction SilentlyContinue
if ($python3Launcher) {
    & python3 $verifyScript @args
    exit $LASTEXITCODE
}

$pythonLauncher = Get-Command python -ErrorAction SilentlyContinue
if ($pythonLauncher) {
    & python $verifyScript @args
    exit $LASTEXITCODE
}

Write-Error 'Python 3.11+ not found. Install Python and retry; verification did not run.'
exit 127
