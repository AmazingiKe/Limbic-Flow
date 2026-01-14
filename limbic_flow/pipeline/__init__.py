from typing import Dict, Any, Optional, List, Generator
import numpy as np
import time
import re
from limbic_flow.core.types import CognitiveState
from limbic_flow.core.articulation.action_event import ActionEvent
from limbic_flow.core.hippocampus import FileHippocampus
from limbic_flow.core.amygdala import Amygdala
from limbic_flow.core.articulation.motor_cortex import MotorCortex
from limbic_flow.core.brain.processor import Brain
from limbic_flow.middleware.pathology import BasePathologyMiddleware, DepressionPathology, AlzheimerPathology
from limbic_flow.core.ai.embedding import EmbeddingService

class LimbicFlowPipeline:
    """
    [职责] 认知总线调度器
    [场景] 协调各器官（感知、情绪、记忆、思考、表达）的数据流转
    [核心] 维护 CognitiveState 的生命周期
    """
    
    def __init__(self, llm_provider: Optional[str] = None):
        # 1. 核心器官实例化
        self.embedding_service = EmbeddingService()
        self.amygdala = Amygdala()
        self.hippocampus = FileHippocampus()
        self.brain = Brain(llm_provider)
        self.motor_cortex = MotorCortex()
        
        # 2. 中间件初始化
        self.pathology_middleware = BasePathologyMiddleware()
        self.pathology_middleware.add_pathology(DepressionPathology())
        self.pathology_middleware.add_pathology(AlzheimerPathology())
        
        # 3. 辅助状态
        self.user_info = {}
        self._load_user_info_from_memory()

    def process_input_stream(self, user_input: str, context: Dict[str, Any] = None) -> Generator[ActionEvent, None, None]:
        """
        [职责] 处理用户输入，生成动作流
        [流程] Input -> Perception -> Amygdala -> Hippocampus -> Pathology -> Brain -> MotorCortex -> Output
        """
        # 1. Create State (初始化认知状态)
        state = CognitiveState(user_input=user_input, context=context or {})
        state.context["user_info"] = self.user_info # 注入用户信息
        
        # 2. Perception (感知: 提取向量 + 初始 PAD)
        self._perception(state)
        
        # 3. Amygdala (化学反应: 计算神经递质)
        state = self.amygdala.process(state)
        
        # 4. Hippocampus (记忆检索)
        if state.query_vector is not None:
            state.memories = self.hippocampus.retrieve_memories(state.query_vector, limit=5)
            state.raw_memories = state.memories # Compatibility
            
        # 5. Pathology Middleware (病理扭曲)
        state = self.pathology_middleware.process(state)
        
        # 6. Brain/Neocortex (认知思考: 生成文本)
        state = self.brain.process(state)
        
        # 7. Motor Cortex (运动表达: 生成动作流)
        state = self.motor_cortex.process(state)
        
        # 8. Memory Storage (记忆存储 - 闭环)
        self._store_memory(state)
        
        # 9. Yield Actions (输出动作流)
        for action in state.action_queue:
            yield action
    
    # Alias for compatibility
    process_input = process_input_stream

    def _perception(self, state: CognitiveState):
        """感知节点: 提取语义向量，计算环境压力和初始情绪冲击"""
        # 提取语义向量
        state.query_vector = self.embedding_service.get_embedding(state.user_input)
        
        # 提取用户信息
        self._extract_user_info(state.user_input)
        
        # 简单的关键词情绪冲击计算
        user_input_lower = state.user_input.lower()
        
        if any(w in user_input_lower for w in ["你好", "hello", "hi", "开心", "good", "happy"]):
            state.pad_vector['pleasure'] += 0.3
        if any(w in user_input_lower for w in ["伤心", "bad", "sad", "angry", "讨厌"]):
            state.pad_vector['pleasure'] -= 0.3
        if any(w in user_input_lower for w in ["兴奋", "wow", "surprise"]):
            state.pad_vector['arousal'] += 0.3
        if any(w in user_input_lower for w in ["平静", "calm", "relax"]):
            state.pad_vector['arousal'] -= 0.2
        if any(w in user_input_lower for w in ["控制", "power", "我要"]):
            state.pad_vector['dominance'] += 0.2
        if any(w in user_input_lower for w in ["无助", "help", "weak"]):
            state.pad_vector['dominance'] -= 0.2

        # 环境压力 (模拟)
        if "rain" in str(state.context) or "night" in str(state.context):
            state.environmental_pressure += 0.1

    def _extract_user_info(self, user_input: str):
        # 跳过询问名字的问题
        name_question_patterns = [
            r"我叫什么名字", r"你知道我叫什么", r"你还记得我叫什么",
            r"What's my name", r"Do you know my name"
        ]
        for pattern in name_question_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return
        
        # 提取名字
        name_patterns = [
            r"我叫(.*?)[。，！？]", r"我的名字是(.*?)[。，！？]", r"你可以叫我(.*?)[。，！？]",
            r"我叫(.*?)$", r"我的名字是(.*?)$", r"你可以叫我(.*?)$"
        ]
        for pattern in name_patterns:
            match = re.search(pattern, user_input)
            if match:
                name = match.group(1).strip()
                if name and not any(sw in name for sw in ["什么", "怎么", "怎样", "吗", "?"]):
                    self.user_info["name"] = name
                    print(f"✅ 提取到用户名字: {name}")
                    break

    def _store_memory(self, state: CognitiveState):
        """存储交互记忆"""
        memory = {
            "vector": state.query_vector.tolist() if state.query_vector is not None else [],
            "pad": {
                "pleasure": state.pad_vector['pleasure'],
                "arousal": state.pad_vector['arousal'],
                "dominance": state.pad_vector['dominance']
            },
            "timestamp": state.timestamp,
            "user_input": state.user_input,
            "system_response": state.final_response_text,
            "emotional_state": {
                "pleasure": state.pad_vector['pleasure'],
                "arousal": state.pad_vector['arousal'],
                "dominance": state.pad_vector['dominance'],
                "dopamine": state.neurotransmitters['dopamine'],
                "cortisol": state.neurotransmitters['cortisol']
            },
            "user_info": self.user_info.copy(),
            "narrative": f"用户说: '{state.user_input[:50]}...'，系统回应: '{state.final_response_text[:50]}...'"
        }
        
        try:
            self.hippocampus.store_memory(memory)
        except Exception:
            pass

    def _load_user_info_from_memory(self):
        """从记忆中加载用户信息"""
        try:
            # 简化版：仅搜索“用户信息”
            query_vector = self.embedding_service.get_embedding("用户信息 名字")
            memories = self.hippocampus.retrieve_memories(query_vector, limit=5)
            
            user_info_memories = [m for m in memories if isinstance(m, dict) and m.get("user_info")]
            
            if user_info_memories:
                user_info_memories.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
                merged = {}
                for mem in user_info_memories:
                    info = mem.get("user_info", {})
                    for k, v in info.items():
                        if v and k not in merged:
                            merged[k] = v
                
                if merged:
                    self.user_info = merged
                    print(f"✅ 从记忆中加载用户信息: {self.user_info}")
        except Exception as e:
            print(f"加载用户信息失败: {str(e)}")
