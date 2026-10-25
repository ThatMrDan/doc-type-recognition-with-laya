import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "golden"))

from checks import components, discriminator  # noqa: E402
from common import banned_hits, char_shingles, jaccard  # noqa: E402
from noise import ocr, past_window, uk_format  # noqa: E402


def test_training_names_match_whole_words_only():
    assert banned_hits("From: Max at Northgate Brokers") == ["max", "northgate"]
    assert banned_hits("Maxwell Tompkins, Leeds") == []


def test_similarity_ignores_digits_and_case():
    a = char_shingles("Schedule of values 22 locations TIV 140m")
    b = char_shingles("SCHEDULE OF VALUES 31 locations TIV 990m")
    assert jaccard(a, b) == 1.0
    assert jaccard(a, char_shingles("Loss run five years incurred")) < 0.2


def test_near_duplicates_share_a_component_but_parent_links_do_not_count():
    rows = [{"id": "a", "text": "Statement of values for nine warehouses in Leeds", "parent_id": None},
            {"id": "b", "text": "Statement of values for nine warehouses in Hull", "parent_id": None},
            {"id": "d", "text": "Premium invoice due in thirty days", "parent_id": None}]
    comp = components(rows)
    assert comp["a"] == comp["b"]
    assert comp["d"] != comp["a"]
    # a contrast or noise child is not merged with its own parent just for resembling it
    pair = components([rows[0], {"id": "c", "text": rows[0]["text"] + "!", "parent_id": "a"}])
    assert pair["c"] != pair["a"]


def test_noise_ops_are_seeded_and_grow_past_the_window():
    text = "Loc 1 | 12 Dock Road | Warehouse | 1,200,000 ; Loc 2 | 3 Mill Lane | Office | 800,000 ; Total 2,000,000"
    assert ocr(text, random.Random(1)) == ocr(text, random.Random(1))
    assert len(past_window(text, random.Random(2)).split()) >= 900
    assert uk_format("Loss date 03/14/2024, paid $1,200", random.Random(3)) == "Loss date 14/03/2024, paid £1,200"


def test_discriminator_is_near_chance_on_one_distribution():
    same = [f"loss run {i} years incurred {i * 7}k claims {i}" for i in range(40)]
    assert discriminator(same[::2], same[1::2]) < 0.75
