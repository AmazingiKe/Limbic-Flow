"""
Pipeline 单轮流程测试：Mock LLM + Mock 海马体，验证动作流输出。
需安装项目依赖后运行（如 sentence_transformers）。
"""
import os
import tempfile
import pytest
from limbic_flow.pipeline import LimbicFlowPipeline
from limbic_flow.core.hippocampus import MockHippocampus
from limbic_flow.core.amygdala import Amygdala
from limbic_flow.core.articulation.action_event import ActionType


@pytest.fixture
def pipeline_mock():
    """使用 Mock 海马体与临时文件杏仁核（:memory: 每连接独立，表不可见）。"""
    hippocampus = MockHippocampus()
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    amygdala = Amygdala(db_path=db_path)
    try:
        yield LimbicFlowPipeline(
            llm_provider="mock",
            hippocampus=hippocampus,
            amygdala=amygdala,
        )
    finally:
        try:
            os.unlink(db_path)
        except Exception:
            pass


def test_pipeline_process_input_yields_actions(pipeline_mock):
    actions = list(pipeline_mock.process_input("你好", context=None))
    assert isinstance(actions, list)
    assert len(actions) >= 0
    for a in actions:
        assert hasattr(a, "action_type")
        assert hasattr(a, "to_dict")
        assert a.action_type in (ActionType.typing, ActionType.message, ActionType.wait)


def test_pipeline_process_input_at_least_one_message_action(pipeline_mock):
    actions = list(pipeline_mock.process_input("hello", context=None))
    message_actions = [a for a in actions if a.action_type == ActionType.message]
    assert len(message_actions) >= 1
    assert any(getattr(a, "content", None) for a in message_actions)


def test_pipeline_process_input_alias_process_input_stream(pipeline_mock):
    out1 = list(pipeline_mock.process_input("hi"))
    out2 = list(pipeline_mock.process_input_stream("hi"))
    assert isinstance(out1, list)
    assert isinstance(out2, list)
