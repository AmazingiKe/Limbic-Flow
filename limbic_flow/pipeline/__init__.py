from typing import Dict, Any, Optional
import numpy as np
from limbic_flow.core.emotion_engine import EmotionEngine
from limbic_flow.core.hippocampus import HippocampusInterface, MockHippocampus
from limbic_flow.core.amygdala import Amygdala
from limbic_flow.core.neocortex import NeocortexInterface, MockNeocortex
from limbic_flow.middleware.pathology import BasePathologyMiddleware, DepressionPathology, AlzheimerPathology

class LimbicFlowPipeline:
    """
    Limbic-Flow 主流程管道
    处理从输入到输出的完整数据流
    """
    
    def __init__(self):
        """
        初始化 Limbic-Flow 管道
        """
        # 初始化核心组件
        self.emotion_engine = EmotionEngine()
        self.hippocampus = MockHippocampus()  # 实际使用时应替换为真实的向量数据库
        self.amygdala = Amygdala()
        self.neocortex = MockNeocortex()  # 实际使用时应替换为真实的图数据库
        
        # 初始化病理中间件
        self.pathology_middleware = BasePathologyMiddleware()
        self.pathology_middleware.add_pathology(DepressionPathology())
        self.pathology_middleware.add_pathology(AlzheimerPathology())
    
    def process_input(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入文本
            context: 上下文信息
        
        Returns:
            Dict[str, Any]: 处理结果，包含生成的回复
        """
        # 1. 感知节点: 处理输入，提取语义，计算初始PAD冲击值
        perception_result = self._perception_node(user_input, context)
        
        # 2. 化学反应: 更新情绪状态
        emotional_state = self._chemistry_solver(perception_result)
        
        # 3. 记忆检索与扭曲: 通过病理中间件检索记忆
        memories = self._retrieve_and_distort_memories(perception_result["query_vector"], emotional_state)
        
        # 4. 认知重构: 构建虚构的当下
        reconstructed_context = self._reconstruction(memories, emotional_state)
        
        # 5. 渲染表达: 生成回复
        response = self._expression(reconstructed_context, emotional_state)
        
        return {
            "response": response,
            "emotional_state": emotional_state,
            "memories": memories
        }
    
    def _perception_node(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        感知节点 - 处理输入，提取语义，计算初始PAD冲击值
        
        Args:
            user_input: 用户输入文本
            context: 上下文信息
        
        Returns:
            Dict[str, Any]: 感知结果
        """
        # 简化实现：模拟语义提取和PAD计算
        # 实际实现中，这里应该使用LLM提取语义并计算PAD值
        
        # 生成随机查询向量（实际应使用真实的嵌入模型）
        query_vector = np.random.rand(768)  # 假设使用768维向量
        
        # 简化的情绪冲击计算
        pleasure = 0.0
        arousal = 0.0
        dominance = 0.0
        
        # 简单的关键词匹配来模拟情绪反应
        if any(word in user_input.lower() for word in ["happy", "joy", "love", "good"]):
            pleasure += 0.3
        if any(word in user_input.lower() for word in ["sad", "angry", "hate", "bad"]):
            pleasure -= 0.3
        if any(word in user_input.lower() for word in ["exciting", "surprise", "wow"]):
            arousal += 0.3
        if any(word in user_input.lower() for word in ["calm", "relax", "peace"]):
            arousal -= 0.2
        if any(word in user_input.lower() for word in ["control", "power", "dominate"]):
            dominance += 0.2
        if any(word in user_input.lower() for word in ["helpless", "weak", "submit"]):
            dominance -= 0.2
        
        return {
            "query_vector": query_vector,
            "initial_pad": {
                "pleasure": pleasure,
                "arousal": arousal,
                "dominance": dominance
            },
            "user_input": user_input,
            "context": context
        }
    
    def _chemistry_solver(self, perception_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        化学反应 - 更新情绪状态
        
        Args:
            perception_result: 感知结果
        
        Returns:
            Dict[str, Any]: 更新后的情绪状态
        """
        initial_pad = perception_result["initial_pad"]
        
        # 更新情绪引擎状态
        emotional_state = self.emotion_engine.update(
            initial_pad["pleasure"],
            initial_pad["arousal"],
            initial_pad["dominance"]
        )
        
        # 记录状态到杏仁核
        self.amygdala.log_state(emotional_state, {
            "user_input": perception_result["user_input"],
            "context": perception_result["context"]
        })
        
        return emotional_state
    
    def _retrieve_and_distort_memories(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> list:
        """
        记忆检索与扭曲 - 通过病理中间件检索记忆
        
        Args:
            query_vector: 查询向量
            emotional_state: 当前情绪状态
        
        Returns:
            list: 扭曲后的记忆列表
        """
        # 扭曲查询向量
        distorted_query = self.pathology_middleware.distort_query(query_vector, emotional_state)
        
        # 从海马体检索记忆
        memories = self.hippocampus.retrieve_memories(distorted_query, limit=5)
        
        # 扭曲检索到的记忆
        distorted_memories = self.pathology_middleware.distort_memories(memories, emotional_state)
        
        return distorted_memories
    
    def _reconstruction(self, memories: list, emotional_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        认知重构 - 构建虚构的当下
        
        Args:
            memories: 扭曲后的记忆列表
            emotional_state: 当前情绪状态
        
        Returns:
            Dict[str, Any]: 重构的上下文
        """
        # 构建记忆叙述
        memory_narratives = []
        for memory in memories:
            # 简化实现：使用记忆中的文本或生成默认叙述
            narrative = memory.get("narrative", "A past experience")
            memory_narratives.append(narrative)
        
        # 构建重构的上下文
        reconstructed_context = {
            "memories": memory_narratives,
            "emotional_state": emotional_state,
            "timestamp": emotional_state["timestamp"]
        }
        
        return reconstructed_context
    
    def _expression(self, reconstructed_context: Dict[str, Any], emotional_state: Dict[str, Any]) -> str:
        """
        渲染表达 - 生成回复
        
        Args:
            reconstructed_context: 重构的上下文
            emotional_state: 当前情绪状态
        
        Returns:
            str: 生成的回复
        """
        # 简化实现：根据情绪状态生成回复
        # 实际实现中，这里应该使用LLM作为渲染器
        
        pleasure = emotional_state["pleasure"]
        arousal = emotional_state["arousal"]
        dopamine = emotional_state["dopamine"]
        cortisol = emotional_state["cortisol"]
        
        # 基于情绪状态生成回复
        if pleasure > 0.3:
            return "我现在感觉很开心！有什么我可以帮忙的吗？"
        elif pleasure < -0.3:
            return "我现在有点沮丧。你有什么想聊的吗？"
        elif arousal > 0.3:
            return "我现在感觉精力充沛！你在想什么？"
        elif cortisol > 0.7:
            return "我现在感觉压力很大。让我们冷静一下。"
        else:
            return "我在这里。你想讨论什么？"