import math
import time

class EmotionEngine:
    """
    情绪引擎 - 负责计算和管理情绪状态
    核心功能:
    - PAD模型向量计算 (Pleasure, Arousal, Dominance)
    - 神经递质模拟 (Dopamine, Cortisol)
    - 情绪半衰期衰减
    """
    
    def __init__(self):
        # 初始状态 - 中性情绪基线
        self.pleasure = 0.0  # 愉悦度 [-1, 1]
        self.arousal = 0.0   # 唤醒度 [-1, 1]
        self.dominance = 0.0 # 控制度 [-1, 1]
        
        # 神经递质水平 [0, 1]
        self.dopamine = 0.5   # 多巴胺 - 奖励系统
        self.cortisol = 0.3   # 皮质醇 - 压力系统
        
        # 上次更新时间戳
        self.last_update_time = time.time()
        
        # 半衰期参数 (秒)
        self.half_life_pleasure = 3600  # 1小时
        self.half_life_arousal = 1800   # 30分钟
        self.half_life_dominance = 2700 # 45分钟
        self.half_life_dopamine = 300   # 5分钟
        self.half_life_cortisol = 600   # 10分钟
    
    def update(self, input_pleasure=0.0, input_arousal=0.0, input_dominance=0.0):
        """
        更新情绪状态
        
        Args:
            input_pleasure: 输入的愉悦度变化 [-1, 1]
            input_arousal: 输入的唤醒度变化 [-1, 1]
            input_dominance: 输入的控制度变化 [-1, 1]
        
        Returns:
            dict: 更新后的情绪状态
        """
        # 计算时间差
        current_time = time.time()
        time_delta = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # 应用半衰期衰减
        self._apply_half_life_decay(time_delta)
        
        # 应用新输入
        self.pleasure += input_pleasure
        self.arousal += input_arousal
        self.dominance += input_dominance
        
        # 应用神经递质变化
        self._update_neurotransmitters()
        
        # 确保值在有效范围内
        self._clamp_values()
        
        return self.get_state()
    
    def _apply_half_life_decay(self, time_delta):
        """
        应用半衰期衰减公式
        
        Args:
            time_delta: 时间差 (秒)
        """
        # 衰减到基线 (0)
        decay_factor_pleasure = math.exp(-math.log(2) * time_delta / self.half_life_pleasure)
        decay_factor_arousal = math.exp(-math.log(2) * time_delta / self.half_life_arousal)
        decay_factor_dominance = math.exp(-math.log(2) * time_delta / self.half_life_dominance)
        decay_factor_dopamine = math.exp(-math.log(2) * time_delta / self.half_life_dopamine)
        decay_factor_cortisol = math.exp(-math.log(2) * time_delta / self.half_life_cortisol)
        
        self.pleasure *= decay_factor_pleasure
        self.arousal *= decay_factor_arousal
        self.dominance *= decay_factor_dominance
        self.dopamine = 0.5 + (self.dopamine - 0.5) * decay_factor_dopamine
        self.cortisol = 0.3 + (self.cortisol - 0.3) * decay_factor_cortisol
    
    def _update_neurotransmitters(self):
        """
        根据情绪状态更新神经递质水平
        """
        # 愉悦度影响多巴胺
        dopamine_change = self.pleasure * 0.1
        self.dopamine += dopamine_change
        
        # 唤醒度影响皮质醇
        cortisol_change = abs(self.arousal) * 0.1
        self.cortisol += cortisol_change
    
    def _clamp_values(self):
        """
        确保所有值在有效范围内
        """
        # PAD值范围 [-1, 1]
        self.pleasure = max(-1.0, min(1.0, self.pleasure))
        self.arousal = max(-1.0, min(1.0, self.arousal))
        self.dominance = max(-1.0, min(1.0, self.dominance))
        
        # 神经递质范围 [0, 1]
        self.dopamine = max(0.0, min(1.0, self.dopamine))
        self.cortisol = max(0.0, min(1.0, self.cortisol))
    
    def get_state(self):
        """
        获取当前情绪状态
        
        Returns:
            dict: 当前情绪状态
        """
        return {
            "pleasure": self.pleasure,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "dopamine": self.dopamine,
            "cortisol": self.cortisol,
            "timestamp": self.last_update_time
        }