param([string]$Repository = "jossmair/Voxcalibur")
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$version = [regex]::Match((Get-Content app/__init__.py -Raw), '__version__ = "([^"]+)"').Groups[1].Value
if (-not $version) { throw "Version de l'application introuvable." }
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "Installez GitHub CLI depuis https://cli.github.com puis exécutez gh auth login." }
gh auth status
if ($LASTEXITCODE) { throw "Connectez GitHub CLI avec gh auth login." }
$assets = @("dist/Voxcalibur-$version-Portable.zip", "dist/Voxcalibur-$version-Installation.zip", "dist/Voxcalibur-$version-Sources.zip", "dist/SHA256SUMS.txt")
foreach ($asset in $assets) { if (-not (Test-Path -LiteralPath $asset)) { throw "Distribution absente : $asset" } }
gh repo view $Repository --json name *> $null
if ($LASTEXITCODE) {
    gh repo create $Repository --private --source . --remote origin --push
} else {
    $remote = git remote get-url origin
    if ($LASTEXITCODE -or $remote -ne "https://github.com/$Repository.git") { throw "Le dépôt distant local ne correspond pas à $Repository." }
    git push origin main
}
if ($LASTEXITCODE) { throw "Publication du dépôt échouée." }
gh release create "v$version" @assets --repo $Repository --title "Voxcalibur $version" --notes-file "docs/RELEASE-$version.md"
if ($LASTEXITCODE) { throw "Publication des archives échouée." }
