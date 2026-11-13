# Protocole terrain français — proposé, collecte non réalisée

## Objectif

Évaluer la dictée sur des voix françaises réelles, plusieurs microphones physiques et plusieurs environnements enregistrés. Les résultats FLEURS constituent un point de comparaison sur de la parole lue ; ils ne valident pas ce protocole terrain.

## Plan de collecte proposé

- Au moins 30 personnes, avec des profils de voix et accents documentés sur la base de déclarations volontaires, sans déduire ces caractéristiques de l’audio.
- Trois types de microphones physiques : microphone intégré d’ordinateur, casque-micro et microphone USB. Documenter le modèle, la distance, le gain, le traitement audio et la fréquence d’échantillonnage.
- Trois conditions réellement enregistrées : pièce calme, bruit de ventilation et conversations ambiantes. Documenter le lieu par une catégorie, pas par une adresse ; mesurer le SNR quand une référence exploitable est disponible.
- Au moins 20 énoncés par combinaison, dont lecture, dictée spontanée, nombres/unités, noms propres, hésitations et pauses. Un plan complet représente 5 400 enregistrements ; tout écart au plan doit être publié.
- Un panel tenu à l’écart du développement. Aucun réglage du modèle, du dictionnaire ou de la normalisation sur le lot final de test.

Ce sont des objectifs de collecte, pas une description de données déjà réunies. Aucun seuil de qualité n’est déclaré atteint ; un objectif métier éventuel doit être fixé avant l’analyse.

## Données et autorisations

Avant enregistrement : consentement à la participation et choix séparé concernant la publication audio, des transcriptions et des métadonnées. Utiliser des identifiants de locuteur pseudonymes. Exclure les documents et identifiants personnels des phrases.

Le manifeste doit décrire chaque audio : `id`, `audio`, `text`, `sha256`, `speaker_id`, `microphone`, `environment`, et les paramètres de capture. Les références sont transcrites puis relues indépendamment. Conserver la version initiale, les arbitrages et les empreintes avant de lancer le système.

## Exécution et analyse

1. Geler la version de Voxcalibur, les modèles, le runtime, le matériel et les options. Publier leurs empreintes.
2. Évaluer la configuration par défaut, puis une condition de dictionnaire personnalisé distincte si souhaité.
3. Publier toutes les lignes prévues, les échecs et les hypothèses vides. Ne pas retirer a posteriori les cas difficiles.
4. Calculer WER/CER pondérés et les distributions par locuteur, microphone et environnement. Présenter les effectifs et les durées de chaque cellule.
5. Calculer les intervalles par rééchantillonnage des locuteurs et utiliser des comparaisons appariées pour les mêmes énoncés.
6. Mesurer séparément la fidélité de transcription, la latence de fin de dictée et la réussite du collage dans les applications.
7. Publier le protocole, le manifeste autorisé, les références autorisées, les sorties, les exclusions motivées et les scripts. Si l’audio ne peut être rendu public, indiquer clairement la limite de reproductibilité.

## Statut

**À collecter.** Le dépôt ne contient actuellement aucune campagne terrain couvrant les microphones et conditions ci-dessus. Les ajouts de bruit numérique aux enregistrements FLEURS sont étiquetés comme simulations.
