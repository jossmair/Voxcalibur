# Voxcalibur 1.1.0

**La parole est votre pouvoir.** Une application de dictée vocale locale pour Windows, avec le moteur et les modèles inclus.

## Télécharger

| Édition | Pour commencer | Archive |
| :-- | :-- | :-- |
| **Installable** | Décompressez, puis lancez `Installer-Voxcalibur.exe`. Gardez les quatre fichiers ensemble. | [Télécharger · 1,89 Go](https://github.com/jossmair/Voxcalibur/releases/download/v1.1.0/Voxcalibur-1.1.0-Installation.zip) |
| **Portable** | Décompressez entièrement, puis lancez `Voxcalibur.exe`. Conservez les dossiers fournis avec l’exécutable. | [Télécharger · 1,87 Go](https://github.com/jossmair/Voxcalibur/releases/download/v1.1.0/Voxcalibur-1.1.0-Portable.zip) |

Windows 10/11 x64 · 16 Go de RAM conseillés · Aucun compte ni clé API requis.

## Les nouveautés

- **Langues à portée de main** : palette avec recherche et navigation au clavier ; votre choix est conservé au redémarrage.
- **Un choix CPU/GPU explicite** : interrupteur d’accélération CUDA/Vulkan, disponible lorsque le matériel est compatible.
- **Un accueil plus réactif** : la fenêtre s’affiche avant la fin de la détection matérielle, réalisée en arrière-plan.
- **Un repli CPU plus robuste** : après un échec GPU, le logiciel conserve temporairement ce choix ; un changement de matériel ou de runtime déclenche une nouvelle évaluation.
- **Des corrections adaptées à la langue** : les corrections françaises sont réservées au français et les réglages sont réappliqués après un changement de langue.
- **Une interface Voxcalibur affinée** : « Dictée » et « Locale » sur deux lignes, logo intégré et en-tête simplifié.
- **Un moteur plus facile à relancer** : la fermeture tolère les handles natifs déjà fermés ; les animations inutiles s’arrêtent au repos.

Parakeet Ultra détecte la langue depuis l’audio. Le sélecteur conserve votre préférence et règle les corrections ; il ne force pas le décodeur natif.

## Vérifications de cette version

**267 tests automatisés réussis.** Transcription réelle vérifiée avec l’exécutable sur CPU et CUDA. Installation et désinstallation vérifiées dans un profil isolé. Le moteur Vulkan est également inclus.

[Empreintes SHA-256](https://github.com/jossmair/Voxcalibur/releases/download/v1.1.0/SHA256SUMS.txt) · [Code source de la version](https://github.com/jossmair/Voxcalibur/releases/download/v1.1.0/Voxcalibur-1.1.0-Sources.zip) · [Guide d’utilisation](https://github.com/jossmair/Voxcalibur/blob/main/docs/UTILISATION.md)

Voxcalibur fonctionne indépendamment de la suite Ergonatus et conserve ses propres réglages. Une mise à jour préserve le dictionnaire et les préférences Voxcalibur. Les deux éditions utilisent le profil Windows pour les préférences.
