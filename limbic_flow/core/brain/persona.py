import yaml
import os
from typing import Dict, Any, List
from limbic_flow.core.types import CognitiveState

class PersonaManager:
    """
    人设管理器 - 负责加载和渲染人设驱动文件
    """

    def __init__(self, persona_file: str = "assets/personas/girlfriend.yaml"):
        self.persona_data = self._load_persona(persona_file)

    def _load_persona(self, file_path: str) -> Dict[str, Any]:
        """加载 YAML 配置文件"""
        # 1. 尝试直接作为绝对路径或相对于当前工作目录的路径
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)

        # 2. 尝试相对于项目根目录查找
        # 当前文件位置: limbic_flow/core/brain/persona.py
        # 项目根目录: ../../../
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "../../../"))

        project_path = os.path.join(project_root, file_path)

        if os.path.exists(project_path):
            with open(project_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)

        # 3. 尝试相对于 limbic_flow 包目录查找 (处理 pip 安装情况)
        # ../../ -> limbic_flow/
        pkg_root = os.path.abspath(os.path.join(current_dir, "../../"))
        pkg_path = os.path.join(pkg_root, file_path)

        if os.path.exists(pkg_path):
             with open(pkg_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)

        raise FileNotFoundError(f"Persona file not found: {file_path}\nTried:\n- {os.path.abspath(file_path)}\n- {project_path}")

    def render_system_prompt(self, state: CognitiveState, location_summary: str = "") -> str:
        """
        根据当前状态渲染 System Prompt
        """
        # 1. 获取基础人设
        base_prompt = self.persona_data.get('base_prompt', '')

        # 2. 计算动态情绪指令
        emotion_instructions = self._get_emotion_instructions(state)

        # 3. 提取用户信息
        user_info_str = self._format_user_info(state)

        # 4. 组装
        full_prompt = f"""{base_prompt}

当前情绪风格指南（必须严格执行）：
{emotion_instructions}

{user_info_str}
你的位置感知：
{location_summary}
"""
        return full_prompt

    def _get_emotion_instructions(self, state: CognitiveState) -> str:
        """根据 PAD 和神经递质匹配规则"""
        rules = self.persona_data.get('emotion_rules', {})
        instructions = []

        # 提取当前数值
        pleasure = state.pad_vector['pleasure']
        arousal = state.pad_vector['arousal']
        cortisol = state.neurotransmitters['cortisol']

        # 匹配 Pleasure 规则
        for rule in rules.get('pleasure', []):
            range_min, range_max = rule['range']
            if range_min <= pleasure <= range_max:
                instructions.append(f"- {rule['instruction']}")
                break # 只要匹配到一个区间就停止

        # 匹配 Arousal 规则
        for rule in rules.get('arousal', []):
            range_min, range_max = rule['range']
            if range_min <= arousal <= range_max:
                instructions.append(f"- {rule['instruction']}")
                break

        # 匹配 Cortisol 规则
        for rule in rules.get('cortisol', []):
            range_min, range_max = rule['range']
            if range_min <= cortisol <= range_max:
                instructions.append(f"- {rule['instruction']}")
                break

        return "\n".join(instructions) if instructions else "保持自然，跟随直觉。"

    def _format_user_info(self, state: CognitiveState) -> str:
        user_info = state.context.get("user_info", {})
        if not user_info:
            return ""

        info_str = "当前对话对象信息：\n"
        if "name" in user_info:
            info_str += f"- 名字: {user_info['name']}\n"
        return info_str + "\n"
