#!/usr/bin/env pwsh
<#
stop-logs.ps1
Para todos os jobs de captura de logs em background e remove arquivos de log.
Uso: Execute na raiz do repositório ou use .\scripts\stop-logs.ps1
#>

Write-Output "Stopping background log jobs (name pattern: log_*)..."
Get-Job -Name 'log_*' | Stop-Job -ErrorAction SilentlyContinue
Get-Job -Name 'log_*' | Remove-Job -ErrorAction SilentlyContinue

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# logs directory is expected to be one level up from scripts (../logs)
$logsPath = Join-Path $scriptDir '..\logs\*.log'
$logsPath = (Resolve-Path -Path $logsPath -ErrorAction SilentlyContinue).Path 2>$null

if ($null -ne $logsPath) {
    Write-Output "Removing log files: $logsPath"
    Remove-Item -Path $logsPath -Force -ErrorAction SilentlyContinue
} else {
    # Fallback: try relative path from current working directory
    $fallback = "./logs/*.log"
    Write-Output "No logs found at expected path; attempting fallback: $fallback"
    Remove-Item -Path $fallback -Force -ErrorAction SilentlyContinue
}

Write-Output "Stopped log jobs and removed log files (if any)."
# docker compose down