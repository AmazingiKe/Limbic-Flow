# Limbic-Flow 项目修改计划

> 基于 32 个研究文档的实施方案

---

## 一、当前项目状态

### 现有模块
- ✅ OCC 情感模型 (22种情绪)
- ✅ PAD 情感计算器
- ✅ 神经递质系统 (多巴胺、皮质醇)
- ✅ 情绪衰减引擎
- ✅ 海马体 (情景记忆 + 向量检索)
- ✅ 杏仁核 (情绪存储)
- ✅ 病理中间件 (可插拔)
- ✅ API 接口

### 需要新增/强化
- ❌ 完整记忆巩固系统
- ❌ 元认知模块
- ❌ 意识模型
- ❌ 睡眠/梦模拟
- ❌ 预测处理
- ❌ 更复杂的病理模块
- ❌ Obsidian/FlowUs 适配器

---

## 二、修改计划

### Phase 1: 核心情感引擎强化 (Week 1-2)

#### 1.1 扩展神经递质系统
```
新增文件: limbic_flow/core/neurotransmitter/
├── dopamine.py        # 多巴胺系统 (奖励预测误差)
├── serotonin.py       #血清素系统 (情绪稳定)
├── acetylcholine.py  # 乙酰胆碱系统 (注意力)
├── norepinephrine.py  # 去甲肾上腺素系统 (唤醒)
└── __init__.py
```

**实现要点:**
- 每种神经递质有独立的时间动力学 (上升/下降速度)
- 递质之间相互影响 (如皮质醇抑制血清素)
- 与情绪状态双向绑定

#### 1.2 情绪调节算法
```
新增: limbic_flow/core/emotion/regulation.py
```

**功能:**
- 认知重评 (Cognitive Reappraisal)
- 情绪抑制 vs 表达
- 正念调节
- 基于上下文的策略选择

---

### Phase 2: 记忆系统升级 (Week 3-5)

#### 2.1 向量化海马体
```
新增: limbic_flow/core/hippocampus/vector_store.py
```

**功能:**
- ChromaDB 集成
- 情绪加权检索
- 时间衰减 (Ebbinghaus 曲线)
- 情景记忆标签

#### 2.2 记忆巩固系统
```
新增: limbic_flow/core/hippocampus/consolidation.py
```

**功能:**
- 睡眠阶段模拟 (NREM/REM)
- 记忆重播优先级
- 长期记忆转换
- 遗忘机制

#### 2.3 情感记忆标记
```
新增: limbic_flow/core/hippocampus/emotional_tagging.py
```

**功能:**
- 情绪标签 (amygdala-hippocampus binding)
- 情感记忆增强
- 情绪一致性检索偏差

---

### Phase 3: 病理模块扩展 (Week 6-10)

#### 3.1 扩展现有病理模块
```
更新: limbic_flow/middleware/pathology/
├── depression.py      # 强化: 快感缺失、负性偏见
├── ptsd.py           # 强化: 触发词、闪回
├── alzheimer.py      # 强化: 记忆扭曲
├── bipolar.py        # 新增: 躁郁循环
├── anxiety.py        # 新增: 广泛性焦虑
└── autism_adhd.py   # 新增: 神经多样性
```

#### 3.2 心理治疗引擎
```
新增: limbic_flow/middleware/psychotherapy/
├── cbt.py            # 认知行为疗法
├── dbt.py            # 辩证行为疗法
├── act.py            # 接纳与承诺疗法
└── trauma_recovery.py # 创伤恢复
```

---

### Phase 4: 高级认知功能 (Week 11-14)

#### 4.1 元认知系统
```
新增: limbic_flow/core/cognition/metacognition.py
```

**功能:**
- 自我监控系统
- 置信度校准
- 不确定性量化
- 思维 hooks (前/中/后)

#### 4.2 预测处理
```
新增: limbic_flow/core/cognition/predictive.py
```

**功能:**
- 自由能原理
- 主动推理
- 分层预测编码
- 惊异检测

#### 4.3 睡眠与梦
```
新增: limbic_flow/core/cognition/sleep.py
```

**功能:**
- 睡眠周期模型
- 记忆重播
- 梦的情感处理

---

### Phase 5: 外部集成 (Week 15-18)

#### 5.1 Obsidian 适配器
```
新增: limbic_flow/adapters/obsidian/
├── adapter.py
├── sync.py
├── metadata.py
└── __init__.py
```

