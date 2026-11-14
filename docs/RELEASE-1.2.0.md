# Voxcalibur 1.2.0

**Les mots du moteur d’abord, la mise en forme à votre choix.**

- Nouveau choix **Sortie du moteur / En chiffres / En lettres** pour les nombres. Par défaut, Voxcalibur conserve l’écriture produite par le moteur.
- Les unités ne sont plus automatiquement abrégées par défaut ; l’option reste disponible.
- Nouvelle case **Dictées courtes sans ponctuation** : cochée, elle supprime la ponctuation de phrase pour les dictées de moins de cinq mots ; décochée, elle conserve celle du moteur. Le seuil reste un à quatre mots, pas cinq.
- Le dictionnaire, les réglages de langue et de GPU et les raccourcis restent disponibles.
- Les changements de texte s’appliquent immédiatement, sans recharger le modèle, et sont conservés.

L’ancienne paire par défaut « chiffres + unités abrégées » est migrée une seule fois vers les nouveaux réglages. Les autres choix personnalisés sont conservés. Vous pouvez réactiver les conversions quand vous le souhaitez.

La reconnaissance acoustique n’a pas été changée. La vérification WER réutilise les sorties brutes de la campagne FLEURS publiée ; elle distingue la reconnaissance du formatage. Les bruits de cette campagne restent simulés et les essais terrain multi-microphones restent à collecter.

[Recherche et décisions](https://github.com/jossmair/Voxcalibur/blob/main/docs/RECHERCHE-WER-1.2.0.md)

**Installable** : décompressez l’archive et lancez `Installer-Voxcalibur.exe`, avec les quatre fichiers ensemble.
**Portable** : décompressez entièrement et lancez `Voxcalibur.exe`. Les modèles et les moteurs CPU/CUDA/Vulkan sont inclus.

**Vérification : 294 tests réussis.** Les options de texte et les sept préférences ont également été vérifiées dans l’exécutable compilé. [Relecture WER documentée](https://github.com/jossmair/Voxcalibur/blob/main/benchmarks/results/defaults-1.2.0-replay.md).
