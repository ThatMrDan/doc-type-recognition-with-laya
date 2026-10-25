from doctype.adapters.fallback import parse_doc_type
from doctype.adapters.laya_model import _to_distribution
from doctype.domain import DOC_TYPES, Document, LabelSource
from doctype.services import fit_temperature, tune_threshold


def test_low_confidence_goes_to_fallback_and_is_labelled(wired):
    out = wired.intake.process(Document("1", "t1", "ACORD 125 application commercial", "acord-125"))
    assert out.decision.route == "fallback"
    assert out.final_type == "acord"
    labels = wired.store.human_labelled("t1")
    assert labels == []  # fallback labels are not human labels


def test_schema_failure_produces_downstream_label(wired):
    # Confident "sov" from keywords, but the text is really a loss run with no TIV or locations
    out = wired.intake.process(Document("2", "t1", "Schedule of values tiv tiv loss summary 5 years incurred 2m", "x"))
    assert out.decision.route == "auto" and out.decision.predicted == "sov"
    assert out.final_type == "loss_run"
    label = wired.store.resolve(out.decision.decision_id, LabelSource.LLM_FALLBACK)
    assert label.source == LabelSource.DOWNSTREAM and label.doc_type == "loss_run"


def test_training_improves_coverage_and_promotes(wired):
    for i, text in enumerate(["Statement of exposures 11 premises, 11 locations, TIV 51m",
                              "Premises list and statement of exposures, 4 locations, TIV 9m",
                              "Statement of exposures 8 premises, 8 locations, TIV 33m"]):
        wired.intake.process(Document(str(i), "t1", text, f"broker-{i}"))
    result = wired.pipeline.run("t1", "sim-v2", 0.85)
    assert result.candidate is not None
    assert result.promoted
    assert wired.models.current().version == "sim-v2"


def test_threshold_and_temperature_from_audit_sample(wired):
    decisions = []
    for i in range(10):
        d = wired.store.record_decision(doc=Document(str(i), "t1", f"doc {i}", "g"), input_uri="u",
                                        model_version="m", probabilities={"sov": 0.95, "other": 0.05},
                                        threshold=0.85)
        decisions.append((d, "sov" if i < 9 else "other"))
    assert tune_threshold(decisions, max_auto_error=0.15) == 0.6
    assert fit_temperature(decisions) > 0


def test_laya_answer_shapes():
    as_dict = _to_distribution({"choice": "sov", "probabilities": {"sov": 0.7, "loss_run": 0.3}})
    as_list = _to_distribution({"choice": "sov", "probabilities": [0.6, 0.1, 0.1, 0.1, 0.1]})
    as_conf = _to_distribution({"choice": "acord", "answer_confidence": 0.8})
    for dist in (as_dict, as_list, as_conf):
        assert set(dist) == set(DOC_TYPES) and abs(sum(dist.values()) - 1) < 1e-9
    assert max(as_conf, key=as_conf.get) == "acord"


def test_export_rows_match_laya_gold_schema(wired, tmp_path):
    import json
    from doctype.adapters.laya_trainer import export_snapshot
    wired.intake.process(Document("1", "t1", "ACORD 125 application commercial", "acord-125"))
    snap = wired.snapshots.read(wired.store.build_snapshot("t1"))
    row = json.loads(export_snapshot(snap, wired.texts, tmp_path / "train.jsonl").read_text().splitlines()[0])
    assert set(row) >= {"state", "questions", "gold"}
    probs = row["gold"]["doc_type"]["probabilities"]
    assert set(probs) == set(row["questions"]["doc_type"]["criteria"])
    assert abs(sum(probs.values()) - 1) < 1e-9 and max(probs, key=probs.get) == "acord"
    assert probs["acord"] == 0.4  # LLM label, soft target


def test_fallback_parser_degrades_to_other():
    assert parse_doc_type('{"doc_type": "sov"}') == "sov"
    assert parse_doc_type('Sure! {"doc_type": "loss_run"} done') == "loss_run"
    assert parse_doc_type('{"doc_type": "invoice"}') == "other"
    assert parse_doc_type("no json") == "other"
