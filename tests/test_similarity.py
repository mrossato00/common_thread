from similarity import jaccard


def test_identical_sets():
    assert jaccard({"a", "b"}, {"a", "b"}) == 1.0


def test_disjoint_sets():
    assert jaccard({"a"}, {"b"}) == 0.0


def test_partial_overlap():
    assert jaccard({"a", "b", "c"}, {"b", "c", "d"}) == 0.5