# Validation continue

Le workflow [Windows validation](https://github.com/jossmair/Voxcalibur/actions/workflows/ci.yml) s’exécute à chaque push et pull request, et peut être lancé manuellement.

## Contrôles

- Windows Server 2025, Python 3.11 et 3.12, dépendances de `requirements-lock.txt`.
- Cohérence des dépendances avec `pip check`.
- Analyse Ruff de l’application, des scripts et des tests.
- Suite pytest complète, avec Qt hors écran et profil de données isolé.
- Compilation PyInstaller et contrôle de la ligne de commande sur Python 3.11.
- Rapports JUnit et journal de compilation conservés pendant 14 jours, y compris en cas d’échec.

Les actions officielles sont épinglées par SHA de commit. Les permissions sont limitées à la lecture du contenu ; les identifiants Git ne sont pas conservés par checkout. Un nouveau changement annule l’exécution devenue obsolète sur la même référence.

## Ce que le voyant vert mesure

La CI contrôle le code, les tests et la compilation sans télécharger les modèles ni ouvrir un microphone. Le test de l’exécutable est `--help`, pas une mesure de transcription. Les tests de reconnaissance simulés vérifient le comportement du programme, pas la précision acoustique.

La précision sur voix humaines est évaluée dans une [campagne séparée et reproductible](../benchmarks/README.md), avec des données audio documentées. Un résultat WER ne peut pas être déduit du nombre de tests automatisés. Les rapports historiques de la version 1.1.0 restent des instantanés ; le badge du README donne l’état courant des exécutions GitHub.

La présence du workflow n’installe pas de règle de protection de branche : le workflow se déclenche sur chaque changement, mais les règles de fusion du dépôt restent distinctes.

## Première exécution vérifiée

[Les deux jobs ont réussi sur GitHub](https://github.com/jossmair/Voxcalibur/actions/runs/43465673614), au commit `a75d971b`. La [preuve structurée](validation/ci-first-success.json) conserve les liens des jobs ; le badge du README indique l’état courant.
