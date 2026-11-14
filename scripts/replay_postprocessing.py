"""Compare text policies on stored ASR outputs without new acoustic inference."""

import argparse
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path
import subprocess

from app import __version__
from app.core.settings import Settings
from app.core.text_options import TextPostprocessor
from scripts.benchmark_metrics import aggregate, bootstrap_wer, tokens


def replay(source, output):
    source, output = Path(source), Path(output)
    previous = json.loads(source.read_text(encoding="utf-8"))
    if not previous.get("run_completed") or not previous.get("is_full_split"):
        raise ValueError("A completed full-split ASR report is required")
    settings = Settings()
    processor = TextPostprocessor(
        [], settings.number_style, settings.abbreviate_units, settings.short_dictation_unpunctuated
    )
    groups, rows = defaultdict(list), []
    for case in previous["cases"]:
        hypothesis = processor.apply(case["raw_hypothesis"])
        # The new defaults must not rewrite any recognized word in this corpus.
        if tokens(hypothesis) != tokens(case["raw_hypothesis"]):
            raise AssertionError(f"Default policy changed words: {case['id']}/{case['condition']}")
        groups[case["condition"]].append(dict(case["raw_metrics"], speaker_id=case.get("speaker_id")))
        rows.append(
            {
                "id": case["id"],
                "condition": case["condition"],
                "reference": case["reference"],
                "raw_hypothesis": case["raw_hypothesis"],
                "new_hypothesis": hypothesis,
                "previous_wer": case["metrics"]["wer"],
                "new_wer": case["raw_metrics"]["wer"],
                "recognized_words_preserved": True,
            }
        )
    summary = {}
    for condition in previous["conditions"]:
        result = aggregate(groups[condition])
        assert result["wer"] == previous["summary"][condition]["raw_asr"]["wer"]
        summary[condition] = {
            "previous_wer": previous["summary"][condition]["wer"],
            "new_defaults": result,
            "wer_95ci": bootstrap_wer(groups[condition], seed=previous["seed"]),
        }
    root = Path(__file__).resolve().parents[1]
    report = {
        "application_version": __version__,
        "evaluation_type": "stored_asr_postprocessing_replay",
        "new_acoustic_inference": False,
        "model_changed": False,
        "source_report": source.name,
        "source_report_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "asr_source_commit": previous["source_commit"],
        "postprocessing_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "postprocessor_sha256": hashlib.sha256((root / "app/core/text_options.py").read_bytes()).hexdigest(),
        "normalization": previous["normalization"],
        "recordings": previous["selected_recordings"],
        "evaluations": len(rows),
        "all_recognized_words_preserved": True,
        "settings": {
            "number_style": settings.number_style,
            "abbreviate_units": settings.abbreviate_units,
            "short_dictation_unpunctuated": settings.short_dictation_unpunctuated,
            "vocabulary": [],
        },
        "summary": summary,
        "limits": previous["limits"]
        + [
            "Punctuation is not scored by this WER normalization.",
            "This replays existing recognized text; it is not a new recording campaign.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    with output.with_suffix(".csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# Voxcalibur 1.2.0 — sortie moteur préservée",
        "",
        "**Relecture des sorties ASR déjà publiées, sans nouvelle inférence acoustique.** Le modèle et la normalisation WER ne changent pas. Les 676 enregistrements et 2 028 variantes viennent de la campagne FLEURS 1.1.0.",
        "",
        "| Condition | Ancien défaut 1.1.0 | Nouveau défaut 1.2.0 |",
        "| :-- | --: | --: |",
    ]
    for condition, values in summary.items():
        lines.append(
            f"| {condition} | {values['previous_wer'] * 100:.2f} % | {values['new_defaults']['wer'] * 100:.2f} % |"
        )
    lines += [
        "",
        "Les mots reconnus sont conservés dans les 2 028 cas. Le gain lexical vient de l’arrêt des conversions automatiques, pas d’une amélioration du modèle acoustique. Les conversions restent disponibles sur demande et le dictionnaire personnel reste actif.",
        "",
        "La case « Dictées courtes sans ponctuation » est indépendante. Elle ne modifie pas ces scores, puisque cette normalisation ignore la ponctuation. Le seuil historique est strictement inférieur à cinq mots.",
        "",
        f"[Métadonnées et intervalles]({output.name}) · [Détail par extrait]({output.with_suffix('.csv').name}) · [Campagne d’origine]({source.with_suffix('.md').name}) · [Sources et décisions](../../docs/RECHERCHE-WER-1.2.0.md)",
        "",
        "Les bruits sont des ajouts numériques et les microphones/locuteurs uniques ne sont pas documentés. Les essais terrain restent à collecter. Références FLEURS : Google et contributeurs, [CC BY 4.0](https://huggingface.co/datasets/google/fleurs).",
        "",
    ]
    output.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    checksums = []
    for suffix in (".json", ".csv", ".md"):
        item = output.with_suffix(suffix)
        checksums.append(f"{hashlib.sha256(item.read_bytes()).hexdigest()}  {item.name}")
    output.with_suffix(".sha256").write_text("\n".join(checksums) + "\n", encoding="ascii")
    print(output)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    replay(options.source, options.output)
