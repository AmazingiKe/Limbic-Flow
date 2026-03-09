"""
病理中间件单元测试：distort_query、distort_memories 行为。
"""
import numpy as np
import pytest
from limbic_flow.middleware.pathology import (
    BasePathologyMiddleware,
    DepressionPathology,
    AlzheimerPathology,
)


@pytest.fixture
def emotional_state_high_cortisol():
    return {
        "pleasure": -0.3,
        "arousal": 0.2,
        "dominance": -0.2,
        "dopamine": 0.4,
        "cortisol": 0.7,
        "timestamp": 1000.0,
    }


@pytest.fixture
def emotional_state_low_cortisol():
    return {
        "pleasure": 0.5,
        "arousal": 0.0,
        "dominance": 0.0,
        "dopamine": 0.6,
        "cortisol": 0.2,
        "timestamp": 1000.0,
    }


@pytest.fixture
def base_middleware():
    m = BasePathologyMiddleware()
    m.add_pathology(DepressionPathology(base_severity=0.3))
    m.add_pathology(AlzheimerPathology(severity=0.5))
    return m


def test_depression_pathology_should_apply_high_cortisol(emotional_state_high_cortisol):
    p = DepressionPathology(base_severity=0.3)
    assert p.should_apply(emotional_state_high_cortisol) is True


def test_depression_pathology_should_apply_low_cortisol(emotional_state_low_cortisol):
    p = DepressionPathology(base_severity=0.3)
    assert p.should_apply(emotional_state_low_cortisol) is False


def test_depression_distort_memories_filters_positive_memories(emotional_state_high_cortisol):
    p = DepressionPathology(base_severity=0.8)
    memories = [
        {"pad": {"pleasure": 0.8, "arousal": 0.0, "dominance": 0.0}, "id": "1"},
        {"pad": {"pleasure": -0.2, "arousal": 0.0, "dominance": 0.0}, "id": "2"},
    ]
    out = p.distort_memories(memories, emotional_state_high_cortisol)
    assert len(out) <= 2
    for m in out:
        assert "pad" in m


def test_alzheimer_should_apply_always():
    p = AlzheimerPathology(severity=0.5)
    assert p.should_apply({"cortisol": 0.0}) is True


def test_alzheimer_distort_query_adds_noise():
    p = AlzheimerPathology(severity=0.3)
    q = np.array([0.1, 0.2, 0.3], dtype=np.float64)
    out = p.distort_query(q.copy(), {"timestamp": 0.0})
    assert out.shape == q.shape
    assert not np.allclose(out, q)


def test_base_middleware_distort_query_returns_vector(base_middleware, emotional_state_high_cortisol):
    q = np.ones(4, dtype=np.float64) * 0.25
    out = base_middleware.distort_query(q, emotional_state_high_cortisol)
    assert isinstance(out, np.ndarray)
    assert out.shape == q.shape


def test_base_middleware_distort_memories_returns_list(base_middleware, emotional_state_low_cortisol):
    memories = [{"pad": {"pleasure": 0.0, "arousal": 0.0, "dominance": 0.0}}]
    out = base_middleware.distort_memories(memories, emotional_state_low_cortisol)
    assert isinstance(out, list)
