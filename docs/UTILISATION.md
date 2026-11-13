# Bien démarrer avec Voxcalibur

[← Retour à la présentation](../README.md)

## Choisir une édition

### Installer Voxcalibur sur votre PC

1. Téléchargez la **version installable** dans les [versions GitHub](https://github.com/jossmair/Voxcalibur/releases/latest).
2. Décompressez entièrement l’archive.
3. Gardez ensemble `Installer-Voxcalibur.exe`, `payload.zip`, `payload.json` et `uninstaller.exe`.
4. Lancez `Installer-Voxcalibur.exe` et laissez l’installation se terminer.

L’installation se fait pour votre compte Windows, sans droits administrateur. La désinstallation est disponible depuis les applications Windows.

### Utiliser la version portable

1. Téléchargez la **version portable**.
2. Décompressez entièrement l’archive dans un dossier disposant de suffisamment d’espace.
3. Lancez `Voxcalibur.exe`.

Conservez les dossiers `_internal`, `models` et `runtimes` avec l’exécutable. Les deux éditions incluent les modèles et les moteurs ; Python n’est pas nécessaire. La version portable conserve elle aussi ses préférences dans le profil Windows.

## Votre première dictée

1. Autorisez votre microphone dans les paramètres Windows et vérifiez le microphone par défaut.
2. Ouvrez Voxcalibur et attendez l’état **Prêt**.
3. Placez le curseur dans l’application où vous voulez écrire.
4. Appuyez puis relâchez **Maj gauche**, puis parlez lorsque l’écoute commence.
5. Appuyez puis relâchez à nouveau **Maj gauche** pour terminer.

Le texte complet est copié et collé dans la fenêtre active au moment où il est prêt. Il reste dans le presse-papiers. Vous pouvez changer de fenêtre pendant la dictée ; le collage suit le focus courant de Windows.

## Les réglages

| Réglage | Ce qu’il change |
| :-- | :-- |
| **Touche de déclenchement** | Maj gauche/droite, Ctrl gauche/droite ou une touche de F1 à F12. Appuyez sur la touche seule pour déclencher. |
| **Langue de dictée** | Une palette avec recherche et navigation clavier. Votre choix est conservé au prochain lancement. |
| **Booster avec la carte graphique** | Active l’accélération CUDA/Vulkan compatible. Désactivé, le moteur utilise le CPU. Le bouton est indisponible si aucun GPU compatible n’est détecté. |
| **Nombres en chiffres** | En français, choisit entre `25` et `vingt-cinq`. |
| **Unités abrégées** | En français, transforme une quantité telle que `250 grammes` en `250 g`. |
| **Démarrage Windows** | Active ou désactive le lancement avec votre session Windows. |

Parakeet Ultra détecte la langue de l’audio. Le sélecteur de langue ne force pas le décodeur natif ; il conserve votre préférence et règle l’application des corrections françaises. Pour une autre langue ou la détection automatique, ces corrections françaises ne sont pas appliquées.

En cas d’échec au chargement GPU, le moteur réessaie sur CPU. Ce repli peut être mémorisé pendant dix minutes afin d’éviter des échecs répétés ; un changement de matériel ou de runtime invalide ce cache.

## Votre dictionnaire

Ouvrez **Dictionnaire**, ajoutez un mot, puis choisissez sa catégorie : noms propres, villes, produits ou mots techniques. La colonne **Erreurs habituelles** permet d’indiquer les variantes à remplacer.

Exemple : nom correct **Josselin**, variantes **Jocelyn, Joselin**. Cliquez sur **Enregistrer** pour conserver les modifications. Fermer avec la croix les abandonne.

Sur le runtime CUDA de guidage compatible, les noms propres et les villes peuvent aussi guider la reconnaissance. Les autres catégories conservent leurs corrections finales en français.

## L’orbe et le menu

L’orbe indique l’activité de la dictée. Il se déploie pendant l’écoute et le traitement, puis redevient compact après le collage. Vous pouvez le déplacer.

Un clic droit sur l’orbe ou sur l’icône près de l’horloge ouvre le menu : ouvrir Voxcalibur, afficher le hub, récupérer le texte conservé ou quitter. Le microphone reste fermé en dehors d’une dictée.

## Si le texte n’apparaît pas

Le texte reste dans le presse-papiers : essayez de le coller manuellement. Le menu propose également la récupération du texte conservé. Windows peut empêcher le collage dans une fenêtre ayant des droits supérieurs à ceux de Voxcalibur.

Si le microphone n’est pas disponible, vérifiez son autorisation Windows et le périphérique d’entrée par défaut. Si les modèles ou les runtimes sont signalés comme absents, décompressez à nouveau l’archive complète en conservant tous ses dossiers.

## Vos données et votre installation

- Préférences : `%LOCALAPPDATA%/Voxcalibur`.
- Application installée : `%LOCALAPPDATA%/Programs/Voxcalibur`.
- Voxcalibur utilise ses propres raccourcis, son verrou d’instance et ses entrées Windows.
- Le profil Transcrinator et la suite Ergonatus restent indépendants.
- La transcription est réalisée sur votre ordinateur avec les modèles livrés. Aucun compte ni clé API n’est demandé.

[Retour à Voxcalibur](../README.md) · [Télécharger la dernière version](https://github.com/jossmair/Voxcalibur/releases/latest)
