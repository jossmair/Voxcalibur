"""Auditable, corpus-weighted speech metrics; no model or Windows dependency."""

import random
import re
import unicodedata


NORMALIZATION = "NFC, Unicode casefold, Unicode word tokens; accents and digits preserved"


def tokens(text):
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).casefold())


def edit_counts(reference, hypothesis):
    """Levenshtein S/D/I counts; ties prefer substitution, deletion, insertion."""
    row = [(j, 0, 0, j) for j in range(len(hypothesis) + 1)]
    for i, expected in enumerate(reference, 1):
        current = [(i, 0, i, 0)]
        for j, actual in enumerate(hypothesis, 1):
            cost, sub, delete, insert = row[j - 1]
            diagonal = (
                (cost, sub, delete, insert) if expected == actual else (cost + 1, sub + 1, delete, insert)
            )
            cost, sub, delete, insert = row[j]
            deletion = (cost + 1, sub, delete + 1, insert)
            cost, sub, delete, insert = current[-1]
            insertion = (cost + 1, sub, delete, insert + 1)
            current.append(min((diagonal, deletion, insertion), key=lambda item: item[0]))
        row = current
    errors, substitutions, deletions, insertions = row[-1]
    return dict(errors=errors, substitutions=substitutions, deletions=deletions, insertions=insertions)


def score(reference, hypothesis):
    expected, actual = tokens(reference), tokens(hypothesis)
    words = edit_counts(expected, actual)
    reference_chars = " ".join(expected)
    chars = edit_counts(reference_chars, " ".join(actual))
    return {
        "reference_words": len(expected),
        "word_errors": words["errors"],
        "substitutions": words["substitutions"],
        "deletions": words["deletions"],
        "insertions": words["insertions"],
        "wer": words["errors"] / len(expected) if expected else None,
        "reference_chars": len(reference_chars),
        "char_errors": chars["errors"],
        "cer": chars["errors"] / len(reference_chars) if reference_chars else None,
    }


def aggregate(cases):
    words = sum(case["reference_words"] for case in cases)
    chars = sum(case["reference_chars"] for case in cases)
    errors = sum(case["word_errors"] for case in cases)
    char_errors = sum(case["char_errors"] for case in cases)
    return {
        "recordings": len(cases),
        "reference_words": words,
        "word_errors": errors,
        "substitutions": sum(case["substitutions"] for case in cases),
        "deletions": sum(case["deletions"] for case in cases),
        "insertions": sum(case["insertions"] for case in cases),
        "wer": errors / words if words else None,
        "reference_chars": chars,
        "char_errors": char_errors,
        "cer": char_errors / chars if chars else None,
    }


def bootstrap_wer(cases, seed=20261113, repetitions=2000):
    """Percentile interval; speaker clusters only when every speaker ID is known."""
    if not cases:
        raise ValueError("Cannot bootstrap an empty evaluation")
    known_speakers = all(case.get("speaker_id") for case in cases)
    groups = {}
    for i, case in enumerate(cases):
        key = case["speaker_id"] if known_speakers else i
        errors, words = groups.get(key, (0, 0))
        groups[key] = errors + case["word_errors"], words + case["reference_words"]
    groups = list(groups.values())
    rng = random.Random(seed)
    values = []
    for _ in range(repetitions):
        selected = [rng.choice(groups) for _ in groups]
        words = sum(item[1] for item in selected)
        if words:
            values.append(sum(item[0] for item in selected) / words)
    if not values:
        raise ValueError("No reference words in bootstrap evaluation")
    values.sort()
    return {
        "low": values[int(0.025 * (len(values) - 1))],
        "high": values[int(0.975 * (len(values) - 1))],
        "confidence": 0.95,
        "repetitions": repetitions,
        "seed": seed,
        "resampling_unit": "speaker" if known_speakers else "recording",
        "units": len(groups),
    }
