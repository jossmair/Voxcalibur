# Mesurer la précision de Voxcalibur

Les tests automatisés de l’application et la précision de reconnaissance sont deux validations distinctes. Aucun taux de précision sur microphones réels ne peut être déduit du nombre de tests pytest.

## Évaluation publique reproductible

La première campagne utilise **tout le split de test français de Google FLEURS** : 676 enregistrements humains, environ 117 minutes. La révision du corpus et le SHA-256 du fichier source sont épinglés dans [le catalogue](corpora/fleurs-fr-test.json).

Chaque enregistrement est évalué dans trois conditions : audio d’origine, bruit blanc gaussien ajouté à 20 dB SNR, bruit blanc ajouté à 10 dB SNR. Le bruit ajouté est une **simulation**, pas un enregistrement dans un bureau ou un café. Les références ne sont pas utilisées pour adapter le dictionnaire ou le modèle.

Le catalogue FLEURS ne fournit pas d’identifiants de locuteur, de modèle de microphone ou de niveau de bruit d’origine pour ces lignes. Le nombre de voix uniques, la diversité des microphones et les environnements réels ne sont donc pas établis par cette campagne.

## Reproduire

Depuis la racine du dépôt, avec les dépendances de l’application installées :

```powershell
.venv/Scripts/python.exe -m pip install -r requirements-benchmark.txt
.venv/Scripts/python.exe -m scripts.prepare_fleurs --allow-download
$env:VOXCALIBUR_BUNDLE = 'C:/chemin/vers/Voxcalibur-1.1.0'
$env:VOXCALIBUR_DATA = Join-Path (Get-Location) 'build/benchmark-profile'
.venv/Scripts/python.exe -m scripts.evaluate_corpus --manifest vendor/fleurs-fr-test/manifest.json --output build/fleurs-fr-report.json --acceleration gpu
```

`--acceleration cpu` permet une mesure CPU séparée. `--limit 3` est destiné uniquement au contrôle du pipeline ; le rapport indique alors explicitement qu’il ne couvre pas le split complet. Les enregistrements audio restent dans `vendor`, hors Git. Le téléchargement n’a lieu qu’avec `--allow-download` ; la transcription normale ne télécharge jamais ce corpus.

Le rapport contient les références et hypothèses du corpus de test explicite. Ne publiez pas de rapport provenant d’enregistrements personnels sans les autorisations correspondantes.

## Mesures

- WER pondéré par le nombre de mots de référence : somme des substitutions, suppressions et insertions divisée par le nombre total de mots.
- WER de l’ASR brut et du texte après les corrections françaises par défaut, publiés séparément.
- CER sur les mots normalisés joints par des espaces simples.
- Normalisation NFC, casse Unicode ignorée et ponctuation séparatrice ; accents et différences chiffres/lettres conservés.
- Hypothèses vides comptées comme suppressions, jamais retirées du score.
- Intervalle à 95 % par bootstrap déterministe. Rééchantillonnage par locuteur seulement si tous les identifiants sont connus ; sinon par enregistrement, sans interprétation comme intervalle sur de nouveaux locuteurs.
- Temps d’inférence, temps de finalisation, facteur de temps réel, backend effectif, matériel, empreintes modèle/runtime/audio/code et révision du corpus.

Le script historique `scripts/benchmark.py` reste un contrôle de fonctionnement sur trois phrases ; ses sorties sont explicitement marquées comme hors campagne de précision.

## Essais terrain à réaliser

La diversité des microphones physiques et les conditions bruyantes réellement enregistrées restent à évaluer. Le [protocole terrain](PROTOCOL.md) définit une collecte distincte avec locuteurs pseudonymisés, microphones documentés, conditions acoustiques et consentements. Le bruit ajouté à FLEURS ne remplace pas cette étape.

## Attribution

FLEURS — *Few-shot Learning Evaluation of Universal Representations of Speech*, Google et contributeurs. Source : https://huggingface.co/datasets/google/fleurs ; licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Modifications d’évaluation : conversion float32 vers PCM16, normalisation textuelle documentée et variantes de bruit synthétique. Les fichiers audio d’origine ne sont pas redistribués dans le dépôt. Les références dérivées du corpus dans les rapports conservent cette attribution et cette licence, distincte de la licence MIT du code.
