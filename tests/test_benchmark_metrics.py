"""Metric regression cases: failures, weighting, French normalization, uncertainty."""

import pytest
from scripts.benchmark_metrics import aggregate, bootstrap_wer, score, tokens


def test_french_normalization_keeps_accents_and_numeric_distinctions():
    assert tokens("L’ÉCOLE, c'est 25 !") == ["l", "école", "c", "est", "25"]
    assert score("école", "ecole")["wer"] == 1
    assert score("vingt cinq", "25")["wer"] == 1
    assert score("cafe\u0301", "café")["wer"] == 0


def test_substitution_deletion_and_insertion_are_counted():
    assert score("un deux trois", "un quatre trois")["substitutions"] == 1
    assert score("un deux trois", "un trois")["deletions"] == 1
    assert score("un deux trois", "un deux quatre trois")["insertions"] == 1
    assert score("oui oui", "oui")["deletions"] == 1


def test_empty_hypothesis_counts_every_missing_word():
    result = score("bonjour à tous", "")
    assert result["wer"] == 1 and result["deletions"] == 3


def test_corpus_wer_is_weighted_by_reference_words_not_utterances():
    result = aggregate(
        [
            score("un", "autre"),
            score(
                "un deux trois quatre cinq six sept huit neuf", "un deux trois quatre cinq six sept huit neuf"
            ),
        ]
    )
    assert result["wer"] == 0.1  # An incorrect mean of utterance WERs would be .5.
    assert result["reference_words"] == 10 and result["word_errors"] == 1


def test_empty_reference_is_not_a_zero_error_claim():
    assert score("", "hallucination")["wer"] is None
    assert score("", "hallucination")["insertions"] == 1
    assert aggregate([])["wer"] is None


def test_bootstrap_is_reproducible_and_discloses_unknown_speakers():
    cases = [dict(score("un deux", "un"), speaker_id=None), score("trois", "trois")]
    first = bootstrap_wer(cases, repetitions=100)
    assert first == bootstrap_wer(cases, repetitions=100)
    assert first["resampling_unit"] == "recording"
    assert first["low"] <= aggregate(cases)["wer"] <= first["high"]
    known = [dict(case, speaker_id="same-person") for case in cases]
    assert bootstrap_wer(known, repetitions=100)["units"] == 1
    assert bootstrap_wer(known, repetitions=100)["resampling_unit"] == "speaker"
    with pytest.raises(ValueError):
        bootstrap_wer([])
