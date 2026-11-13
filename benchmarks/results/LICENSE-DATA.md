# Attribution des données de référence

Les références textuelles incluses dans les rapports JSON et CSV proviennent de FLEURS — Few-shot Learning Evaluation of Universal Representations of Speech, Google et contributeurs.

- Source officielle : https://huggingface.co/datasets/google/fleurs
- Licence des données de référence : Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/
- Sous-ensemble : français `fr_fr`, split `test` ; révision et SHA-256 dans `../corpora/fleurs-fr-test.json`.
- Transformations documentées : conversion audio float32/PCM16, ajout de bruit numérique et normalisation pour la mesure. Les fichiers audio ne sont pas redistribués ici.

Le code des outils reste sous la licence MIT du dépôt. Les transcriptions produites, métadonnées d’exécution et scores sont identifiés séparément des références dans les rapports. Conservez cette attribution lorsque vous redistribuez les références issues du corpus.
