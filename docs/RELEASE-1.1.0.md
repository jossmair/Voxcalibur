# Voxcalibur 1.1.0

Cette version reprend les ajouts actuels de Transcrinator dans la suite Ergonatus qui manquaient dans Voxcalibur 1.0.0, tout en conservant une installation indépendante et les moteurs hors ligne.

- Langues : choix avec recherche, navigation clavier et détection automatique Parakeet.
- Choix de langue et de CPU/GPU conservés au redémarrage.
- Interrupteur « Booster avec la carte graphique », désactivé si aucun GPU compatible n'est disponible.
- Affichage rapide de l'interface, détection du matériel en arrière-plan.
- Repli CPU temporairement mémorisé après un échec GPU, nouvelle tentative quand le matériel ou les runtimes changent.
- Arrêt du moteur plus robuste après une défaillance native.
- Corrections françaises réservées au français ; reconfiguration correcte lors d'un changement de langue.
- Animations inutiles arrêtées au repos.
- Titre d'accueil « Dictée » puis « Locale » sur deux lignes ; suppression de la petite mention dans l'en-tête.

Le modèle Ultra détecte la langue depuis l'audio : le sélecteur ne force pas le décodage natif. Il conserve votre préférence et réserve les corrections françaises au choix Français.

Installation et désinstallation réelles vérifiées dans un profil isolé. 267 tests automatisés réussis. Transcriptions réelles CPU et CUDA vérifiées avec l’exécutable compilé ; interface compilée identique à la capture de référence. Les modèles et les moteurs CPU, Vulkan et CUDA sont inclus. Aucun composant de la suite n'est nécessaire.

**Portable** : décompresser entièrement puis lancer Voxcalibur.exe.
**Installation** : décompresser, garder les quatre fichiers ensemble puis lancer Installer-Voxcalibur.exe. La mise à jour conserve les réglages et le dictionnaire Voxcalibur.
