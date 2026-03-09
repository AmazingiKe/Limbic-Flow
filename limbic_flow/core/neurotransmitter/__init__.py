"""
神经递质系统 - 基于研究文档实现

参考:
- REWARD_LEARNING_MOTIVATION.md
- HORMONAL_SYSTEMS_MODELING.md
- STRESS_RESPONSE_SYSTEMS.md
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum
import math
import time


class NeurotransmitterType(Enum):
    """神经递质类型"""
    DOPAMINE = "dopamine"           # 多巴胺 - 奖励、动机
    SEROTONIN = "serotonin"         # 血清素 - 情绪稳定
    ACETYLCHOLINE = "acetylcholine" # 乙酰胆碱 - 注意力
    NOREPINEPHRINE = "norepinephrine"  # 去甲肾上腺素 - 唤醒
    CORTISOL = "cortisol"          # 皮质醇 - 压力
    OXYTOCIN = "oxytocin"          # 催产素 - 信任、依恋
    ENDORPHIN = "endorphin"        # 内啡肽 - 疼痛调节


@dataclass
class NeurotransmitterState:
    """
    神经递质状态
    
    每种递质的水平 [0.0 - 1.0]
    """
    dopamine: float = 0.5         # 奖励、动机
    serotonin: float = 0.5         # 情绪稳定、满足感
    acetylcholine: float = 0.5    # 注意力、学习
    norepinephrine: float = 0.5   # 唤醒、警觉
    cortisol: float = 0.2         # 压力反应
    oxytocin: float = 0.5         # 信任、依恋
    endorphin: float = 0.5        # 疼痛调节、愉悦
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "dopamine": self.dopamine,
            "serotonin": self.serotonin,
            "acetylcholine": self.acetylcholine,
            "norepinephrine": self.norepinephrine,
            "cortisol": self.cortisol,
            "oxytocin": self.oxytocin,
            "endorphin": self.endorphin,
        }


@dataclass
class NeurotransmitterDynamics:
    """
    神经递质动力学参数
    
    基于研究文档中的生物学模型:
    - 上升时间 (rise_time): 递质释放所需时间
    - 下降时间 (decay_time): 递质清除所需时间
    - 基线水平 (baseline): 正常状态下的水平
    - 最大/最小: 递质水平的边界
    """
    # 多巴胺: 快速上升，快速下降
    dopamine_rise: float = 0.1      # 快速上升 (秒)
    dopamine_decay: float = 1.0      # 指数下降
    dopamine_baseline: float = 0.5
    
    # 血清素: 慢速变化
    serotonin_rise: float = 10.0     # 慢速上升 (秒)
    serotonin_decay: float = 30.0   # 慢速下降
    serotonin_baseline: float = 0.5
    
    # 乙酰胆碱: 中等速度
    acetylcholine_rise: float = 0.5
    acetylcholine_decay: float = 5.0
    acetylcholine_baseline: float = 0.5
    
    # 去甲肾上腺素: 快速上升，快速下降
    norepinephrine_rise: float = 0.05
    norepinephrine_decay: float = 0.5
    norepinephrine_baseline: float = 0.3
    
    # 皮质醇: 慢速上升，持续时间长
    cortisol_rise: float = 30.0      # 30秒上升
    cortisol_decay: float = 300.0    # 5分钟下降
    cortisol_baseline: float = 0.2
    
    # 催产素: 中等速度
    oxytocin_rise: float = 5.0
    oxytocin_decay: float = 60.0
    oxytocin_baseline: float = 0.5
    
    # 内啡肽: 快速上升，缓慢下降
    endorphin_rise: float = 0.2
    endorphin_decay: float = 10.0
    endorphin_baseline: float = 0.5


class NeurotransmitterSystem:
    """
    神经递质系统
    
    模拟大脑中的神经递质动力学:
    - 奖励系统 (多巴胺)
    - 情绪稳定 (血清素)
    - 注意力 (乙酰胆碱)
    - 唤醒/压力 (去甲肾上腺素、皮质醇)
    - 信任/依恋 (催产素)
    - 疼痛调节 (内啡肽)
    """
    
    def __init__(self, dynamics: Optional[NeurotransmitterDynamics] = None):
        self.state = NeurotransmitterState()
        self.dynamics = dynamics or NeurotransmitterDynamics()
        self.last_update = time.time()
        
        # 历史记录 (用于分析)
        self.history: list[Dict] = []
        self.max_history = 1000
    
    def update(self, stimulus: Dict) -> NeurotransmitterState:
        """
        更新神经递质状态
        
        Args:
            stimulus: 刺激输入，包含:
                - reward: 奖励强度 [0-1]
                - stress: 压力强度 [0-1]
                - social: 社会互动强度 [0-1]
                - pain: 疼痛强度 [0-1]
                - pleasure: 愉悦强度 [0-1]
        
        Returns:
            NeurotransmitterState: 更新后的状态
        """
        current_time = time.time()
        delta_time = current_time - self.last_update
        self.last_update = current_time
        
        # 提取刺激
        reward = stimulus.get("reward", 0.0)
        stress = stimulus.get("stress", 0.0)
        social = stimulus.get("social", 0.0)
        pain = stimulus.get("pain", 0.0)
        pleasure = stimulus.get("pleasure", 0.0)
        
        # === 多巴胺系统 (奖励预测误差) ===
        # 研究: 多巴胺响应奖励预测误差，而非奖励本身
        dopamine_target = self._calculate_dopamine(reward, pleasure)
        self.state.dopamine = self._update_with_dynamics(
            self.state.dopamine, 
            dopamine_target,
            self.dynamics.dopamine_rise,
            self.dynamics.dopamine_decay,
            delta_time
        )
        
        # === 血清素系统 (情绪稳定) ===
        # 研究: 血清素抑制多巴胺，影响情绪稳定性
        serotonin_target = self._calculate_serotonin(pleasure, stress)
        self.state.serotonin = self._update_with_dynamics(
            self.state.serotonin,
            serotonin_target,
            self.dynamics.serotonin_rise,
            self.dynamics.serotonin_decay,
            delta_time
        )
        
        # === 乙酰胆碱系统 (注意力) ===
        # 研究: 乙酰胆碱调节注意力切换
        acetylcholine_target = self._calculate_acetylcholine(stimulus)
        self.state.acetylcholine = self._update_with_dynamics(
            self.state.acetylcholine,
            acetylcholine_target,
            self.dynamics.acetylcholine_rise,
            self.dynamics.acetylcholine_decay,
            delta_time
        )
        
        # === 去甲肾上腺素系统 (唤醒) ===
        # 研究: 去甲肾上腺素调节警觉性
        norepinephrine_target = self._calculate_norepinephrine(stress, reward)
        self.state.norepinephrine = self._update_with_dynamics(
            self.state.norepinephrine,
            norepinephrine_target,
            self.dynamics.norepinephrine_rise,
            self.dynamics.norepinephrine_decay,
            delta_time
        )
        
        # === 皮质醇系统 (压力) ===
        # 研究: 皮质醇响应压力，滞后于去甲肾上腺素
        cortisol_target = self._calculate_cortisol(stress)
        self.state.cortisol = self._update_with_dynamics(
            self.state.cortisol,
            cortisol_target,
            self.dynamics.cortisol_rise,
            self.dynamics.cortisol_decay,
            delta_time
        )
        
        # === 催产素系统 (信任/依恋) ===
        # 研究: 催产素促进信任形成
        oxytocin_target = self._calculate_oxytocin(social, pleasure)
        self.state.oxytocin = self._update_with_dynamics(
            self.state.oxytocin,
            oxytocin_target,
            self.dynamics.oxytocin_rise,
            self.dynamics.oxytocin_decay,
            delta_time
        )
        
        # === 内啡肽系统 (疼痛调节) ===
        # 研究: 内啡肽响应疼痛和愉悦
        endorphin_target = self._calculate_endorphin(pain, pleasure)
        self.state.endorphin = self._update_with_dynamics(
            self.state.endorphin,
            endorphin_target,
            self.dynamics.endorphin_rise,
            self.dynamics.endorphin_decay,
            delta_time
        )
        
        # === 递质相互作用 ===
        self._apply_neurotransmitter_interactions()
        
        # 记录历史
        self._record_history()
        
        return self.state
    
    def _calculate_dopamine(self, reward: float, pleasure: float) -> float:
        """计算多巴胺目标水平"""
        # 研究: 多巴胺对奖励和愉悦都响应
        # 但对新颖性更敏感
        target = (reward * 0.6 + pleasure * 0.4)
        return min(1.0, max(0.0, target))
    
    def _calculate_serotonin(self, pleasure: float, stress: float) -> float:
        """计算血清素目标水平"""
        # 研究: 血清素与愉悦正相关，与压力负相关
        # 皮质醇抑制血清素
        cortisol_effect = 1.0 - self.state.cortisol * 0.5
        target = (pleasure * 0.7 - stress * 0.3) * cortisol_effect
        return min(1.0, max(0.0, target))
    
    def _calculate_acetylcholine(self, stimulus: Dict) -> float:
        """计算乙酰胆碱目标水平"""
        # 研究: 乙酰胆碱响应新奇和需要专注的刺激
        novelty = stimulus.get("novelty", 0.0)
        focus = stimulus.get("focus_required", 0.0)
        target = novelty * 0.4 + focus * 0.6
        return min(1.0, max(0.0, target))
    
    def _calculate_norepinephrine(self, stress: float, reward: float) -> float:
        """计算去甲肾上腺素目标水平"""
        # 研究: 去甲肾上腺素响应压力和重要奖励
        target = stress * 0.7 + reward * 0.3
        return min(1.0, max(0.0, target))
    
    def _calculate_cortisol(self, stress: float) -> float:
        """计算皮质醇目标水平"""
        # 研究: 皮质醇是最后响应的压力激素
        # 延迟效应
        target = 0.2 + stress * 0.8
        return min(1.0, max(0.0, target))
    
    def _calculate_oxytocin(self, social: float, pleasure: float) -> float:
        """计算催产素目标水平"""
        # 研究: 催产素响应社会互动和身体接触
        target = social * 0.7 + pleasure * 0.3
        return min(1.0, max(0.0, target))
    
    def _calculate_endorphin(self, pain: float, pleasure: float) -> float:
        """计算内啡肽目标水平"""
        # 研究: 内啡肽响应疼痛缓解和愉悦
        pain_relief = 1.0 - pain  # 疼痛缓解
        target = pain_relief * 0.5 + pleasure * 0.5
        return min(1.0, max(0.0, target))
    
    def _update_with_dynamics(
        self, 
        current: float, 
        target: float, 
        rise_time: float,
        decay_time: float,
        delta_time: float
    ) -> float:
        """使用动力学模型更新递质水平"""
        if target > current:
            # 上升阶段
            rate = delta_time / rise_time if rise_time > 0 else 1.0
            new_value = current + (target - current) * rate
        else:
            # 下降阶段
            rate = delta_time / decay_time if decay_time > 0 else 1.0
            new_value = current - (current - target) * rate
        
        return min(1.0, max(0.0, new_value))
    
    def _apply_neurotransmitter_interactions(self):
        """应用神经递质相互作用"""
        # 研究: 递质之间相互影响
        
        # 皮质醇抑制血清素
        serotonin_inhibition = 1.0 - self.state.cortisol * 0.3
        self.state.serotonin *= serotonin_inhibition
        
        # 皮质醇抑制多巴胺 (长期压力降低奖励敏感度)
        dopamine_inhibition = 1.0 - self.state.cortisol * 0.2
        self.state.dopamine *= dopamine_inhibition
        
        # 血清素抑制多巴胺波动
        dopamine_stabilization = 0.8 + self.state.serotonin * 0.2
        self.state.dopamine *= dopamine_stabilization
        
        # 去甲肾上腺素增强唤醒
        if self.state.norepinephrine > 0.7:
            self.state.acetylcholine *= 1.2  # 增强注意力
    
    def _record_history(self):
        """记录历史"""
        self.history.append({
            "timestamp": self.last_update,
            "state": self.state.to_dict()
        })
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_reward_sensitivity(self) -> float:
        """获取奖励敏感度 (基于多巴胺)"""
        return self.state.dopamine
    
    def get_stress_level(self) -> float:
        """获取压力水平 (基于皮质醇和去甲肾上腺素)"""
        return (self.state.cortisol * 0.6 + self.state.norepinephrine * 0.4)
    
    def get_attention_level(self) -> float:
        """获取注意力水平 (基于乙酰胆碱)"""
        return self.state.acetylcholine
    
    def get_emotional_stability(self) -> float:
        """获取情绪稳定性 (基于血清素)"""
        return self.state.serotonin
    
    def get_trust_level(self) -> float:
        """获取信任水平 (基于催产素)"""
        return self.state.oxytocin
    
    def decay_to_baseline(self, elapsed_seconds: float) -> NeurotransmitterState:
        """衰减到基线水平"""
        decay_factor = 0.5 ** (elapsed_seconds / 60.0)  # 1分钟半衰期
        
        self.state.dopamine = self._decay_toward(
            self.state.dopamine, self.dynamics.dopamine_baseline, decay_factor
        )
        self.state.serotonin = self._decay_toward(
            self.state.serotonin, self.dynamics.serotonin_baseline, decay_factor
        )
        self.state.acetylcholine = self._decay_toward(
            self.state.acetylcholine, self.dynamics.acetylcholine_baseline, decay_factor
        )
        self.state.norepinephrine = self._decay_toward(
            self.state.norepinephrine, self.dynamics.norepinephrine_baseline, decay_factor
        )
        self.state.cortisol = self._decay_toward(
            self.state.cortisol, self.dynamics.cortisol_baseline, decay_factor
        )
        self.state.oxytocin = self._decay_toward(
            self.state.oxytocin, self.dynamics.oxytocin_baseline, decay_factor
        )
        self.state.endorphin = self._decay_toward(
            self.state.endorphin, self.dynamics.endorphin_baseline, decay_factor
        )
        
        return self.state
    
    def _decay_toward(self, current: float, target: float, factor: float) -> float:
        """向目标衰减"""
        return current * factor + target * (1 - factor)


class RewardPredictionError:
    """
    奖励预测误差计算
    
    研究: 多巴胺信号编码奖励预测误差 (RPE)
    RPE = 实际奖励 - 预期奖励
    """
    
    def __init__(self):
        self.expected_reward = 0.5  # 初始预期
        self.alpha = 0.1  # 学习率
    
    def compute(self, actual_reward: float) -> float:
        """
        计算奖励预测误差
        
        Args:
            actual_reward: 实际获得的奖励 [0-1]
        
        Returns:
            float: 预测误差 (正值 = 超出预期, 负值 = 低于预期)
        """
        rpe = actual_reward - self.expected_reward
        
        # 更新预期 (学习)
        self.expected_reward += self.alpha * rpe
        
        return rpe
    
    def get_dopamine_signal(self, rpe: float) -> float:
        """
        将RPE转换为多巴胺信号
        
        正RPE -> 增加多巴胺
        负RPE -> 减少多巴胺
        """
        # 多巴胺响应是RPE的缩放
        # 超出预期: 多巴胺激增
        # 低于预期: 多巴胺下降
        return 0.5 + rpe * 0.5


# 示例用法
if __name__ == "__main__":
    # 创建系统
    nt_system = NeurotransmitterSystem()
    
    # 模拟奖励刺激
    stimulus = {
        "reward": 0.8,
        "stress": 0.1,
        "social": 0.3,
        "pain": 0.0,
        "pleasure": 0.7
    }
    
    # 更新
    state = nt_system.update(stimulus)
    print("After reward:", state.to_dict())
    
    # 计算奖励预测误差
    rpe_calculator = RewardPredictionError()
    rpe = rpe_calculator.compute(0.9)
    dopamine_signal = rpe_calculator.get_dopamine_signal(rpe)
    print(f"RPE: {rpe}, Dopamine signal: {dopamine_signal}")
