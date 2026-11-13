"""Publish-readable tables and per-recording CSV from a completed measurement."""

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path


def percentage(value):
    return f"{100 * value:.2f} %" if value is not None else "n/a"


def summarize(path):
    path = Path(path)
    report = json.loads(path.read_text(encoding="utf-8"))
    if not report.get("run_completed") or len(report["cases"]) != report["expected_evaluations"]:
        raise ValueError("Refusing to publish a completed-campaign summary from a partial run")
    unique = {case["id"]: case for case in report["cases"]}
    minutes = sum(case["audio_seconds"] for case in unique.values()) / 60
    reference_words = sum(case["metrics"]["reference_words"] for case in unique.values())
    sentences = len({case["source_sentence_id"] for case in unique.values()})
    names = {
        "clean": "Audio d’origine",
        "white20": "Bruit blanc ajouté · 20 dB SNR",
        "white10": "Bruit blanc ajouté · 10 dB SNR",
    }
    lines = [
        "# Voxcalibur — mesure sur le split de test FLEURS français",
        "",
        f"**{len(unique)} enregistrements humains · {sentences} phrases distinctes · {minutes:.1f} minutes uniques · {reference_words:,} mots de référence.**",
        "",
        f"{len(report['cases'])} transcriptions, sur {len(report['conditions'])} variantes des mêmes enregistrements. "
        "Le split de test épinglé est évalué en entier."
        if report["is_full_split"]
        else "**Sous-ensemble : cette mesure ne couvre pas le split complet.**",
        "",
        "## Résultats",
        "",
        "Le WER est un taux d’erreur : plus il est bas, mieux c’est. Il est pondéré par les mots de référence, pas moyenné par phrase.",
        "",
        "| Condition | Extraits | WER après corrections | IC 95 % par enregistrement | WER ASR brut | CER après corrections | RTF | Hypothèses vides |",
        "| :-- | --: | --: | :-- | --: | --: | --: | --: |",
    ]
    for condition in report["conditions"]:
        result = report["summary"][condition]
        ci = result["wer_95ci"]
        lines.append(
            f"| {names[condition]} | {result['recordings']} | {percentage(result['wer'])} | "
            f"[{percentage(ci['low'])} ; {percentage(ci['high'])}] | {percentage(result['raw_asr']['wer'])} | "
            f"{percentage(result['cer'])} | {result['real_time_factor']:.3f} | {result['empty_hypotheses']} |"
        )
    clean = [case for case in report["cases"] if case["condition"] == "clean"]
    if clean:
        worse = sum(case["metrics"]["word_errors"] > case["raw_metrics"]["word_errors"] for case in clean)
        better = sum(case["metrics"]["word_errors"] < case["raw_metrics"]["word_errors"] for case in clean)
        delta = sum(case["metrics"]["word_errors"] - case["raw_metrics"]["word_errors"] for case in clean)
        lines += [
            "",
            "## Effet des corrections françaises",
            "",
            f"Sur l’audio d’origine, le nombre d’erreurs lexicales augmente pour {worse} enregistrements et diminue pour {better}, avec un solde de {delta:+d} erreurs. Les deux séries de scores sont conservées.",
            "",
            "L’écart comprend des différences de représentation : par exemple, dans `fleurs-fr-test-00004`, le moteur écrit « dix-sept » et le réglage par défaut le convertit en « 17 ». La référence conserve les lettres. La normalisation annoncée préserve cette différence et la compte comme erreur lexicale, même si la quantité est la même. Les scores n’ont pas été recalculés avec une normalisation plus favorable après observation des résultats.",
            "",
        ]
    labels = Counter(case.get("gender_label", "unknown") for case in unique.values())
    hardware = report["environment"]
    gpus = ", ".join(gpu["name"] for gpu in hardware["gpus"])
    lines += [
        "",
        "## Portée exacte",
        "",
        "- FLEURS est de la parole lue publique. La représentativité de la dictée spontanée n’est pas établie.",
        "- **Le nombre d’enregistrements n’est pas le nombre de personnes.** Les identifiants de locuteur ne sont pas fournis ; le nombre de voix uniques est inconnu.",
        "- Les modèles de microphones et les environnements d’origine sont inconnus. Aucune diversité de microphones physiques n’est démontrée ici.",
        "- Le bruit blanc est ajouté numériquement. Il ne représente pas une collecte réelle en café, bureau ou pièce réverbérante.",
        "- Les intervalles bootstrap portent sur les enregistrements et ne sont pas des intervalles de généralisation à de nouveaux locuteurs. Des phrases se répètent dans le corpus.",
        "- Le chevauchement éventuel entre ce corpus public et l’entraînement du modèle n’est pas établi.",
        f"- Étiquettes fournies par le corpus : {dict(labels)}. Elles ne constituent pas un recensement des personnes enregistrées.",
        "",
        "Les [essais terrain multi-microphones et en bruit réel](../PROTOCOL.md) restent **à collecter**. Aucun objectif de qualité métier n’a été déclaré atteint sur cette base.",
        "",
        "## Configuration gelée",
        "",
        f"- Application : Voxcalibur {report['application_version']} ; [code mesuré](https://github.com/jossmair/Voxcalibur/tree/{report['source_commit']}).",
        f"- Backend effectif : `{report['backend']}` ; GPU détecté : {gpus}.",
        f"- CPU : {hardware['cpu']} ; {hardware['cores']} cœurs physiques ; RAM : {hardware['ram_gib']} Gio.",
        f"- Python {hardware['python']} ; NumPy {hardware['numpy']} ; soxr {hardware['soxr']}.",
        f"- Runtime : `{report['runtime_filename']}` ; SHA-256 `{report['runtime_sha256']}`.",
        f"- Modèle : SHA-256 `{report['model_sha256']}`.",
        "- Dictionnaire vide, français, nombres en chiffres, unités abrégées, segmentation et VAD par défaut.",
        f"- Graine du bruit et du bootstrap : `{report['seed']}`. Le SNR est calculé sur l’enregistrement entier, pauses comprises. Un gain commun limite les pics du mélange à 0,999.",
        "",
        "## Méthode et fichiers",
        "",
        f"Normalisation WER : {report['normalization']}. La casse et la ponctuation ne sont pas notées. Les accents et les différences chiffres/lettres sont conservés. Les scores ne sont pas directement comparables à ceux d’une autre normalisation.",
        "",
        "Le CER s’applique aux mots normalisés joints par des espaces simples. Une hypothèse vide contribue autant de suppressions qu’il y a de mots de référence. Le RTF couvre l’ingestion audio et le moteur en traitement hors temps réel, divisés par la durée audio. Chargement initial, préparation, corrections textuelles, scores et collage sont exclus ; ce n’est pas une mesure de la latence après arrêt au microphone.",
        "",
        f"[Rapport JSON complet]({path.name}) · [Détail CSV]({path.with_suffix('.csv').name}) · [Reproduire](../README.md) · [Corpus épinglé](../corpora/fleurs-fr-test.json)",
        "",
        "Attribution : Google et contributeurs, FLEURS — Few-shot Learning Evaluation of Universal Representations of Speech. [Source officielle](https://huggingface.co/datasets/google/fleurs), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Conversion PCM16, bruit synthétique et normalisation documentés ; les fichiers audio ne sont pas redistribués.",
        "",
    ]
    path.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    fields = [
        "id",
        "condition",
        "reference",
        "hypothesis",
        "raw_hypothesis",
        "reference_words",
        "word_errors",
        "substitutions",
        "deletions",
        "insertions",
        "wer",
        "cer",
        "raw_wer",
        "audio_seconds",
        "inference_seconds",
        "speaker_id",
        "source_sentence_id",
        "gender_label",
        "microphone",
        "environment",
        "audio_sha256",
        "processed_audio_sha256",
        "dataset",
        "dataset_revision",
        "source_license",
    ]
    with path.with_suffix(".csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for case in report["cases"]:
            row = {field: case.get(field) for field in fields}
            row.update(
                {
                    key: case["metrics"][key]
                    for key in (
                        "reference_words",
                        "word_errors",
                        "substitutions",
                        "deletions",
                        "insertions",
                        "wer",
                        "cer",
                    )
                }
            )
            row.update(
                raw_wer=case["raw_metrics"]["wer"],
                dataset=report["provenance"]["dataset"],
                dataset_revision=report["provenance"]["revision"],
                source_license=report["provenance"]["license"],
            )
            writer.writerow(row)
    checksums = []
    for suffix in (".json", ".csv", ".md"):
        item = path.with_suffix(suffix)
        checksums.append(f"{hashlib.sha256(item.read_bytes()).hexdigest()}  {item.name}")
    path.with_suffix(".sha256").write_text("\n".join(checksums) + "\n", encoding="ascii")
    return path.with_suffix(".md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    print(summarize(parser.parse_args().report))
