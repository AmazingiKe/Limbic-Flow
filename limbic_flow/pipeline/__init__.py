from typing import Dict, Any, Optional, List
import numpy as np
from limbic_flow.core.emotion_engine import EmotionEngine
from limbic_flow.core.hippocampus import HippocampusInterface, MockHippocampus, FileHippocampus
from limbic_flow.core.amygdala import Amygdala
from limbic_flow.core.neocortex import NeocortexInterface, MockNeocortex
from limbic_flow.middleware.pathology import BasePathologyMiddleware, DepressionPathology, AlzheimerPathology
from limbic_flow.core.ai import LLMFactory, Message, MessageRole
from limbic_flow.core.location import LocationDetector
from limbic_flow.core.ai.embedding import EmbeddingService

class LimbicFlowPipeline:
    """
    Limbic-Flow 主流程管道
    处理从输入到输出的完整数据流
    """
    
    def __init__(self, llm_provider: Optional[str] = None):
        """
        初始化 Limbic-Flow 管道
        
        Args:
            llm_provider: LLM 提供商（openai, deepseek, anthropic, ollama）
                        如果为 None，使用环境变量 DEFAULT_LLM_PROVIDER
        """
        # 初始化核心组件
        self.emotion_engine = EmotionEngine()
        self.hippocampus = FileHippocampus()  # 使用文件持久化存储
        self.amygdala = Amygdala()
        self.neocortex = MockNeocortex()  # 实际使用时应替换为真实的图数据库
        self.location_detector = LocationDetector()
        
        # 初始化嵌入服务
        self.embedding_service = EmbeddingService()
        
        # 初始化病理中间件
        self.pathology_middleware = BasePathologyMiddleware()
        self.pathology_middleware.add_pathology(DepressionPathology())
        self.pathology_middleware.add_pathology(AlzheimerPathology())
        
        # 初始化 LLM
        self.llm_factory = LLMFactory()
        self.llm = self.llm_factory.create_llm(llm_provider)
        
        # 检测并缓存用户位置
        self.user_location = self.location_detector.detect_location()
        
        # 用户信息存储
        self.user_info = {}
        
        # 从记忆中加载用户信息
        self._load_user_info_from_memory()
    
    def _load_user_info_from_memory(self):
        """
        从记忆中加载用户信息
        """
        try:
            # 生成多个查询向量，用于检索不同类型的用户信息
            query_vectors = [
                self.embedding_service.get_embedding("用户信息 名字"),
                self.embedding_service.get_embedding("用户信息 个人信息"),
                self.embedding_service.get_embedding("用户介绍 自己")
            ]
            
            # 汇总所有检索到的记忆
            all_memories = []
            for query_vector in query_vectors:
                memories = self.hippocampus.retrieve_memories(query_vector, limit=5)
                all_memories.extend(memories)
            
            # 去重
            unique_memories = []
            seen_contents = set()
            for memory in all_memories:
                if isinstance(memory, dict):
                    content = f"{memory.get('user_input', '')}:{memory.get('system_response', '')}"
                    if content not in seen_contents:
                        seen_contents.add(content)
                        unique_memories.append(memory)
            
            # 查找包含用户信息的记忆
            user_info_memories = []
            for memory in unique_memories:
                if isinstance(memory, dict) and "user_info" in memory and memory["user_info"]:
                    user_info_memories.append(memory)
            
            # 按时间戳排序，合并用户信息
            if user_info_memories:
                # 确保记忆包含时间戳
                user_info_memories = [m for m in user_info_memories if "timestamp" in m]
                if user_info_memories:
                    # 按时间戳降序排序
                    user_info_memories.sort(key=lambda x: x["timestamp"], reverse=True)
                    
                    # 合并用户信息，优先使用最新的信息
                    merged_user_info = {}
                    for memory in user_info_memories:
                        user_info = memory.get("user_info", {})
                        # 只合并非空信息
                        for key, value in user_info.items():
                            if value and key not in merged_user_info:
                                merged_user_info[key] = value
                    
                    if merged_user_info:
                        self.user_info = merged_user_info
                        print(f"✅ 从记忆中加载用户信息: {self.user_info}")
        except Exception as e:
            print(f"加载用户信息失败: {str(e)}")
    
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
        response = self._expression(reconstructed_context, emotional_state, user_input)
        
        # 6. 记忆存储: 存储当前交互作为新记忆
        self._store_interaction_memory(user_input, response, emotional_state, perception_result["query_vector"])
        
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
        # 使用嵌入服务生成语义向量
        query_vector = self.embedding_service.get_embedding(user_input)
        
        # 提取用户信息
        self._extract_user_info(user_input)
        
        # 增强的情绪冲击计算
        pleasure = 0.0
        arousal = 0.0
        dominance = 0.0
        
        # 积极情绪词汇（包含中英文）
        positive_words = ["你好", "hello", "hi", "嗨", "高兴", "开心", "快乐", "good", "happy", "joy", "love", "喜欢", "谢谢", "thanks"]
        # 消极情绪词汇
        negative_words = ["伤心", "难过", "生气", "愤怒", "bad", "sad", "angry", "hate", "讨厌", "烦", "无聊"]
        # 唤醒情绪词汇
        arousing_words = ["兴奋", "激动", "震惊", "surprise", "exciting", "wow", "哇", "厉害", "棒"]
        # 平静情绪词汇
        calming_words = ["平静", "放松", "peace", "calm", "relax", "休息", "安静"]
        # 控制感词汇
        dominance_words = ["控制", "power", "dominate", "决定", "选择", "我要", "我想"]
        # 无力感词汇
        helpless_words = ["无助", "weak", "submit", "不知道", "怎么办", "帮我"]
        
        # 计算情绪冲击
        user_input_lower = user_input.lower()
        if any(word in user_input_lower or word in user_input for word in positive_words):
            pleasure += 0.3
        if any(word in user_input_lower or word in user_input for word in negative_words):
            pleasure -= 0.3
        if any(word in user_input_lower or word in user_input for word in arousing_words):
            arousal += 0.3
        if any(word in user_input_lower or word in user_input for word in calming_words):
            arousal -= 0.2
        if any(word in user_input_lower or word in user_input for word in dominance_words):
            dominance += 0.2
        if any(word in user_input_lower or word in user_input for word in helpless_words):
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
    
    def _extract_user_info(self, user_input: str):
        """
        提取用户信息并存储
        
        Args:
            user_input: 用户输入文本
        """
        import re
        
        # 跳过询问名字的问题
        name_question_patterns = [
            r"我叫什么名字",
            r"你知道我叫什么",
            r"你还记得我叫什么",
            r"What's my name",
            r"Do you know my name",
            r"Remember my name"
        ]
        
        for pattern in name_question_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return
        
        # 提取名字 - 支持带标点和不带标点的情况
        name_patterns = [
            # 带标点的情况
            r"我叫(.*?)[。，！？]",
            r"我的名字是(.*?)[。，！？]",
            r"你可以叫我(.*?)[。，！？]",
            r"I'm (.*?)[.!?]",
            r"My name is (.*?)[.!?]",
            r"You can call me (.*?)[.!?]",
            # 不带标点的情况
            r"我叫(.*?)$",
            r"我的名字是(.*?)$",
            r"你可以叫我(.*?)$",
            r"I'm (.*?)$",
            r"My name is (.*?)$",
            r"You can call me (.*?)$"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, user_input)
            if match:
                name = match.group(1).strip()
                if name and not any(stop_word in name for stop_word in ["什么", "怎么", "怎样", "吗", "?"]):
                    self.user_info["name"] = name
                    print(f"✅ 提取到用户名字: {name}")
                    break
        
        # 提取其他信息（可扩展）
        # 例如：年龄、爱好、职业等
    
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
        
        # 增强记忆：优先保留包含用户信息的记忆
        enhanced_memories = self._enhance_memories(distorted_memories)
        
        return enhanced_memories
    
    def _enhance_memories(self, memories: list) -> list:
        """
        增强记忆 - 优先保留包含用户信息的记忆
        
        Args:
            memories: 记忆列表
        
        Returns:
            list: 增强后的记忆列表
        """
        if not memories:
            return []
        
        # 分离包含用户信息的记忆和普通记忆
        user_info_memories = []
        regular_memories = []
        
        for memory in memories:
            if isinstance(memory, dict) and "user_info" in memory and memory["user_info"]:
                user_info_memories.append(memory)
            else:
                regular_memories.append(memory)
        
        # 优先返回包含用户信息的记忆，然后是普通记忆
        # 确保总数量不超过5个
        enhanced_memories = user_info_memories[:3] + regular_memories[:2]
        
        return enhanced_memories
    
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
    
    def _expression(self, reconstructed_context: Dict[str, Any], emotional_state: Dict[str, Any], user_input: str) -> str:
        """
        渲染表达 - 生成回复
        
        Args:
            reconstructed_context: 重构的上下文
            emotional_state: 当前情绪状态
            user_input: 用户原始输入
        
        Returns:
            str: 生成的回复
        """
        # 构建 LLM 提示词
        system_prompt = self._build_system_prompt(emotional_state)
        user_prompt = self._build_user_prompt(reconstructed_context, emotional_state, user_input)
        
        try:
            response = self.llm.chat_simple(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.8
            )
            return response.content
        except Exception as e:
            # 如果 LLM 调用失败，回退到简化实现
            return self._fallback_expression(emotional_state)
    
    def _build_system_prompt(self, emotional_state: Dict[str, Any]) -> str:
        """
        构建系统提示词
        
        Args:
            emotional_state: 当前情绪状态
        
        Returns:
            str: 系统提示词
        """
        pleasure = emotional_state["pleasure"]
        arousal = emotional_state["arousal"]
        dominance = emotional_state["dominance"]
        dopamine = emotional_state["dopamine"]
        cortisol = emotional_state["cortisol"]
        
        # 生成情绪表达风格指南，而不是直接陈述情绪状态
        emotion_style_guide = ""
        
        # 基于愉悦度的表达风格
        if pleasure > 0.5:
            emotion_style_guide += "使用非常积极、热情的语气，充满活力。可以使用更多的感叹号和积极的表情符号。\n"
        elif pleasure > 0.2:
            emotion_style_guide += "使用友好、温暖的语气，带有轻微的积极情绪。可以适当使用表情符号。\n"
        elif pleasure < -0.5:
            emotion_style_guide += "使用温和、理解的语气，带有轻微的忧郁。避免使用过多的感叹号和过于活泼的表达。\n"
        elif pleasure < -0.2:
            emotion_style_guide += "使用平静、稳重的语气，保持中性偏温和。\n"
        else:
            emotion_style_guide += "使用平静、自然的语气，保持中性。\n"
        
        # 基于唤醒度的表达风格
        if arousal > 0.5:
            emotion_style_guide += "回应应该更加生动、有活力，可能会稍微长一些，表达更丰富的细节。\n"
        elif arousal < -0.5:
            emotion_style_guide += "回应应该简洁、平静，节奏较慢，避免过于复杂的表达。\n"
        
        # 基于压力水平的表达风格
        if cortisol > 0.7:
            emotion_style_guide += "表现出轻微的紧张或专注，回应会更加直接和有条理。\n"
        
        # 获取位置信息
        location_summary = self.location_detector.get_location_summary(self.user_location)
        
        # 构建用户信息部分
        user_info_str = ""
        if self.user_info:
            user_info_str = "用户信息：\n"
            if "name" in self.user_info:
                user_info_str += f"- 名字: {self.user_info['name']}\n"
            # 可以添加其他用户信息
            user_info_str += "\n"
        
        system_prompt = f"""你是一个具有人类情绪特征的 AI 助手。

表达风格指南：
{emotion_style_guide}

{user_info_str}
用户的位置信息：
{location_summary}

请根据上述风格指南、用户信息和用户的位置信息，以自然、真实的方式回应。
注意：
1. 如果用户询问时间、天气、地点等信息，请参考上述位置信息
2. 保持友好、温暖的语气，避免冷漠的回应
3. 可以适当使用表情符号增强表达效果
4. 绝对不要直接陈述你的情绪状态或情绪数值，而是通过语言风格和语气来体现
5. 如果用户询问关于他们自己的信息（如名字），请使用存储的用户信息回答
6. 如果你已经知道用户的名字，请在回应中使用他们的名字
7. 回应应该直接回答用户的问题，不要重复无关的内容
8. 不要提及任何关于"愉悦度"、"唤醒度"或其他情绪指标的数值或状态
9. 不要猜测用户的位置，除非位置信息明确提供"""
        
        return system_prompt
    
    def _build_user_prompt(self, reconstructed_context: Dict[str, Any], emotional_state: Dict[str, Any], user_input: str) -> str:
        """
        构建用户提示词
        
        Args:
            reconstructed_context: 重构的上下文
            emotional_state: 当前情绪状态
            user_input: 用户原始输入
        
        Returns:
            str: 用户提示词
        """
        memories = reconstructed_context.get("memories", [])
        
        prompt = "用户刚刚说：\n"
        prompt += user_input + "\n\n"
        
        # 添加用户信息
        if self.user_info:
            prompt += "用户信息：\n"
            if "name" in self.user_info:
                prompt += f"- 名字: {self.user_info['name']}\n"
            prompt += "\n"
        
        if memories:
            prompt += "相关的记忆：\n"
            for i, memory in enumerate(memories, 1):
                # 提取记忆中的用户输入和系统响应
                if isinstance(memory, dict):
                    if "user_input" in memory:
                        prompt += f"{i}. 用户说: '{memory['user_input'][:100]}...'\n"
                    if "system_response" in memory:
                        prompt += f"   系统回应: '{memory['system_response'][:100]}...'\n"
                    # 提取记忆中的用户信息
                    if "user_info" in memory:
                        memory_user_info = memory["user_info"]
                        if memory_user_info:
                            prompt += "   用户信息: "
                            if "name" in memory_user_info:
                                prompt += f"名字: {memory_user_info['name']}"
                            prompt += "\n"
                else:
                    prompt += f"{i}. {memory}\n"
            prompt += "\n"
        
        prompt += "请根据用户的输入和用户信息，给出一个自然、真实的回应。\n"
        prompt += "重要提示：\n"
        prompt += "1. 如果用户询问关于他们自己的信息（如名字、爱好等），请使用存储的用户信息回答\n"
        prompt += "2. 如果你已经知道用户的名字，请在回应中使用他们的名字\n"
        prompt += "3. 回应应该通过语言风格和语气体现情感，绝对不要直接陈述情绪状态或情绪数值\n"
        prompt += "4. 回应应该直接回答用户的问题，不要重复无关的内容\n"
        prompt += "5. 保持友好、温暖的语气，避免冷漠的回应\n"
        prompt += "6. 不要提及任何关于'愉悦度'、'唤醒度'或其他情绪指标的数值或状态\n"
        prompt += "7. 不要猜测用户的位置，除非位置信息明确提供"
        
        return prompt
    
    def _fallback_expression(self, emotional_state: Dict[str, Any]) -> str:
        """
        回退的表达生成 - 当 LLM 调用失败时使用
        
        Args:
            emotional_state: 当前情绪状态
        
        Returns:
            str: 生成的回复
        """
        pleasure = emotional_state["pleasure"]
        arousal = emotional_state["arousal"]
        dopamine = emotional_state["dopamine"]
        cortisol = emotional_state["cortisol"]
        
        # 构建基础回应
        if pleasure > 0.3:
            base_response = "我现在感觉很开心！有什么我可以帮忙的吗？"
        elif pleasure < -0.3:
            base_response = "我现在有点沮丧。你有什么想聊的吗？"
        elif arousal > 0.3:
            base_response = "我现在感觉精力充沛！你在想什么？"
        elif cortisol > 0.7:
            base_response = "我现在感觉压力很大。让我们冷静一下。"
        else:
            base_response = "我在这里。你想讨论什么？"
        
        # 如果知道用户名字，添加到回应中
        if self.user_info and "name" in self.user_info:
            name = self.user_info["name"]
            if base_response.startswith("我现在"):
                base_response = f"{name}，{base_response}"
            elif base_response.startswith("我在这里"):
                base_response = f"{name}，{base_response}"
        
        return base_response
    
    def _store_interaction_memory(self, user_input: str, response: str, emotional_state: Dict[str, Any], query_vector: "np.ndarray"):
        """
        存储交互记忆
        
        Args:
            user_input: 用户输入文本
            response: 系统响应文本
            emotional_state: 情绪状态
            query_vector: 查询向量
        """
        import time
        
        # 创建记忆对象
        memory = {
            "vector": query_vector.tolist(),
            "pad": {
                "pleasure": emotional_state["pleasure"],
                "arousal": emotional_state["arousal"],
                "dominance": emotional_state["dominance"]
            },
            "timestamp": time.time(),
            "user_input": user_input,
            "system_response": response,
            "emotional_state": emotional_state,
            "user_info": self.user_info.copy(),  # 存储当前用户信息
            "narrative": f"用户说: '{user_input[:50]}...'，系统回应: '{response[:50]}...'"
        }
        
        # 存储记忆
        try:
            memory_id = self.hippocampus.store_memory(memory)
            # 可选：记录存储成功的日志
            # print(f"记忆存储成功，ID: {memory_id}")
        except Exception as e:
            # 记忆存储失败不应影响主流程
            # print(f"记忆存储失败: {str(e)}")
            pass