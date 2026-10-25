from doctype.domain import Document, LabelSource


def _decide(w, text, group, probs):
    doc = Document("d", "t1", text, group)
    return w.store.record_decision(doc=doc, input_uri=w.texts.put("t1", text), model_version="m",
                                   probabilities=probs, threshold=0.85)


def test_route_follows_threshold(wired):
    assert _decide(wired, "a", "g1", {"sov": 0.9, "other": 0.1}).route == "auto"
    assert _decide(wired, "b", "g1", {"sov": 0.6, "other": 0.4}).route == "fallback"


def test_human_beats_lower_tiers(wired):
    d = _decide(wired, "x", "g1", {"sov": 0.6, "other": 0.4})
    wired.store.add_label(d.decision_id, "sov", LabelSource.LLM_FALLBACK, "llm")
    wired.store.add_label(d.decision_id, "loss_run", LabelSource.HUMAN, "ops")
    assert wired.store.resolve(d.decision_id, LabelSource.LLM_FALLBACK).doc_type == "loss_run"


def test_disagreement_below_human_is_unresolved(wired):
    d = _decide(wired, "x", "g1", {"sov": 0.6, "other": 0.4})
    wired.store.add_label(d.decision_id, "sov", LabelSource.DOWNSTREAM, "e1")
    wired.store.add_label(d.decision_id, "acord", LabelSource.DOWNSTREAM, "e2")
    assert wired.store.resolve(d.decision_id, LabelSource.LLM_FALLBACK) is None


def test_snapshot_excludes_golden_hash_and_template(wired):
    golden_text = "Statement of values: 14 locations, total TIV 82.4m"
    a = _decide(wired, golden_text, "prod-group", {"sov": 0.9, "other": 0.1})
    b = _decide(wired, "Statement of values 99 locations", "g-sov", {"sov": 0.9, "other": 0.1})
    c = _decide(wired, "Schedule of values 3 locations TIV 4m", "aon", {"sov": 0.9, "other": 0.1})
    for d in (a, b, c):
        wired.store.add_label(d.decision_id, "sov", LabelSource.HUMAN, "ops")
    snap = wired.snapshots.read(wired.store.build_snapshot("t1"))
    assert [e.decision_id for e in snap.examples] == [c.decision_id]
    assert (snap.excluded_golden, snap.excluded_template) == (1, 1)


def test_trust_floor_counts_below_floor_not_conflict(wired):
    d = _decide(wired, "Loss history 5 yr", "g9", {"loss_run": 0.6, "other": 0.4})
    wired.store.add_label(d.decision_id, "loss_run", LabelSource.LLM_FALLBACK, "llm")
    snap = wired.snapshots.read(wired.store.build_snapshot("t1", LabelSource.DOWNSTREAM))
    assert not snap.examples
    assert (snap.excluded_below_floor, snap.excluded_conflict) == (1, 0)
