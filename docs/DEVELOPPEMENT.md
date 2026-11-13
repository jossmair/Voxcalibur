# Développer et compiler Voxcalibur

[← Retour à la présentation](../README.md)

## Environnement

Windows x64, Python 3.11 ou supérieur, Git. Les versions compilées sont autonomes ; ces outils concernent uniquement le développement.

```powershell
git clone https://github.com/jossmair/Voxcalibur.git
cd Voxcalibur
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-lock.txt
.venv/Scripts/python.exe -m pytest -q
```

Les dépendances sont figées dans `requirements-lock.txt`. Les tests Qt utilisent une plateforme hors écran. La version 1.1.0 a passé 267 tests ; les rapports sont dans `docs/validation`.

## Organisation du code

| Dossier | Rôle |
| :-- | :-- |
| `app/core` | Réglages, contrôleur, capture, raccourcis, insertion et traitement du texte |
| `app/engines` | Intégration Parakeet, processus natif et guidage du vocabulaire |
| `app/services` | Choix du backend, modèles, diagnostics et validations |
| `app/ui` | Fenêtre principale, orbe, langues, dictionnaire et préférences |
| `assets` | Identité Voxcalibur, visuels et licences |
| `installer` | Installation par utilisateur et désinstallation |
| `scripts` | Compilation, empaquetage et outils de vérification |
| `tests` | Tests automatisés |

Les symboles ABI natifs historiques `transcrinator_*` restent inchangés pour conserver la compatibilité avec les runtimes vérifiés. Ils ne créent pas de dépendance envers la suite.

## Isoler un profil de développement

```powershell
$env:VOXCALIBUR_DATA = Join-Path (Get-Location) 'build/dev-profile'
$env:VOXCALIBUR_BUNDLE = 'C:/chemin/vers/un/bundle/complet'
.venv/Scripts/python.exe -m app.main --show
```

`VOXCALIBUR_DATA` désigne les préférences et caches. `VOXCALIBUR_BUNDLE` désigne un ensemble existant contenant `models`, `runtimes` et `bundle.json`. Les poids et binaires volumineux sont livrés dans les distributions et exclus de l’historique Git.

## Compiler les distributions

Les modèles et runtimes réels doivent être présents avant la compilation. L’empaqueteur vérifie les modèles par SHA-256 et ne les télécharge pas automatiquement.

```powershell
$env:VOXCALIBUR_BUNDLE = 'C:/chemin/vers/un/bundle/complet'
./scripts/build.ps1
```

Le script exécute les tests, prépare l’icône et les licences, compile l’application avec PyInstaller, ajoute les moteurs, puis construit l’installation et les archives de distribution.

Les sorties dans `dist` comprennent :

- `Voxcalibur-<version>-Portable.zip` : application, modèles et runtimes.
- `Voxcalibur-<version>-Installation.zip` : installateur et son ensemble de fichiers.
- `Voxcalibur-<version>-Sources.zip` : instantané des sources.
- `SHA256SUMS.txt` : empreintes des trois archives.

## Provenance et validations

Les ajouts de Transcrinator dans Ergonatus ont été repris dans la 1.1.0 : langues, réglage GPU, démarrage rapide, repli CPU mémorisé, fermeture native et traitements adaptés à la langue. Leur provenance est documentée dans `docs/validation/suite-feature-parity-110.json`.

Les essais compilés CPU/CUDA, l’interface et l’installation isolée sont documentés dans `docs/validation`. La prise en charge de Vulkan est incluse ; les essais de transcription réels rapportés pour cette version concernent CPU et CUDA.

## Publication

Le script `scripts/publish_github.ps1` utilise GitHub CLI et la version déclarée dans `app/__init__.py`. Il publie le code et une nouvelle version accompagnée des archives déjà construites. GitHub CLI doit être installé et connecté au compte autorisé.

Le code est sous licence MIT. Les modèles et runtimes conservent leurs licences propres ; consultez `assets/licenses` et les fichiers de licences distribués avec les modèles.
