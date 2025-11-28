#!/usr/bin/env pwsh
<#
Stops background log capture jobs named 'log_*' and removes log files in the repository `logs` folder.
Run this from the repository root before `./scripts/capture-logs.ps1`.
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
docker compose down

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# repoRoot is the parent of the scripts directory (assume script is in ./scripts)
$repoRoot = Resolve-Path (Join-Path $scriptDir '..')
Set-Location -Path $repoRoot

$logsDir = Join-Path $repoRoot 'logs'
if (-Not (Test-Path $logsDir)) {
    New-Item -Path $logsDir -ItemType Directory | Out-Null
}

Write-Host "Bringing up containers (build)..."
# docker compose up -d --build
docker compose build --no-cache
docker compose up -d

Write-Host "Starting log capture jobs (output -> $logsDir)"

# Get list of services from docker compose
$services = docker compose ps --services
if (-not $services) {
    Write-Warning "Nenhum serviço retornado por 'docker compose ps --services'"
}

foreach ($s in $services) {
    $jobName = "log_$s"
    # Skip if a job with same name already running
    $existing = Get-Job -Name $jobName -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "Job $jobName já existe. Pulando. Use Get-Job para gerenciar."
        continue
    }

    $file = Join-Path $logsDir "$s.log"
    Write-Host "Iniciando captura de logs para serviço: $s -> $file"

    Start-Job -Name $jobName -ScriptBlock {
        param($service, $filePath, $workDir)
        try {
            Set-Location -Path $workDir
        } catch {
            # If we can't set location, emit warning but continue (docker may still be in PATH)
            Write-Warning "Could not Set-Location to $workDir inside job: $_"
        }
        # Use explicit compose file path so the job can find the configuration
        $composeFile = Join-Path $workDir 'docker-compose.yml'
        docker compose -f $composeFile logs --no-color -f $service 2>&1 | Tee-Object -FilePath $filePath
    } -ArgumentList $s, $file, $repoRoot | Out-Null
}

Write-Host "Jobs iniciados. Para listar: Get-Job"
Write-Host "Para parar e remover os jobs (quando quiser):"
Write-Host "  Get-Job -Name 'log_*' | Stop-Job; Get-Job -Name 'log_*' | Remove-Job"
Write-Host "Arquivos de log em: $logsDir"
