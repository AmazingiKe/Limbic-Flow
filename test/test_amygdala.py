"""
杏仁核单元测试：process 对 state 的神经递质与半衰期基线。
"""
import os
import tempfile
import pytest
from limbic_flow.core.types import CognitiveState
from limbic_flow.core.amygdala import Amygdala, _apply_half_life_decay


@pytest.fixture
def amygdala_memory():
    """使用临时数据库文件（:memory: 每连接独立，表不可见）。"""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        yield Amygdala(db_path=path)
    finally:
        try:
            os.unlink(path)
        except Exception:
            pass


@pytest.fixture
def state_positive():
    s = CognitiveState(user_input="hello 开心")
    s.pad_vector["pleasure"] = 0.5
    s.pad_vector["arousal"] = 0.2
    s.pad_vector["dominance"] = 0.3
    return s


@pytest.fixture
def state_anxious():
    s = CognitiveState(user_input="help")
    s.pad_vector["pleasure"] = -0.3
    s.pad_vector["arousal"] = 0.5
    s.pad_vector["dominance"] = -0.3
    return s


def test_apply_half_life_decay_zero_time():
    record = {"pleasure": 0.5, "arousal": 0.2, "dominance": 0.0, "dopamine": 0.7, "cortisol": 0.4}
    out = _apply_half_life_decay(record, 0.0)
    assert out["pleasure"] == 0.5
    assert out["dopamine"] == 0.7
    assert out["cortisol"] == 0.4


def test_apply_half_life_decay_positive_time():
    record = {"pleasure": 0.5, "arousal": 0.2, "dominance": 0.0, "dopamine": 0.7, "cortisol": 0.4}
    out = _apply_half_life_decay(record, 3600)
    assert out["pleasure"] < 0.5
    assert 0 <= out["dopamine"] <= 1
    assert 0 <= out["cortisol"] <= 1


def test_amygdala_process_updates_neurotransmitters(amygdala_memory, state_positive):
    out = amygdala_memory.process(state_positive)
    assert "dopamine" in out.neurotransmitters
    assert "cortisol" in out.neurotransmitters
    assert 0 <= out.neurotransmitters["dopamine"] <= 1
    assert 0 <= out.neurotransmitters["cortisol"] <= 1
    assert out.neurotransmitters["dopamine"] >= 0.5


def test_amygdala_process_high_stress_raises_cortisol(amygdala_memory, state_anxious):
    out = amygdala_memory.process(state_anxious)
    assert out.neurotransmitters["cortisol"] >= 0.3


def test_amygdala_process_idempotent_state_fields(amygdala_memory, state_positive):
    out = amygdala_memory.process(state_positive)
    assert out.user_input == state_positive.user_input
    assert out.pad_vector["pleasure"] == state_positive.pad_vector["pleasure"]
