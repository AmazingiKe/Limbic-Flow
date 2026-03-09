"""
大脑/新皮层 - 负责高级认知、内省与文本生成

[职责] 接收扭曲后的记忆，生成最终回复内容
[可替换性] 可替换为不同的大模型或认知架构
"""

from typing import Optional
from limbic_flow.core.types import CognitiveState
from limbic_flow.core.ai.factory import LLMFactory
from limbic_flow.core.location import LocationDetector
from limbic_flow.core.brain.prompt_builder import PromptBuilder
from limbic_flow.utils.logger import get_logger


class Brain:
    """
    大脑/新皮层 - 负责高级认知与文本生成
    
    [比喻] 就像人的大脑皮层:
    - 整合各种信息（记忆、情绪、上下文）
    - 生成合适的回应
    - 根据情绪调整表达方式
    
    [设计]
    - 使用 PromptBuilder 分离提示词构建逻辑，便于测试
    - 依赖 LLMFactory 创建不同提供商
    - 依赖 LocationDetector 获取位置信息
    """
    
    def __init__(self, llm_provider: Optional[str] = None):
        self.logger = get_logger("Brain")
        self.llm_factory = LLMFactory()
        self.llm = self.llm_factory.create_llm(llm_provider)
        self.location_detector = LocationDetector()
        self.user_location = self.location_detector.detect_location()
        self.prompt_builder = PromptBuilder()
        
        self.logger.info(f"大脑初始化完成，使用 LLM 提供商: {llm_provider or '默认'}")

    def process(self, state: CognitiveState) -> CognitiveState:
        """
        处理认知状态，生成回复
        
        [流程]
        1. 构建系统提示词（包含情绪风格指南）
        2. 构建用户提示词（包含记忆和上下文）
        3. 调用 LLM 生成内容
        4. 失败时使用回退响应
        """
        # 1. 构建提示词
        system_prompt = self.prompt_builder.build_system_prompt(
            state, 
            self.location_detector.get_location_summary(self.user_location)
        )
        user_prompt = self.prompt_builder.build_user_prompt(state)
        
        # 2. 调用 LLM
        try:
            response = self.llm.chat_simple(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.8
            )
            state.final_response_text = response.content
            state.content = response.content
        except Exception as e:
            self.logger.error(f"LLM 调用失败: {e}", exc_info=True)
            state.final_response_text = self.prompt_builder.get_fallback_response(state)
            state.content = state.final_response_text
        
        return state
    
    def update_location(self) -> None:
        """更新位置信息"""
        self.user_location = self.location_detector.detect_location()