#### 5.2 FlowUs 适配器
```
新增: limbic_flow/adapters/flowus/
├── adapter.py
├── sync.py
├── metadata.py
└── __init__.py
```

#### 5.3 统一记忆网关
```
新增: limbic_flow/core/memory_gateway.py
```

---

## 三、关键代码修改

### 3.1 情绪状态类增强

```python
# limbic_flow/core/emotion/state.py

@dataclass
class EmotionalState:
    # 现有
    pad: PADState
    
    # 新增
    neurotransmitters: NeurotransmitterState
    appraisal: Optional[Appraisal]  # OCC 评估
    regulation_strategy: Optional[str]  # 调节策略
    
    # 元认知
    confidence: float  # 置信度
    uncertainty: UncertaintyMetrics
    
    # 时间
    last_update: datetime
    decay_schedule: Dict[str, float]
```

### 3.2 海马体接口扩展

```python
# limbic_flow/core/hippocampus/__init__.py

class HippocampusInterface(ABC):
    # 现有方法...
    
    @abstractmethod
    def consolidate_during_sleep(self, sleep_stage: str) -> List[Memory]:
        """睡眠时记忆巩固"""
        pass
    
    @abstractmethod
    def tag_emotional(self, memory_id: str, emotion_tags: Dict) -> None:
        """情感标记"""
        pass
    
    @abstractmethod
    def retrieve_with_bias(self, query: Query, mood_state: MoodState) -> List[Memory]:
        """情绪一致性检索"""
        pass
```

### 3.3 中间件架构扩展

```python
# limbic_flow/middleware/pathology/base.py

class PathologyModule(ABC):
    """病理模块基类 - 扩展支持更多功能"""
    
    @abstractmethod
    def get_therapy_recommendations(self, state: EmotionalState) -> List[Therapy]:
        """获取治疗建议"""
        pass
    
    @abstractmethod
    def calculate_severity(self) -> float:
        """计算严重程度"""
        pass
```

---

## 四、实施优先级

### P0 (立即)
1. 神经递质系统扩展 (dopamine, serotonin, cortisol)
2. 记忆巩固基础 (向量存储 + 情感标记)
3. 病理模块强化 (现有模块bug修复 + 新增)

### P1 (重要)
4. 元认知系统
5. 预测处理基础
6. 心理治疗引擎

### P2 (后续)
7. 睡眠/梦模拟
8. Obsidian/FlowUs 适配器
9. 意识模型

---

## 五、文件结构更新后

```
limbic_flow/
├── core/
│   ├── emotion/
│   │   ├── pad_calculator.py      # 已存在
│   │   ├── occ.py                 # 已存在
│   │   ├── neurotransmitter/     # 新增
│   │   │   ├── __init__.py
│   │   │   ├── dopamine.py
│   │   │   ├── serotonin.py
│   │   │   ├── acetylcholine.py
│   │   │   └── norepinephrine.py
│   │   └── regulation.py          # 新增
│   ├── hippocampus/
│   │   ├── __init__.py            # 已存在
│   │   ├── vector_store.py        # 新增
│   │   ├── consolidation.py       # 新增
│   │   └── emotional_tagging.py    # 新增
│   ├── cognition/                 # 新增
│   │   ├── metacognition.py
│   │   ├── predictive.py
│   │   └── sleep.py
│   ├── amygdala/                  # 已存在
│   └── brain/                      # 已存在
├── middleware/
│   ├── pathology/
│   │   ├── base.py                # 需扩展
│   │   ├── depression.py          # 需强化
│   │   ├── ptsd.py                # 需强化
│   │   ├── bipolar.py             # 新增
│   │   ├── anxiety.py             # 新增
│   │   └── autism_adhd.py        # 新增
│   └── psychotherapy/             # 新增
│       ├── cbt.py
│       ├── dbt.py
│       ├── act.py
│       └── trauma_recovery.py
├── adapters/                       # 新增
│   ├── obsidian/
│   └── flowus/
└── memory_gateway.py              # 新增
```

---

## 六、测试计划

### 单元测试
- PAD 计算准确性
- 神经递质动力学
- 记忆检索算法
- 病理模块行为

### 集成测试
- 情绪 → 记忆 → 反应流程
- 病理状态下的行为变化
- 外部适配器同步

---

*End of Modification Plan*
