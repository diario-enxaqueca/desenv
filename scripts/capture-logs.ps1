# capture-logs.ps1
# Uso: execute este script na raiz do repositório (PowerShell 5.1)
# Ele irá subir os containers (docker compose up -d --build) e criar um job por serviço
# que segue os logs e grava em arquivos separados dentro de ./logs/<service>.log

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
