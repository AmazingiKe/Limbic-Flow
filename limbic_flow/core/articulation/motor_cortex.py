"""
运动皮层核心类 (Motor Cortex)
"""

import re
import random
from typing import List, Dict, Any, Optional
from .action_event import ActionEvent, ActionType
from limbic_flow.core.types import CognitiveState


class MotorCortex:
    """
    [职责] 运动皮层 - 将文本转化为带有时序的动作流
    [场景] Pipeline 末端，负责最终输出
    [可替换性] 可替换为不同的表达风格引擎
    """
    
    def __init__(
        self,
        base_wpm: int = 60,
        min_segment_length: int = 10,
        max_segment_length: int = 50,
        hesitation_base: float = 0.5,
        hesitation_multiplier: float = 1.5
    ):
        """
        初始化运动皮层
        """
        self.base_wpm = base_wpm
        self.min_segment_length = min_segment_length
        self.max_segment_length = max_segment_length
        self.hesitation_base = hesitation_base
        self.hesitation_multiplier = hesitation_multiplier
        
        # 标点符号集合（用于分段）
        self.sentence_endings = "。！？...？"
        self.clause_separators = "，、；："

    def process(self, state: CognitiveState) -> CognitiveState:
        """
        [职责] 处理认知状态，生成动作流
        [场景] Pipeline 调度调用
        """
        # 构建 PAD 状态字典供内部方法使用
        pad_state = {
            "pleasure": state.pad_vector['pleasure'],
            "arousal": state.pad_vector['arousal'],
            "dominance": state.pad_vector['dominance'],
            "dopamine": state.neurotransmitters['dopamine'],
            "cortisol": state.neurotransmitters['cortisol']
        }
        
        # 生成动作流
        actions = self.articulate(state.final_response_text, pad_state)
        
        # 更新状态
        state.action_queue = actions
        return state

    
    def _calculate_typing_delay(self, text_length: int, pad_state: Dict[str, float]) -> float:
        """
        根据文本长度和情绪状态计算打字耗时
        """
        arousal = pad_state.get("arousal", 0.0)
        dopamine = pad_state.get("dopamine", 0.0)

        # 计算速度修正因子
        speed_modifier = 1.0 + (arousal * 0.5)
        
        # 多巴胺 (Dopamine) 影响：兴奋时打字飞快
        if dopamine > 0.8:
            speed_modifier *= 1.3
        
        # 限制速度修正范围 [0.5, 2.0]
        speed_modifier = max(0.5, min(2.0, speed_modifier))
        
        # 计算有效打字速度
        effective_wpm = self.base_wpm * speed_modifier
        
        # 计算每秒字符数（假设平均每个词 5 个字符）
        chars_per_second = effective_wpm * 5 / 60
        
        # 计算基础延迟
        base_delay = text_length / chars_per_second
        
        # 加入随机噪声 (±10%)，模拟手速波动
        noise_factor = random.uniform(0.9, 1.1)
        
        return base_delay * noise_factor
    
    def _calculate_hesitation(self, dominance: float, arousal: float) -> float:
        """
        根据控制度(Dominance)和激活度(Arousal)计算犹豫停顿时间
        """
        # Dominance 越低，犹豫时间越长
        dominance_factor = 1.0 - (dominance * 0.5)
        
        # Arousal 越高，犹豫时间越短（急躁）
        arousal_factor = 1.0 - (arousal * 0.3)
        
        # 计算犹豫时间
        hesitation = self.hesitation_base * dominance_factor * arousal_factor
        
        # 限制犹豫时间范围 [0.1, 3.0]
        hesitation = max(0.1, min(3.0, hesitation))
        
        return hesitation
    
    def _segment_text(self, text: str, pad_state: Dict[str, float]) -> List[str]:
        """
        语义分段器：将完整文本切分为自然的语义块
        """
        arousal = pad_state.get("arousal", 0.0)
        dominance = pad_state.get("dominance", 0.0)
        dopamine = pad_state.get("dopamine", 0.0)
        
        # 情绪影响分段策略
        segment_multiplier = 1.0
        
        if arousal > 0.5 and dominance < -0.3:
            segment_multiplier = 0.8  # 犹豫状态，切分稍碎
            
        # 多巴胺 (Dopamine) 影响：兴奋时连发模式 (Burst Mode)
        if dopamine > 0.8:
            segment_multiplier = 0.5  # 极短的分段，模拟连珠炮
        
        # 按句号、感叹号、问号等完整句尾标点切分
        # 确保句子完整
        segments = re.split(r'([。！？])', text)
        
        # 清洗空字符串
        segments = [s for s in segments if s.strip()]
        
        # 重新组合标点和文本
        bubbles = []
        current_buffer = ""
        
        for i, segment in enumerate(segments):
            current_buffer += segment
            
            # 条件：遇到句尾标点，作为一个完整句子
            if segment in "。！？":
                # 检查缓冲区长度
                if len(current_buffer) >= self.min_segment_length * segment_multiplier:
                    bubbles.append(current_buffer)
                    current_buffer = ""
        
        # 处理剩余内容
        if current_buffer.strip():
            bubbles.append(current_buffer)
        
        # 确保至少有一个分段
        if not bubbles and text.strip():
            bubbles.append(text.strip())
        
        return bubbles
    
    def articulate(
        self,
        full_response_text: str,
        pad_state: Dict[str, float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[ActionEvent]:
        """
        核心接口：接收完整文本，返回动作流
        """
        # 提取情绪参数
        arousal = pad_state.get("arousal", 0.0)
        dominance = pad_state.get("dominance", 0.0)
        pleasure = pad_state.get("pleasure", 0.0)
        cortisol = pad_state.get("cortisol", 0.0)
        
        # 合并元数据
        event_metadata = {
            "pleasure": pleasure,
            "arousal": arousal,
            "dominance": dominance,
            **(metadata or {})
        }
        
        # 1. 语义分段
        segments = self._segment_text(full_response_text, pad_state)
        
        # 2. 生成动作流
        actions = []
        
        for i, segment in enumerate(segments):
            # 计算打字时间
            typing_duration = self._calculate_typing_delay(len(segment), pad_state)
            
            # 计算犹豫停顿
            hesitation_duration = self._calculate_hesitation(dominance, arousal)
            
            # 添加正在输入动作
            actions.append(ActionEvent.create_typing(
                duration=typing_duration,
                metadata={**event_metadata, "segment_index": i}
            ))
            
            # 皮质醇 (Cortisol) 影响：压力大时，输入后会犹豫（模拟打了又删）
            if cortisol > 0.7:
                # 额外的纠结时间
                stress_hesitation = random.uniform(1.0, 3.0)
                actions.append(ActionEvent.create_wait(
                    duration=stress_hesitation,
                    metadata={**event_metadata, "reason": "cortisol_hesitation"}
                ))
            
            # 添加发送消息动作
            actions.append(ActionEvent.create_message(
                content=segment,
                metadata={**event_metadata, "segment_index": i}
            ))
            
            # 如果不是最后一段，添加停顿动作
            if i < len(segments) - 1:
                actions.append(ActionEvent.create_wait(
                    duration=hesitation_duration,
                    metadata={**event_metadata, "segment_index": i}
                ))
        
        return actions
    
    def articulate_with_emotion(
        self,
        full_response_text: str,
        emotion_state: Dict[str, float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[ActionEvent]:
        """
        带情绪状态的表达（兼容旧接口）
        """
        return self.articulate(full_response_text, emotion_state, metadata)
