param([string]$Repository = "jossmair/Voxcalibur")
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "Installez GitHub CLI depuis https://cli.github.com puis exécutez gh auth login." }
gh auth status
if ($LASTEXITCODE) { throw "Connectez GitHub CLI avec gh auth login." }
$assets = @("dist/Voxcalibur-1.0.0-Portable.zip", "dist/Voxcalibur-1.0.0-Installation.zip", "dist/Voxcalibur-1.0.0-Sources.zip", "dist/SHA256SUMS.txt")
foreach ($asset in $assets) { if (-not (Test-Path -LiteralPath $asset)) { throw "Distribution absente : $asset" } }
gh repo view $Repository --json name *> $null
if ($LASTEXITCODE -eq 0) { throw "Le dépôt existe déjà : vérifiez-le avant toute publication." }
gh repo create $Repository --private --source . --remote origin --push
if ($LASTEXITCODE) { throw "Création ou publication du dépôt échouée." }
gh release create v1.0.0 @assets --repo $Repository --title "Voxcalibur 1.0.0" --notes-file docs/RELEASE-1.0.0.md
if ($LASTEXITCODE) { throw "Publication des archives échouée ; le dépôt source a été créé." }
