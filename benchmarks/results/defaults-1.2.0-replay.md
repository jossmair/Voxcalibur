# Voxcalibur 1.2.0 — sortie moteur préservée

**Relecture des sorties ASR déjà publiées, sans nouvelle inférence acoustique.** Le modèle et la normalisation WER ne changent pas. Les 676 enregistrements et 2 028 variantes viennent de la campagne FLEURS 1.1.0.

| Condition | Ancien défaut 1.1.0 | Nouveau défaut 1.2.0 |
| :-- | --: | --: |
| clean | 5.00 % | 4.62 % |
| white20 | 6.88 % | 6.47 % |
| white10 | 11.81 % | 11.41 % |

Les mots reconnus sont conservés dans les 2 028 cas. Le gain lexical vient de l’arrêt des conversions automatiques, pas d’une amélioration du modèle acoustique. Les conversions restent disponibles sur demande et le dictionnaire personnel reste actif.

La case « Dictées courtes sans ponctuation » est indépendante. Elle ne modifie pas ces scores, puisque cette normalisation ignore la ponctuation. Le seuil historique est strictement inférieur à cinq mots.

[Métadonnées et intervalles](defaults-1.2.0-replay.json) · [Détail par extrait](defaults-1.2.0-replay.csv) · [Campagne d’origine](fleurs-fr-test-2026-11-13.md) · [Sources et décisions](../../docs/RECHERCHE-WER-1.2.0.md)

Les bruits sont des ajouts numériques et les microphones/locuteurs uniques ne sont pas documentés. Les essais terrain restent à collecter. Références FLEURS : Google et contributeurs, [CC BY 4.0](https://huggingface.co/datasets/google/fleurs).
