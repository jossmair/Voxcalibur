# WER, mise en forme et ponctuation courte — décisions de la 1.2.0

## Ce que les sources établissent

Le [cours audio Hugging Face sur les métriques ASR](https://huggingface.co/learn/audio-course/chapter5/evaluation) décrit le WER comme une distance lexicale entre référence et hypothèse ; casse et ponctuation peuvent être retirées par la normalisation. Les chiffres et les mots ne deviennent pas automatiquement équivalents.

[NVIDIA explique la normalisation inverse](https://developer.nvidia.com/blog/text-normalization-and-inverse-text-normalization-with-nvidia-nemo/) comme une étape de passage de la forme parlée à la forme écrite pour améliorer la lisibilité. La [documentation NeMo](https://docs.nvidia.com/nemo-framework/user-guide/24.12/nemotoolkit/nlp/text_normalization/wfst/wfst_text_normalization.html) la distingue de la reconnaissance acoustique elle-même.

Ainsi, « dix-sept » → « 17 » peut convenir à l’utilisateur tout en augmentant le WER par rapport à une référence en lettres. Un WER brut plus bas ne prouve pas que chaque mise en forme soit erronée. Une règle universelle qui retirerait la ponctuation sous cinq mots n’est pas établie par ces sources : c’est une préférence de produit.

## Décisions

- **Sortie du moteur** devient le mode par défaut pour les nombres : aucune réécriture chiffres/lettres. Ce mode conserve aussi les chiffres déjà produits par le moteur.
- Les conversions **En chiffres** et **En lettres** restent disponibles. Les unités abrégées restent une option indépendante et deviennent désactivées par défaut.
- Le dictionnaire est toujours appliqué : il s’agit de corrections explicitement enregistrées par l’utilisateur.
- **Dictées courtes sans ponctuation** devient une option indépendante, cochée par défaut pour conserver ce comportement historique. Décochée, elle garde la ponctuation produite par le moteur.
- Le seuil historique est conservé : **moins de cinq mots**, donc un à quatre. À cinq mots exactement, la ponctuation n’est pas retirée par cette règle. Décimales, heures, apostrophes et liens restent protégés.
- Le changement est immédiat, conservé au redémarrage et ne recharge pas le modèle.

## Mise à jour des profils existants

La paire d’anciens réglages par défaut « chiffres + unités abrégées » est remplacée une seule fois par « sortie du moteur + unités non abrégées ». Le dictionnaire, la langue, la touche et les autres réglages sont conservés. Les choix personnalisés différents de cette paire sont conservés ; un choix explicite effectué en 1.2.0 n’est plus réinitialisé. Les sauvegardes de préférences continuent de fonctionner.

## Vérification et limites

Le modèle, le décodeur et les enregistrements ne sont pas modifiés pour améliorer le chiffre affiché. La campagne FLEURS 1.1.0 reste inchangée. La comparaison de la 1.2.0 réapplique le traitement nouveau aux **mêmes sorties brutes enregistrées**, sans nouvelle inférence ni nouvelle collecte. Elle est publiée comme une relecture de pipeline, pas comme une nouvelle campagne acoustique.

La normalisation WER annoncée n’est pas modifiée après coup. Elle ne mesure pas la qualité de la ponctuation : la nouvelle case est une préférence d’écriture, pas une promesse de baisse du WER.
