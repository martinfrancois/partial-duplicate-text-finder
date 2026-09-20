from pathlib import Path

import pytest

from finder import calculate_similarity, find_partial_duplicates

EXAMPLES = Path(__file__).parent / "examples"


def read(name):
    return (EXAMPLES / name).read_text(encoding="utf-8")


def test_identical_files_have_ratio_one():
    assert calculate_similarity(read("garden-notice.txt"), read("garden-notice-copy.txt")) == 1.0


def test_revised_notice_is_a_partial_duplicate():
    ratio = calculate_similarity(read("garden-notice.txt"), read("garden-notice-revised.txt"))
    assert ratio == pytest.approx(0.9213, abs=0.0005)


def test_unrelated_text_is_far_below_threshold():
    ratio = calculate_similarity(read("garden-notice.txt"), read("soup-recipe.txt"))
    assert ratio < 0.1


def test_example_folder_at_default_threshold():
    assert find_partial_duplicates(str(EXAMPLES), 0.8) == {
        "garden-notice-copy.txt": ["garden-notice-revised.txt", "garden-notice.txt"],
        "garden-notice-revised.txt": ["garden-notice.txt"],
    }


def test_high_threshold_keeps_only_the_exact_copy():
    assert find_partial_duplicates(str(EXAMPLES), 0.99) == {
        "garden-notice-copy.txt": ["garden-notice.txt"],
    }


def test_folder_without_duplicates_returns_empty_dict(tmp_path):
    (tmp_path / "a.txt").write_text(read("garden-notice.txt"), encoding="utf-8")
    (tmp_path / "b.txt").write_text(read("soup-recipe.txt"), encoding="utf-8")
    assert find_partial_duplicates(str(tmp_path), 0.8) == {}
