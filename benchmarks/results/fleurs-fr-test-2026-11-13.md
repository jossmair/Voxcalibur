# Voxcalibur — mesure sur le split de test FLEURS français

**676 enregistrements humains · 332 phrases distinctes · 117.1 minutes uniques · 17,997 mots de référence.**

2028 transcriptions, sur 3 variantes des mêmes enregistrements. Le split de test épinglé est évalué en entier.

## Résultats

Le WER est un taux d’erreur : plus il est bas, mieux c’est. Il est pondéré par les mots de référence, pas moyenné par phrase.

| Condition | Extraits | WER après corrections | IC 95 % par enregistrement | WER ASR brut | CER après corrections | RTF | Hypothèses vides |
| :-- | --: | --: | :-- | --: | --: | --: | --: |
| Audio d’origine | 676 | 5.00 % | [4.52 % ; 5.46 %] | 4.62 % | 1.87 % | 0.054 | 0 |
| Bruit blanc ajouté · 20 dB SNR | 676 | 6.88 % | [6.33 % ; 7.44 %] | 6.47 % | 2.76 % | 0.054 | 0 |
| Bruit blanc ajouté · 10 dB SNR | 676 | 11.81 % | [11.01 % ; 12.65 %] | 11.41 % | 5.38 % | 0.054 | 0 |

## Effet des corrections françaises

Sur l’audio d’origine, le nombre d’erreurs lexicales augmente pour 69 enregistrements et diminue pour 10, avec un solde de +67 erreurs. Les deux séries de scores sont conservées.

L’écart comprend des différences de représentation : par exemple, dans `fleurs-fr-test-00004`, le moteur écrit « dix-sept » et le réglage par défaut le convertit en « 17 ». La référence conserve les lettres. La normalisation annoncée préserve cette différence et la compte comme erreur lexicale, même si la quantité est la même. Les scores n’ont pas été recalculés avec une normalisation plus favorable après observation des résultats.


## Portée exacte

- FLEURS est de la parole lue publique. La représentativité de la dictée spontanée n’est pas établie.
- **Le nombre d’enregistrements n’est pas le nombre de personnes.** Les identifiants de locuteur ne sont pas fournis ; le nombre de voix uniques est inconnu.
- Les modèles de microphones et les environnements d’origine sont inconnus. Aucune diversité de microphones physiques n’est démontrée ici.
- Le bruit blanc est ajouté numériquement. Il ne représente pas une collecte réelle en café, bureau ou pièce réverbérante.
- Les intervalles bootstrap portent sur les enregistrements et ne sont pas des intervalles de généralisation à de nouveaux locuteurs. Des phrases se répètent dans le corpus.
- Le chevauchement éventuel entre ce corpus public et l’entraînement du modèle n’est pas établi.
- Étiquettes fournies par le corpus : {'female': 175, 'male': 501}. Elles ne constituent pas un recensement des personnes enregistrées.

Les [essais terrain multi-microphones et en bruit réel](../PROTOCOL.md) restent **à collecter**. Aucun objectif de qualité métier n’a été déclaré atteint sur cette base.

## Configuration gelée

- Application : Voxcalibur 1.1.0 ; [code mesuré](https://github.com/jossmair/Voxcalibur/tree/a75d971b2e7b112daea2210f544ae9ad7e8507ff).
- Backend effectif : `CUDA0` ; GPU détecté : NVIDIA T500.
- CPU : Intel64 Family 6 Model 140 Stepping 1, GenuineIntel ; 4 cœurs physiques ; RAM : 15.73 Gio.
- Python 3.11.9 ; NumPy 2.4.6 ; soxr 1.1.0.
- Runtime : `parakeet-context-sm75.dll` ; SHA-256 `4073941ad1d69760efc98f3c5a0bb8480c121c894454f66abb031e72df8c212f`.
- Modèle : SHA-256 `c2fb452a9df468a141012b01c8c168a25ce93f710897c7de6e353c6cc250986a`.
- Dictionnaire vide, français, nombres en chiffres, unités abrégées, segmentation et VAD par défaut.
- Graine du bruit et du bootstrap : `20261113`. Le SNR est calculé sur l’enregistrement entier, pauses comprises. Un gain commun limite les pics du mélange à 0,999.

## Méthode et fichiers

Normalisation WER : NFC, Unicode casefold, Unicode word tokens; accents and digits preserved. La casse et la ponctuation ne sont pas notées. Les accents et les différences chiffres/lettres sont conservés. Les scores ne sont pas directement comparables à ceux d’une autre normalisation.

Le CER s’applique aux mots normalisés joints par des espaces simples. Une hypothèse vide contribue autant de suppressions qu’il y a de mots de référence. Le RTF couvre l’ingestion audio et le moteur en traitement hors temps réel, divisés par la durée audio. Chargement initial, préparation, corrections textuelles, scores et collage sont exclus ; ce n’est pas une mesure de la latence après arrêt au microphone.

[Rapport JSON complet](fleurs-fr-test-2026-11-13.json) · [Détail CSV](fleurs-fr-test-2026-11-13.csv) · [Reproduire](../README.md) · [Corpus épinglé](../corpora/fleurs-fr-test.json)

Attribution : Google et contributeurs, FLEURS — Few-shot Learning Evaluation of Universal Representations of Speech. [Source officielle](https://huggingface.co/datasets/google/fleurs), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Conversion PCM16, bruit synthétique et normalisation documentés ; les fichiers audio ne sont pas redistribués.
