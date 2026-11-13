import json

import pytest

from scripts.summarize_benchmark import summarize


def test_partial_measurement_cannot_be_published_as_a_complete_campaign(tmp_path):
    report = tmp_path / "partial.json"
    report.write_text(json.dumps({"run_completed": False, "cases": [], "expected_evaluations": 2028}))
    with pytest.raises(ValueError, match="partial"):
        summarize(report)
    assert not report.with_suffix(".md").exists()
    assert not report.with_suffix(".csv").exists()
