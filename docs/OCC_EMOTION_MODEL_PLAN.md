# Limbic-Flow OCC 情绪模型重构方案

> 文档版本: 1.0
> 创建日期: 2026-03-09
> 作者: Amazing_ike (阿皓)
> 状态: 规划中

---

## 目录

1. [背景与动机](#1-背景与动机)
2. [当前系统诊断](#2-当前系统诊断)
3. [OCC 情绪模型理论](#3-occ-情绪模型理论)
4. [架构设计](#4-架构设计)
5. [数据流变更](#5-数据流变更)
6. [详细实现步骤](#6-详细实现步骤)
7. [文件修改清单](#7-文件修改清单)
8. [新数据结构定义](#8-新数据结构定义)
9. [代码示例](#9-代码示例)
10. [配置变更](#10-配置变更)
11. [测试策略](#11-测试策略)
12. [风险与缓解](#12-风险与缓解)
13. [时间线与里程碑](#13-时间线与里程碑)
14. [附录](#14-附录)

---

## 1. 背景与动机

### 1.1 项目愿景

Limbic-Flow 是一个计算精神病学引擎，旨在模拟人类认知的不完美性。通过数学情感模型与噪声注入的 RAG 中间件，在向量数据库环境中模拟情感衰减、记忆扭曲和病理特征。

### 1.2 现有情绪模型的局限

当前系统采用 **PAD 模型**（Pleasure-Arousal-Dominance），这是一个经典的维度型情绪模型。PAD 模型将情绪映射到三个连续维度：

- **Pleasure (愉悦度)**: 情绪的正负极性，从 -1（悲伤）到 +1（喜悦）
- **Arousal (唤醒度)**: 情绪的激活程度，从 -1（平静）到 +1（兴奋）
- **Dominance (控制度)**: 对情绪的控制能力，从 -1（无助）到 +1（掌控）

然而，PAD 模型存在以下根本性局限：

#### 1.2.1 语义模糊性

PAD 模型的三个维度无法区分具有相似数值但语义完全不同的情绪。例如：

| 情绪 | Pleasure | Arousal | Dominance |
|------|----------|---------|-----------|
| 恐惧 (Fear) | -0.6 | +0.7 | -0.6 |
| 愤怒 (Anger) | -0.5 | +0.7 | +0.5 |

从 PAD 数值来看，两者的 Pleasure 和 Arousal 非常接近，但它们的语义本质和应对策略完全不同。恐惧倾向于逃避，愤怒倾向于攻击。当前的病理模块无法针对具体情绪类型进行差异化处理。

#### 1.2.2 缺乏因果归因

PAD 模型无法表达「情绪的来源」。OCC 模型的核心洞见是：情绪是对事件的认知评估结果。同一个事件（比如「朋友取消了约定」），不同的人可能有不同的归因方式，从而产生不同的情绪：

- 归因于朋友不重视 → 愤怒
- 归因于朋友遇到困难 → 担心
- 归因于自己被讨厌 → 悲伤

当前的 PAD 模型完全无法表达这种因果归因。

#### 1.2.3 病理模块的粗糙触发

现有的病理模块（如 DepressionPathology）使用极其简单的阈值判断：

```python
def should_apply(self, emotional_state):
    cortisol = emotional_state.get("cortisol", 0.0)
    pleasure = emotional_state.get("pleasure", 0.0)
    return cortisol > 0.4 or pleasure < -0.2
```

这种判断无法区分「因为失业而悲伤」（需要支持）还是「因为错过公交车而愤怒」（需要安抚）。缺乏对具体情绪类型的感知能力。

#### 1.2.4 Prompt 生成的语义贫乏

当前的 PromptBuilder 只能基于 PAD 数值生成风格指南：

```
"使用积极、热情的语气，充满活力。可以使用更多的感叹号和积极的表情符号。"
```

这种描述缺乏语义特异性，无法精准控制 LLM 的表达方式。比如，我们无法让 LLM 「表现出愤怒但克制」还是「表现出恐惧但试图勇敢」。

### 1.3 OCC 模型的优势

OCC（Ortony, Clore, Collins）模型是一种基于认知评估的情绪模型，由 Ortony、Clore 和 Collins 于 1988 年提出。与 PAD 模型相比，OCC 模型具有以下优势：

#### 1.3.1 情绪类型的完整性

OCC 模型定义了 22 种基本情绪类型，覆盖了人类情绪的绝大部分场景：

| 类别 | 情绪类型 | 触发条件 |
|------|----------|----------|
| 事件结果 | Hope, Satisfaction, Relief, Joy, Disappointment, Fear-Confounding | 对事件的评估 |
| 行为评估 | Pride, Shame, Admiration, Reproach | 对他人/自己的行为评估 |
| 对象吸引 | Love, Hate | 对对象的吸引程度 |
| 复合情绪 | Gratitude, Anger, Fear, Distress, Happiness, Sadness | 多种评估的组合 |

#### 1.3.2 认知评估的显式表达

OCC 模型将情绪生成过程分解为明确的认知评估维度：

- **Desirability (期望程度)**: 事件对主体的好坏程度
- **Likelihood (可能性)**: 事件发生的可能性
- **Praiseworthiness (称赞程度): 行为的道德评价
- **Attractiveness (吸引力)**: 对象对主体的吸引程度
- **Causal Attribution (因果归因)**: 归因于自己还是他人

这种显式的评估结构使得情绪生成过程完全可解释、可调试。

#### 1.3.3 病理模拟的精确性

基于 OCC 模型，病理模块可以实现精确的情绪级别干预：

- **抑郁症**: 压低 joy/satisfaction/hope，放大 sadness/distress
- **PTSD**: 触发词 → fear/distress 闪回
- **HSP**: 放大所有情绪的感知强度

### 1.4 重构目标

本次重构的核心目标是：

1. **认知深度提升**: 从「数值映射」升级为「语义理解」，让情绪系统真正理解用户在说什么
2. **向下兼容**: PAD 模型退化为 OCC 的低维投影，保持所有下游模块接口不变
3. **可调试性**: 每个情绪的产生都有明确的认知评估路径，便于追踪和调试
4. **病理精确性**: 病理模块能够针对具体情绪类型进行差异化处理
5. **Prompt 语义丰富**: PromptBuilder 能够基于具体情绪类型生成精准的风格指南

---

## 2. 当前系统诊断

### 2.1 代码组织结构

当前 Limbic-Flow 的情绪相关代码分布在以下模块中：

```
limbic_flow/
├── core/
│   ├── types.py                 # CognitiveState 定义
│   ├── config.py               # LimbicConfig 配置
│   ├── emotion/
│   │   ├── __init__.py         # 模块导出
│   │   └── occ.py              # OCC 模型（已实现但未集成）
│   ├── amygdala/
│   │   ├── __init__.py         # Amygdala 核心逻辑
│   │   ├── decay.py            # 衰减计算
│   │   └── storage.py          # SQLite 存储
│   ├── brain/
│   │   ├── processor.py         # Brain 处理器
│   │   └── prompt_builder.py   # Prompt 构建
│   └── ai/
│       └── ...
├── pipeline/
│   ├── __init__.py             # LimbicFlowPipeline
│   └── config.py               # PipelineConfig
├── middleware/
│   └── pathology/
│       ├── __init__.py
│       ├── classic.py           # 经典病理模块
│       └── pluggable.py        # 插件化病理
└── utils/
    └── emotion_analyzer.py     # 情绪分析工具
```

### 2.2 当前数据流

当前 Pipeline 的处理流程如下：

```
用户输入
    ↓
_perception()          # 关键词 → PAD delta
    ↓
amygdala.process()    # PAD 衰减 + 神经递质计算
    ↓
pathology_middleware.distort_query()  # PAD 驱动的查询扭曲
    ↓
hippocampus.retrieve_memories()       # 记忆检索
    ↓
pathology_middleware.process()        # PAD 驱动的记忆扭曲
    ↓
brain.process()       # PAD 驱动的 Prompt 生成
    ↓
motor_cortex.process()  # 动作流生成
    ↓
输出
```

### 2.3 关键问题点

#### 问题 1: OCC 代码已实现但完全断线

`core/emotion/occ.py` 包含完整的 OCC 模型实现（约 300 行代码），包括：

- `OCCEmotion` 枚举（22 种情绪）
- `Appraisal` 数据类（认知评估结构）
- `OCCState` 数据类（情绪状态）
- `OCCEngine` 类（评估逻辑）

**问题**: 这个模块在 Pipeline 中 **零引用**，完全处于未使用状态。

#### 问题 2: 感知层过于简陋

`_perception()` 方法使用硬编码的关键词匹配来计算 PAD 值：

```python
# pipeline/__init__.py:140-151
if any(w in user_input_lower for w in ["你好", "hello", "hi", "开心", "good", "happy"]):
    state.pad_vector['pleasure'] += 0.3
if any(w in user_input_lower for w in ["伤心", "bad", "sad", "angry", "讨厌"]):
    state.pad_vector['pleasure'] -= 0.3
```

这种实现无法处理：
- 否定句（「我不开心」）
- 复杂语义（「我今天本来很开心，但是...」）
- 反讽（「真是太好了」）
- 归因（「他骂了我，所以我很生气」）

#### 问题 3: 病理模块缺乏情绪语义理解

当前的病理模块只能读取 PAD 数值，无法感知具体情绪类型：

```python
# classic.py:135-138
def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
    cortisol = emotional_state.get("cortisol", 0.0)
    pleasure = emotional_state.get("pleasure", 0.0)
    return cortisol > 0.4 or pleasure < -0.2
```

这导致：
- 抑郁症模块无法区分「悲伤」和「愤怒」
- PTSD 模块无法感知「恐惧」情绪的触发
- HSP 模块无法针对特定情绪类型进行放大

#### 问题 4: Prompt 生成缺乏特异性

当前的 PromptBuilder 只能生成基于 PAD 数值的风格指南：

```python
# prompt_builder.py:119-120
if pleasure > 0.5:
    guide.append("使用非常积极、热情的语气，充满活力...")
```

这种描述无法精准控制 LLM 的表达方式，比如「愤怒地抱怨」vs「悲伤地倾诉」vs「恐惧地颤抖」需要完全不同的表达策略。

### 2.4 当前代码缺陷

#### 缺陷 1: OCC 引擎中的 typo

文件: `core/emotion/occ.py:258`

```python
# ❌ 错误代码
self.state.self_shame = abs(appraise.praiseworthiness) * abs(appraisal.causal_attribution_self)

# ✅ 正确代码
self.state.self_shame = abs(appraisal.praiseworthiness) * abs(appraisal.causal_attribution_self)
```

变量名 `appraise` 应为 `appraisal`。

#### 缺陷 2: 感知节点关键词匹配过于简陋

当前实现使用简单的关键词列表匹配，无法处理自然语言的复杂性。

#### 缺陷 3: 记忆存储缺乏 OCC 字段

当前的 `EmotionalMemory` 数据类只存储 PAD 向量和神经递质，缺少 OCC 情绪状态的快照。

---

## 3. OCC 情绪模型理论

### 3.1 OCC 模型概述

OCC 模型由 Ortony、Clore 和 Collins 于 1988 年在《The Cognitive Structure of Emotions》一书中提出。该模型的核心观点是：**情绪是对事件、行为或对象的认知评估结果**。

OCC 模型将情绪分为三大类：

1. **事件结果情绪 (Consequences of Events)**: 对发生在自己身上的事件的情绪反应
2. **代理行为情绪 (Actions of Agents)**: 对他人或自己的行为的情绪反应
3. **对象吸引情绪 (Aspects of Objects)**: 对事物或人的吸引程度的情绪反应

### 3.2 情绪类型详解

#### 3.2.1 事件结果情绪（Prospect-Based）

这类情绪基于对事件结果（通常是期望与现实的一致性）的评估：

| 情绪 | 英文 | 触发条件 |
|------|------|----------|
| 希望 | Hope | 正向事件 + 未发生 + 高可能性 |
| 满意 | Satisfaction | 正向事件 + 已发生 |
| 宽慰 | Relief | 负向事件 + 预期未发生 |
| 喜悦 | Joy | 正向事件 + 已发生 |
| 失望 | Disappointment | 负向事件 + 已发生 |
| 恐惧困惑 | Fear-Confounding | 负向事件 + 高可能性 + 未发生 |

#### 3.2.2 行为评估情绪（Agent Actions）

这类情绪基于对行为（通常是道德评价）的评估：

| 情绪 | 英文 | 触发条件 |
|------|------|----------|
| 自豪 | Pride | 自己的正向行为 |
| 羞耻 | Shame | 自己的负向行为 |
| 钦佩 | Admiration | 他人的正向行为 |
| 责备 | Reproach | 他人的负向行为 |

#### 3.2.3 对象吸引情绪（Object Aspects）

这类情绪基于对对象的吸引程度评估：

| 情绪 | 英文 | 触发条件 |
|------|------|----------|
| 爱 | Love | 高吸引 |
| 恨 | Hate | 低吸引 |

#### 3.2.4 复合情绪

| 情绪 | 英文 | 组成 |
|------|------|------|
| 感激 | Gratitude | 钦佩 + 喜悦 |
| 愤怒 | Anger | 责备 + 失望 |
| 恐惧 | Fear | 恐惧困惑 + 失望 |
| 苦恼 | Distress | 失望 + 悲伤 |
| 幸福 | Happiness | 喜悦 + 满意 |
| 悲伤 | Sadness | 失望 + 失望 |

### 3.3 认知评估维度

OCC 模型使用以下评估维度来确定情绪类型和强度：

#### 3.3.1 事件评估维度

- **Desirability (期望程度)**: 事件对主体的好坏程度，范围 [-1, 1]
  - +1: 非常好的事情
  - 0: 中性事件
  - -1: 非常坏的事情

- **Likelihood (可能性)**: 事件发生的可能性，范围 [0, 1]
  - 1: 肯定发生
  - 0.5: 可能发生
  - 0: 不可能发生

- **Expectedness (预期性)**: 事件是否符合预期，范围 [0, 1]
  - 1: 完全符合预期
  - 0: 完全出乎意料

- **Realized (实现性)**: 事件是否已经发生，布尔值

- **Goal Relevance (目标相关性)**: 事件是否与主体目标相关，布尔值

#### 3.3.2 行为评估维度

- **Praiseworthiness (称赞程度)**: 行为的道德评价，范围 [-1, 1]
  - +1: 值得称赞
  - 0: 中性
  - -1: 应受谴责

- **Causal Attribution Self (归因自己)**: 归因于自己的程度，范围 [-1, 1]
  - +1: 完全是自己的责任
  - -1: 完全不是自己的责任

- **Causal Attribution Other (归因他人)**: 归因于他人的程度，范围 [-1, 1]

#### 3.3.3 对象评估维度

- **Attractiveness (吸引力)**: 对象的吸引程度，范围 [-1, 1]
  - +1: 非常有吸引力
  - 0: 中性
  - -1: 没有吸引力甚至令人厌恶

### 3.4 OCC 到 PAD 的映射

虽然 OCC 模型在语义表达上更丰富，但 PAD 模型在某些场景下仍有价值（如需要连续数值进行衰减计算）。我们可以建立 OCC 到 PAD 的映射：

| OCC 情绪 | Pleasure | Arousal | Dominance |
|----------|----------|---------|-----------|
| Joy | +0.8 | +0.3 | +0.2 |
| Hope | +0.5 | +0.2 | +0.1 |
| Satisfaction | +0.6 | -0.1 | +0.3 |
| Relief | +0.4 | -0.3 | +0.2 |
| Fear | -0.6 | +0.7 | -0.6 |
| Disappointment | -0.5 | -0.2 | -0.3 |
| Sadness | -0.7 | -0.3 | -0.4 |
| Anger | -0.5 | +0.7 | +0.5 |
| Pride | +0.5 | +0.3 | +0.6 |
| Shame | -0.5 | +0.2 | -0.6 |
| Admiration | +0.5 | +0.2 | -0.1 |
| Reproach | -0.4 | +0.3 | +0.3 |
| Love | +0.7 | +0.3 | +0.1 |
| Hate | -0.6 | +0.5 | +0.3 |
| Gratitude | +0.6 | +0.1 | -0.1 |
| Distress | -0.6 | +0.4 | -0.5 |

### 3.5 差异化半衰期

不同情绪的持续时间差异很大，这是 OCC 模型的重要扩展点：

| 情绪类别 | 典型半衰期 | 理由 |
|----------|------------|------|
| 愤怒 (Anger) | 900 秒 (15 分钟) | 情绪来得快去得也快 |
| 惊讶 (Surprise) | 600 秒 (10 分钟) | 惊讶是短暂的 |
| 恐惧 (Fear) | 1200 秒 (20 分钟) | 恐惧消退较快 |
| 喜悦 (Joy) | 3600 秒 (1 小时) | 好心情持续较久 |
| 悲伤 (Sadness) | 5400 秒 (1.5 小时) | 悲伤持续更久 |
| 爱 (Love) | 86400 秒 (24 小时) | 爱是持久的 |
| 恨 (Hate) | 43200 秒 (12 小时) | 恨也持续较久 |
| 自豪 (Pride) | 7200 秒 (2 小时) | 成就感持续较久 |
| 羞耻 (Shame) | 14400 秒 (4 小时) | 羞耻感更持久 |

---

## 4. 架构设计

### 4.1 总体架构

本次重构采用 **「OCC 为主 + PAD 为投影」的双层架构**：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           用户输入                                       │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      感知节点 (Perception)                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              LLM 驱动的认知评估器 (LLMAppraiser)                   │   │
│  │  - 语义理解: 理解用户输入的深层含义                                  │   │
│  │ - 评估生成: 产出 OCC Appraisal 结构                               │   │
│  │ - 规则回退: LLM 不可用时的规则引擎兜底                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      OCC 引擎 (OCCEngine)                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  - Appraisal → 22 种情绪强度                                      │   │
│  │  - 差异化半衰期衰减                                               │   │
│  │  - 情绪状态管理                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    OCC → PAD 投影层                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  OCCToPADProjector:                                             │   │
│  │  - 22 种情绪 → pleasure/arousal/dominance                      │   │
│  │  - OCC 情绪 → dopamine/cortisol 神经递质映射                    │   │
│  │  - 归一化到 [-1, 1] 范围                                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
            ┌────────────────────┴────────────────────┐
            │                                         │
            ▼                                         ▼
┌────────────────────────┐              ┌────────────────────────────┐
│    Amygdala (存储)    │              │  PathologyMiddleware     │
│  ┌────────────────┐   │              │  ┌────────────────────┐   │
│  │ PAD + 神经递质  │   │              │  │ OCC 情绪感知扭曲   │   │
│  │ 衰减 + 记录     │   │              │  │ 基于具体情绪类型   │   │
│  └────────────────┘   │              │  └────────────────────┘   │
└────────────────────────┘              └────────────────────────────┘
            │                                         │
            └────────────────────┬────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Brain (认知思考)                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  - system prompt 含 OCC 情绪标签                                │   │
│  │  - 而非抽象的 pleasure=0.7                                      │   │
│  │  - 精准的情绪风格控制                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 核心设计原则

#### 4.2.1 认知驱动原则

情绪不是凭空产生的，而是对输入的认知评估结果。本次重构将情绪生成从「关键词匹配」升级为「语义理解 + 认知评估」。

#### 4.2.2 向下兼容原则

PAD 模型退化为 OCC 的低维投影，所有下游模块（Amygdala、Pathology、PromptBuilder）的接口保持不变，确保存量代码无需修改。

#### 4.2.3 可替换性原则

各组件保持接口抽象，支持替换：

- `LLMAppraiser`: 可替换为本地模型、规则引擎或外部 NLU 服务
- `OCCEngine`: 可替换为其他 OCC 实现
- `OCCToPADProjector`: 映射矩阵可配置化

#### 4.2.4 增量部署原则

重构分阶段进行，每个阶段都可运行、可测试：

1. 阶段 1: 修复 OCC typo + 增强 OCC 引擎
2. 阶段 2: 实现 LLM Appraiser + Pipeline 集成
3. 阶段 3: 病理模块 OCC 感知
4. 阶段 4: PromptBuilder OCC 增强
5. 阶段 5: 完整测试 + 文档

### 4.3 模块职责

| 模块 | 职责 | 关键类/方法 |
|------|------|--------------|
| `LLMAppraiser` | 语义理解 → Appraisal | `appraise()`, `_rule_based_appraise()` |
| `OCCEngine` | 认知评估 → 情绪强度 | `appraise()`, `decay_differential()` |
| `OCCHalfLifeConfig` | 差异化半衰期配置 | `get()` |
| `OCCToPADProjector` | OCC → PAD 投影 | `project()`, `project_neurotransmitters()` |
| `CognitiveState` | 状态容器 | 新增 4 个 OCC 字段 |
| `Pathology` | 情绪感知扭曲 | 新增 `distort_occ()` |
| `PromptBuilder` | OCC 风格指南 | `_build_occ_style_guide()` |

---

## 5. 数据流变更

### 5.1 新数据流

```
用户输入
    │
    ├──────────────────────────────────────────────────────────────┐
    │                      阶段 1: 感知 (Perception)                │
    │                                                               │
    │  1.1 语义向量提取 (EmbeddingService.get_embedding)          │
    │       → state.query_vector                                   │
    │                                                               │
    │  1.2 用户信息提取 (_extract_user_info)                       │
    │       → state.context["user_info"]                           │
    │                                                               │
    │  1.3 LLM 认知评估 (LLMAppraiser.appraise) [新增]            │
    │       user_input → LLM → Appraisal                          │
    │       → state.appraisal                                      │
    │                                                               │
    │  1.4 OCC 情绪推理 (OCCEngine.appraise) [新增]               │
    │       Appraisal → 22 种情绪强度                               │
    │       → state.occ_state                                      │
    │       → state.dominant_emotion                               │
    │       → state.emotion_intensity                             │
    │                                                               │
    │  1.5 OCC → PAD 投影 (OCCToPADProjector) [新增]             │
    │       OCCState → PAD 向量 + 神经递质                         │
    │       → state.pad_vector                                     │
    │       → state.neurotransmitters                             │
    │                                                               │
    │  1.6 环境压力计算                                            │
    │       → state.environmental_pressure                        │
    └──────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    阶段 2: OCC 衰减 (Decay)                         │
│                                                                      │
│  OCCEngine.decay_differential(time_delta, config)                   │
│  - 不同情绪有不同的半衰期                                            │
│  - joy 衰减慢，anger 衰减快                                        │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    阶段 3: Amygdala 处理                             │
│                                                                      │
│  amygdala.process(state)                                              │
│  - 获取历史状态                                                      │
│  - 计算 PAD 衰减 (保持现有逻辑)                                     │
│  - 叠加刺激                                                         │
│  - 计算神经递质                                                      │
│  - 记录到 SQLite                                                   │
│                                                                      │
│  注意: 此时 PAD 已是 OCC 的投影，衰减逻辑保持不变                     │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    阶段 4: 病理中间件 - 查询扭曲                      │
│                                                                      │
│  emotional_state = {                                                │
│      ...state.pad_vector,                                           │
│      ...state.neurotransmitters,                                    │
│      "timestamp": state.timestamp,                                   │
│      "occ_state": state.occ_state.to_dict(),  [新增]              │
│      "dominant_emotion": state.dominant_emotion,  [新增]           │
│  }                                                                  │
│                                                                      │
│  query = pathology_middleware.distort_query(                        │
│      state.query_vector.copy(),                                      │
│      emotional_state                                                 │
│  )                                                                  │
│                                                                      │
│  state.memories = hippocampus.retrieve_memories(                   │
│      query, limit=self.config.memory_limit                          │
│  )                                                                  │
│  state.raw_memories = state.memories                                │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    阶段 5: 病理中间件 - 记忆扭曲                       │
│                                                                      │
│  state = pathology_middleware.process(state)                         │
│  - 扭曲检索到的记忆 (保持现有逻辑)                                    │
│                                                                      │
│  [新增] 病理模块 OCC 情绪扭曲:                                       │
│  for pathology in pathologies:                                      │
│      if hasattr(pathology, 'distort_occ'):                          │
│          if pathology.should_apply(emotional_state):                 │
│              state.occ_state = pathology.distort_occ(               │
│                  state.occ_state,                                    │
│                  severity                                           │
│              )                                                       │
│                                                                      │
│  [新增] 重新投影 PAD (被病理扭曲后):                                  │
│  state.pad_vector = OCCToPADProjector.project(state.occ_state)    │
│  state.dominant_emotion = state.occ_state.get_dominant()            │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    阶段 6: 新皮层 - 语义知识                          │
│                                                                      │
│  state.context["semantic_knowledge"] =                             │
│      self._gather_semantic_knowledge(state)                         │
│                                                                      │
│  当前为 MockNeocortex，返回空列表                                    │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    阶段 7: Brain - 认知思考                          │
│                                                                      │
│  state = brain.process(state)                                       │
│                                                                       │
│  PromptBuilder.build_system_prompt() [增强]                          │
│  - 包含 OCC 情绪标签                                                │
│  - 包含 dominant_emotion 和 emotion_intensity                       │
│  - _build_occ_style_guide() 替代 _build_emotion_style_guide()      │
│                                                                       │
│  PromptBuilder.build_user_prompt()                                   │
│  - 保持现有逻辑                                                     │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    阶段 8: MotorCortex - 动作生成                    │
│                                                                      │
│  state = motor_cortex.process(state)                                │
│  - 解析文本为 TYPING/MESSAGE/WAIT 动作                              │
│  - 保持现有逻辑                                                     │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    阶段 9: 记忆存储                                   │
│                                                                      │
│  _store_memory(state) [增强]                                         │
│  - 保存向量 + PAD + 神经递质 (保持现有逻辑)                          │
│  - [新增] 保存 OCC 情绪快照:                                        │
│      "occ_state": state.occ_state.to_dict(),                       │
│      "dominant_emotion": state.dominant_emotion,                   │
│      "emotion_intensity": state.emotion_intensity,                 │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
输出 (ActionEvent 流)
```

### 5.2 数据流变化对比

| 阶段 | 旧流程 | 新流程 | 变化 |
|------|--------|--------|------|
| 感知 | 关键词 → PAD delta | LLM 语义理解 → Appraisal → OCC → PAD | 重大变化 |
| 衰减 | PAD 统一半衰期 | OCC 差异化半衰期 | 重要变化 |
| 病理触发 | PAD 阈值判断 | PAD 阈值 + OCC 情绪感知 | 重要变化 |
| 病理扭曲 | 仅 PAD 扭曲 | PAD 扭曲 + OCC 扭曲 | 重要变化 |
| Prompt | PAD 数值风格 | OCC 情绪标签风格 | 重要变化 |
| 存储 | 仅 PAD | PAD + OCC | 小变化 |

---

## 6. 详细实现步骤

### 阶段 1: OCC 引擎修复与增强

#### 步骤 1.1: 修复 OCC typo

**文件**: `limbic_flow/core/emotion/occ.py`

找到第 258 行，修复变量名错误：

```python
# 修复前 (第 258 行)
self.state.self_shame = abs(appraise.praiseworthiness) * abs(appraisal.causal_attribution_self)

# 修复后
self.state.self_shame = abs(appraisal.praiseworthiness) * abs(appraisal.causal_attribution_self)
```

#### 步骤 1.2: 添加 OCCHalfLifeConfig

在 `occ.py` 文件末尾添加差异化半衰期配置类：

```python
@dataclass
class OCCHalfLifeConfig:
    """OCC 情绪的差异化半衰期配置

    不同情绪有不同的衰减速度，模拟真实的人类情绪特点：
    - 愤怒消退快（15分钟）
    - 惊讶很短暂（10分钟）
    - 爱持续久（24小时）
    """

    # 快速衰减（秒）
    anger: float = 900           # 愤怒来得快去得快
    surprise: float = 600        # 惊讶很短暂
    fear: float = 1200           # 恐惧消退较快

    # 中等衰减
    joy: float = 3600            # 喜悦持续约 1 小时
    sadness: float = 5400        # 悲伤持续较久
    disappointment: float = 3600 # 失望中等持续
    distress: float = 2700        # 苦恼中等
    relief: float = 1800         # 宽慰较快

    # 慢速衰减
    love: float = 86400          # 爱是长久的
    hate: float = 43200          # 恨也持续很久
    pride: float = 7200          # 自豪感持续较久
    shame: float = 14400         # 羞耻感更持久

    # 行为评估情绪
    hope: float = 3600           # 希望中等
    satisfaction: float = 2700   # 满意中等
    self_pride: float = 5400     # 自我自豪较久
    self_shame: float = 10800    # 自我羞耻更久
    admiration: float = 3600     # 钦佩中等
    reproach: float = 3600       # 责备中等
    gratitude: float = 7200      # 感激持续

    # 对象情绪
    fear_confounding: float = 1200 # 恐惧困惑较短

    # 默认
    default: float = 3600

    def get(self, emotion_name: str) -> float:
        """获取指定情绪的半衰期"""
        return getattr(self, emotion_name, self.default)
```

#### 步骤 1.3: 添加 OCCToPADProjector

在 `occ.py` 文件末尾添加投影器类：

```python
class OCCToPADProjector:
    """
    OCC 情绪 → PAD 维度投影

    [职责] 将离散情绪映射到连续维度空间
    [依据] Mehrabian (1996) 情绪-PAD 映射 + OCC 模型语义
    [可替换性] 映射矩阵可配置化
    """

    # 映射矩阵: emotion_name → (pleasure, arousal, dominance) 权重
    # 基于 Mehrabian 的研究和 OCC 语义
    PROJECTION_MATRIX: Dict[str, Tuple[float, float, float]] = {
        # 正面事件情绪
        "joy":            ( 0.8,  0.3,  0.2),
        "hope":           ( 0.5,  0.2,  0.1),
        "satisfaction":   ( 0.6,  -0.1, 0.3),
        "relief":         ( 0.4,  -0.3, 0.2),
        "happiness":      ( 0.7,  0.2,  0.2),

        # 负面事件情绪
        "fear":           (-0.6,  0.7, -0.6),
        "disappointment": (-0.5, -0.2, -0.3),
        "sadness":        (-0.7, -0.3, -0.4),
        "distress":       (-0.6,  0.4, -0.5),

        # 行为评估情绪
        "pride":          ( 0.5,  0.3,  0.6),
        "shame":          (-0.5,  0.2, -0.6),
        "self_pride":     ( 0.4,  0.2,  0.5),
        "self_shame":     (-0.4,  0.3, -0.5),
        "admiration":     ( 0.5,  0.2, -0.1),
        "reproach":       (-0.4,  0.3,  0.3),

        # 复合情绪
        "gratitude":      ( 0.6,  0.1, -0.1),
        "anger":          (-0.5,  0.7,  0.5),

        # 对象情绪
        "love":           ( 0.7,  0.3,  0.1),
        "hate":           (-0.6,  0.5,  0.3),
    }

    @classmethod
    def project(cls, occ_state: OCCState) -> Dict[str, float]:
        """将 OCC 情绪状态投影到 PAD 空间

        Args:
            occ_state: OCC 情绪状态

        Returns:
            PAD 向量 dict: {pleasure, arousal, dominance}
        """
        p, a, d = 0.0, 0.0, 0.0
        emotions = occ_state.to_dict()

        # 加权求和
        for emotion_name, intensity in emotions.items():
            if intensity <= 0.0:
                continue
            weights = cls.PROJECTION_MATRIX.get(emotion_name, (0, 0, 0))
            p += intensity * weights[0]
            a += intensity * weights[1]
            d += intensity * weights[2]

        # 归一化到 [-1, 1]
        return {
            "pleasure": max(-1.0, min(1.0, p)),
            "arousal":  max(-1.0, min(1.0, a)),
            "dominance": max(-1.0, min(1.0, d)),
        }

    @classmethod
    def project_neurotransmitters(cls, occ_state: OCCState) -> Dict[str, float]:
        """从 OCC 情绪推导神经递质水平

        Args:
            occ_state: OCC 情绪状态

        Returns:
            神经递质 dict: {dopamine, cortisol}
        """
        emotions = occ_state.to_dict()

        # 多巴胺：积极情绪驱动
        dopamine = 0.5  # 基线
        dopamine += emotions.get("joy", 0) * 0.3
        dopamine += emotions.get("satisfaction", 0) * 0.2
        dopamine += emotions.get("hope", 0) * 0.2
        dopamine += emotions.get("love", 0) * 0.15
        dopamine += emotions.get("pride", 0) * 0.15
        dopamine += emotions.get("admiration", 0) * 0.1
        dopamine += emotions.get("gratitude", 0) * 0.15
        dopamine -= emotions.get("sadness", 0) * 0.2
        dopamine -= emotions.get("disappointment", 0) * 0.15
        dopamine -= emotions.get("shame", 0) * 0.1

        # 皮质醇：压力/威胁情绪驱动
        cortisol = 0.3  # 基线
        cortisol += emotions.get("fear", 0) * 0.3
        cortisol += emotions.get("anger", 0) * 0.25
        cortisol += emotions.get("distress", 0) * 0.2
        cortisol += emotions.get("shame", 0) * 0.15
        cortisol += emotions.get("self_shame", 0) * 0.15
        cortisol += emotions.get("reproach", 0) * 0.1
        cortisol -= emotions.get("relief", 0) * 0.15
        cortisol -= emotions.get("joy", 0) * 0.1
        cortisol -= emotions.get("satisfaction", 0) * 0.1

        return {
            "dopamine": max(0.0, min(1.0, dopamine)),
            "cortisol": max(0.0, min(1.0, cortisol)),
        }
```

#### 步骤 1.4: 添加差异化衰减方法

在 `OCCEngine` 类中添加新方法：

```python
def decay_differential(self, time_delta: float, config: OCCHalfLifeConfig = None):
    """差异化衰减 - 不同情绪有不同的半衰期

    joy 消退慢（好心情持续久），anger 消退快（气过了就好了）

    Args:
        time_delta: 经过的时间（秒）
        config: 半衰期配置
    """
    import math
    config = config or OCCHalfLifeConfig()

    emotions = self.state.to_dict()
    for emotion_name, current in emotions.items():
        if current <= 0.001:  # 忽略极小值
            continue
        half_life = config.get(emotion_name)
        decay_factor = math.exp(-math.log(2) * time_delta / half_life)
        setattr(self.state, emotion_name, current * decay_factor)
```

---

### 阶段 2: LLM Appraiser 实现

#### 步骤 2.1: 创建 Appraiser 模块

**新文件**: `limbic_flow/core/emotion/appraiser.py`

```python
"""
LLM 驱动的认知评估器

[职责] 用 LLM 理解用户输入的语义，产出 OCC Appraisal
[设计] 将「情绪理解」从关键词匹配升级为语义理解
[可替换性] 可替换为本地模型、规则引擎、或外部 NLU 服务
"""

import json
from typing import Dict, Any, Optional
from limbic_flow.core.emotion.occ import Appraisal


class LLMAppraiser:
    """
    LLM 驱动的认知评估器

    使用 LLM 对用户输入进行深层次的语义理解，
    生成 OCC 模型所需的认知评估结果。
    """

    APPRAISAL_PROMPT = """你是一个情绪认知评估器。分析用户的输入，返回以下 JSON：

{
  "event_type": "event" | "action" | "object",
  "desirability": -1.0 ~ 1.0,
  "desirability_for_other": -1.0 ~ 1.0,
  "praiseworthiness": -1.0 ~ 1.0,
  "attractiveness": -1.0 ~ 1.0,
  "likelihood": 0.0 ~ 1.0,
  "expectedness": 0.0 ~ 1.0,
  "causal_attribution_self": -1.0 ~ 1.0,
  "causal_attribution_other": -1.0 ~ 1.0,
  "realized": true | false,
  "goal_relevant": true | false
}

只返回 JSON，不要解释。"""

    def __init__(self, llm):
        """初始化评估器

        Args:
            llm: LLM 实例（来自 LLMFactory）
        """
        self.llm = llm

    def appraise(self, user_input: str, context: Dict = None) -> Appraisal:
        """用 LLM 对用户输入进行认知评估

        Args:
            user_input: 用户输入文本
            context: 额外上下文

        Returns:
            Appraisal: 认知评估结果
        """
        context = context or {}

        try:
            # 调用 LLM 进行评估
            response = self.llm.chat_simple(
                prompt=f"用户说: {user_input}",
                system_prompt=self.APPRAISAL_PROMPT,
                temperature=0.3  # 低温度保证稳定性
            )

            # 解析 JSON 响应
            data = json.loads(response.content)
            return self._parse_appraisal(data)

        except (json.JSONDecodeError, AttributeError) as e:
            # JSON 解析失败，回退到规则引擎
            return self._rule_based_appraise(user_input)
        except Exception as e:
            # 其他异常，规则引擎兜底
            return self._rule_based_appraise(user_input)

    def _parse_appraisal(self, data: Dict) -> Appraisal:
        """解析 LLM 返回的评估 JSON

        Args:
            data: LLM 返回的字典

        Returns:
            Appraisal: 评估结果
        """
        return Appraisal(
            desirability=self._clamp(data.get("desirability", 0.0)),
            desirability_for_other=self._clamp(data.get("desirability_for_other", 0.0)),
            praiseworthiness=self._clamp(data.get("praiseworthiness", 0.0)),
            attractiveness=self._clamp(data.get("attractiveness", 0.0)),
            likelihood=max(0.0, min(1.0, data.get("likelihood", 0.5))),
            expectedness=max(0.0, min(1.0, data.get("expectedness", 0.5))),
            causal_attribution_self=self._clamp(data.get("causal_attribution_self", 0.0)),
            causal_attribution_other=self._clamp(data.get("causal_attribution_other", 0.0)),
            realized=data.get("realized", True),
            goal_relevant=data.get("goal_relevant", True),
        )

    def _rule_based_appraise(self, user_input: str) -> Appraisal:
        """规则引擎回退

        当 LLM 不可用时，使用简化的规则引擎进行评估。
        这是现有关键词逻辑的升级版。

        Args:
            user_input: 用户输入

        Returns:
            Appraisal: 评估结果
        """
        text = user_input.lower()
        appraisal = Appraisal()

        # 事件类型推断
        if any(w in text for w in ["我做了", "我完成了", "我决定"]):
            appraisal.praiseworthiness = 0.0  # 待定
            appraisal.realized = True
            appraisal.goal_relevant = True
        elif any(w in text for w in ["他做了", "她说", "他们"]):
            appraisal.praiseworthiness = 0.0  # 待定
            appraisal.realized = True
            appraisal.goal_relevant = True

        # 期望程度判断
        if any(w in text for w in ["开心", "happy", "好事", "成功", "太好了", "好开心", "棒", "喜欢"]):
            appraisal.desirability = 0.7
            appraisal.realized = True
        elif any(w in text for w in ["伤心", "sad", "失败", "难过", "糟糕", "讨厌", "不喜欢"]):
            appraisal.desirability = -0.7
            appraisal.realized = True
        elif any(w in text for w in ["害怕", "fear", "担心", "紧张", "焦虑"]):
            appraisal.desirability = -0.5
            appraisal.likelihood = 0.7
            appraisal.realized = False  # 担心通常是未来的
        elif any(w in text for w in ["希望", "hope", "期待", "希望能"]):
            appraisal.desirability = 0.5
            appraisal.likelihood = 0.6
            appraisal.realized = False
        elif any(w in text for w in ["生气", "angry", "愤怒", "火大", "不爽"]):
            appraisal.desirability = -0.6
            appraisal.praiseworthiness = -0.5
            appraisal.causal_attribution_other = 0.8
            appraisal.realized = True
        elif any(w in text for w in ["骄傲", "proud", "自豪", "厉害"]):
            appraisal.praiseworthiness = 0.7
            appraisal.causal_attribution_self = 0.8
            appraisal.realized = True
        elif any(w in text for w in ["谢谢", "感谢", "感激"]):
            appraisal.desirability = 0.5
            appraisal.praiseworthiness = 0.6
            appraisal.realized = True
        elif any(w in text for w in ["害怕", "恐惧", "吓人"]):
            appraisal.desirability = -0.6
            appraisal.likelihood = 0.7
            appraisal.realized = False

        # 归因推断
        if any(w in text for w in ["都怪他", "是他", "她害的"]):
            appraisal.causal_attribution_other = 0.7
        elif any(w in text for w in ["都怪我", "是我不好", "我的错"]):
            appraisal.causal_attribution_self = 0.7

        return appraisal

    @staticmethod
    def _clamp(v: float) -> float:
        """限制值在 [-1, 1] 范围内"""
        return max(-1.0, min(1.0, v))


# 便捷函数
def create_appraiser(llm) -> LLMAppraiser:
    """创建 LLM 评估器"""
    return LLMAppraiser(llm)
```

#### 步骤 2.2: 更新 emotion 模块导出

**文件**: `limbic_flow/core/emotion/__init__.py`

```python
"""
情感模块

包含:
- OCC: OCC 认知情绪模型
- PAD: PAD 维度情绪模型 (兼容)
- Appraiser: LLM 驱动的认知评估
"""

from limbic_flow.core.emotion.occ import OCCEngine, OCCState, OCCEmotion, create_occ_engine
from limbic_flow.core.emotion.appraiser import LLMAppraiser, create_appraiser

__all__ = [
    "OCCEngine",
    "OCCState",
    "OCCEmotion",
    "create_occ_engine",
    "LLMAppraiser",
    "create_appraiser",
]
```

---

### 阶段 3: CognitiveState 扩展

#### 步骤 3.1: 更新类型定义

**文件**: `limbic_flow/core/types.py`

在 `CognitiveState` 类中添加 OCC 相关字段：

```python
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, TYPE_CHECKING
import time

if TYPE_CHECKING:
    from limbic_flow.core.articulation.action_event import ActionEvent
    from limbic_flow.core.emotion.occ import Appraisal, OCCState

@dataclass
class CognitiveState:
    """
    [职责] 认知状态总线 - 贯穿整个 Pipeline 的核心数据对象
    [场景] 在各个器官之间传递，承载感知、情绪、记忆、表达和动作信息
    [可替换性] 核心数据结构，不可替换
    """

    # ─── 现有字段（保持不变） ───

    # Input Channel (输入通道)
    user_input: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    # Physiological Channel (生理通道)
    pad_vector: Dict[str, float] = field(default_factory=lambda: {
        "pleasure": 0.0,
        "arousal": 0.0,
        "dominance": 0.0
    })
    neurotransmitters: Dict[str, float] = field(default_factory=lambda: {
        "dopamine": 0.5,
        "cortisol": 0.3
    })
    environmental_pressure: float = 0.0

    # Memory Channel (记忆通道)
    query_vector: Optional[Any] = None
    memories: List[Dict[str, Any]] = field(default_factory=list)
    distorted_memories: List[Dict[str, Any]] = field(default_factory=list)

    # Expression Channel (表达通道)
    introspection: str = ""
    final_response_text: str = ""

    # Action Channel (动作通道)
    action_queue: List["ActionEvent"] = field(default_factory=list)

    # ─── 新增: OCC 层 ───

    appraisal: Optional["Appraisal"] = None
    """认知评估结果

    包含用户输入的语义分析结果：
    - desirability: 期望程度
    - praiseworthiness: 称赞程度
    - 因果归因等
    """

    occ_state: Optional["OCCState"] = None
    """OCC 情绪状态

    22 种情绪的强度值 [0, 1]：
    - joy, sadness, anger, fear, hope, pride, shame...
    """

    dominant_emotion: str = "neutral"
    """主导情绪标签

    当前最强的情绪类型，用于：
    - Prompt 风格控制
    - 病理模块触发判断
    - 日志和调试
    """

    emotion_intensity: float = 0.0
    """总情绪强度

    所有情绪强度的平均值 [0, 1]，用于：
    - 判断情绪的激烈程度
    - 调节响应策略
    """

    # ─── 别名属性（保持不变） ───

    @property
    def raw_memories(self) -> List[Dict[str, Any]]:
        return self.memories

    @raw_memories.setter
    def raw_memories(self, value: List[Dict[str, Any]]) -> None:
        self.memories = value

    @property
    def final_text(self) -> str:
        return self.final_response_text

    @final_text.setter
    def final_text(self, value: str) -> None:
        self.final_response_text = value

    @property
    def content(self) -> str:
        return self.final_response_text

    @content.setter
    def content(self, value: str) -> None:
        self.final_response_text = value
```

---

### 阶段 4: Pipeline 集成

#### 步骤 4.1: 更新 Pipeline 初始化

**文件**: `limbic_flow/pipeline/__init__.py`

在 `LimbicFlowPipeline.__init__` 中添加 OCC 引擎和评估器：

```python
def __init__(
    self,
    config: PipelineConfig = None,
    hippocampus: Optional[Any] = None,
    amygdala: Optional[Any] = None,
):
    # ... 现有初始化代码保持不变 ...

    # 新增: OCC 引擎 + 评估器
    from limbic_flow.core.emotion.occ import OCCEngine, OCCHalfLifeConfig
    from limbic_flow.core.emotion.appraiser import LLMAppraiser

    self.occ_engine = OCCEngine()
    self.occ_half_life = OCCHalfLifeConfig()

    # LLM Appraiser（使用与 Brain 相同的 LLM）
    # 注意：这里使用 Brain 的 LLM，后续可优化为更轻量的模型
    self.appraiser = LLMAppraiser(self.brain.llm)

    # 记录上次处理时间，用于计算衰减
    self._last_process_time: Optional[float] = None

    self.logger.info(f"Limbic-Flow Pipeline 初始化完成 (OCC 引擎已启用)")
```

#### 步骤 4.2: 重写感知方法

替换当前的 `_perception()` 方法：

```python
def _perception(self, state: CognitiveState):
    """
    感知节点重构:
    1. 提取语义向量 (embedding)
    2. LLM/规则评估 → Appraisal
    3. OCC 引擎 → 22 种情绪
    4. OCC → PAD 投影 (向下兼容)
    """
    from limbic_flow.core.emotion.occ import OCCToPADProjector

    # 1. 语义向量（不变）
    state.query_vector = self.embedding_service.get_embedding(state.user_input)

    # 2. 提取用户信息（不变）
    self._extract_user_info(state.user_input)

    # 3. 认知评估 (新)
    state.appraisal = self.appraiser.appraise(state.user_input, state.context)

    # 4. OCC 情绪推理 (新)
    event = {
        "type": "event",  # 简化：暂时全部视为事件
        "desirability": state.appraisal.desirability,
        "desirability_for_other": state.appraisal.desirability_for_other,
        "praiseworthiness": state.appraisal.praiseworthiness,
        "attractiveness": state.appraisal.attractiveness,
        "likelihood": state.appraisal.likelihood,
        "expectedness": state.appraisal.expectedness,
        "causal_attribution_self": state.appraisal.causal_attribution_self,
        "causal_attribution_other": state.appraisal.causal_attribution_other,
        "realized": state.appraisal.realized,
        "goal_relevant": state.appraisal.goal_relevant,
    }
    state.occ_state = self.occ_engine.appraise(event)
    state.dominant_emotion = state.occ_state.get_dominant()
    state.emotion_intensity = state.occ_state.get_intensity()

    # 5. OCC → PAD 投影 (兼容层)
    state.pad_vector = OCCToPADProjector.project(state.occ_state)
    state.neurotransmitters = OCCToPADProjector.project_neurotransmitters(state.occ_state)

    # 6. 环境压力 (不变)
    if "rain" in str(state.context) or "night" in str(state.context):
        state.environmental_pressure += 0.1
```

#### 步骤 4.3: 更新主处理流程

修改 `process_input_stream()` 方法，在适当位置添加 OCC 衰减和病理 OCC 扭曲：

```python
def process_input_stream(self, user_input: str, context: Dict[str, Any] = None):
    """处理用户输入，生成动作流"""

    # 1. Create State
    state = CognitiveState(user_input=user_input, context=context or {})
    state.context["user_info"] = self.user_info

    # 2. 感知 (含 OCC 评估)
    self._perception(state)

    # 3. OCC 差异化衰减 (新)
    if self._last_process_time is not None:
        time_delta = state.timestamp - self._last_process_time
        self.occ_engine.decay_differential(
            time_delta=time_delta,
            config=self.occ_half_life
        )
    self._last_process_time = state.timestamp

    # 4. Amygdala 处理 (PAD 投影已在感知中完成)
    state = self.amygdala.process(state)

    # 5. 病理中间件 - 查询扭曲
    emotional_state = {
        **state.pad_vector,
        **state.neurotransmitters,
        "timestamp": state.timestamp,
        "occ_state": state.occ_state.to_dict() if state.occ_state else None,
        "dominant_emotion": state.dominant_emotion,
        "user_input": state.user_input,
    }

    if state.query_vector is not None:
        query = self.pathology_middleware.distort_query(
            state.query_vector.copy(), emotional_state
        )
        state.memories = self.hippocampus.retrieve_memories(
            query, limit=self.config.memory_limit
        )
        state.raw_memories = state.memories

    # 6. 病理中间件 - 记忆扭曲
    state = self.pathology_middleware.process(state)

    # 6.5 病理模块 OCC 情绪扭曲 (新)
    if state.occ_state:
        for pathology in self.pathology_middleware.pathologies:
            if hasattr(pathology, 'distort_occ') and pathology.should_apply(emotional_state):
                severity = getattr(pathology, 'severity', 0.5)
                state.occ_state = pathology.distort_occ(state.occ_state, severity)

        # 重新投影 PAD（被病理扭曲后）
        state.pad_vector = OCCToPADProjector.project(state.occ_state)
        state.dominant_emotion = state.occ_state.get_dominant()

    # 7. 新皮层 - 语义知识
    state.context["semantic_knowledge"] = self._gather_semantic_knowledge(state)

    # 8. Brain - 认知思考
    state = self.brain.process(state)

    # 9. MotorCortex - 动作生成
    state = self.motor_cortex.process(state)

    # 10. 记忆存储 (增强)
    self._store_memory(state)

    # 11. Yield Actions
    for action in state.action_queue:
        yield action
```

---

### 阶段 5: PromptBuilder 增强

#### 步骤 5.1: 更新系统 Prompt 构建

**文件**: `limbic_flow/core/brain/prompt_builder.py`

修改 `build_system_prompt()` 方法，添加 OCC 情绪信息：

```python
def build_system_prompt(
    self,
    state: CognitiveState,
    location_summary: str = ""
) -> str:
    """构建系统提示词 (增强版)

    包含 OCC 情绪标签，用于精准控制 LLM 的表达风格。
    """
    # 情绪风格指南 - OCC 驱动
    if state.occ_state:
        style_guide = self._build_occ_style_guide(
            state.occ_state,
            state.dominant_emotion
        )
    else:
        # 回退到 PAD 版本
        style_guide = self._build_emotion_style_guide(
            state.pad_vector.get('pleasure', 0.0),
            state.pad_vector.get('arousal', 0.0),
            state.pad_vector.get('dominance', 0.0),
            state.neurotransmitters.get('cortisol', 0.3)
        )

    user_info_str = self._build_user_info(state.context.get("user_info", {}))

    # 添加主导情绪信息
    emotion_info = ""
    if state.occ_state:
        emotion_info = f"\n当前情绪状态: {state.dominant_emotion} (强度: {state.emotion_intensity:.1f})"

    return f"""你是一个有点情绪的 AI。尽量像朋友聊天一样自然。

{emotion_info}

表达风格：
- 简洁，像正常人发消息一样
- 少用emoji，最多用1-2个
- 少用套路话（"我理解你的感受"、"根据你的描述"这种不要用）
- 可以用口语化的表达
- 用户叫阿皓
- 直接回答问题，不要绕弯子

{user_info_str}
位置：{location_summary}

注意：别把天聊死，给对方继续聊的空间。

{style_guide}"""
```

#### 步骤 5.2: 添加 OCC 风格指南方法

在 `PromptBuilder` 类中添加新方法：

```python
def _build_occ_style_guide(self, occ_state, dominant: str) -> str:
    """基于 OCC 情绪生成风格指南

    OCC 情绪 → 表达风格映射，提供比 PAD 更精准的控制。

    Args:
        occ_state: OCC 情绪状态
        dominant: 主导情绪标签

    Returns:
        str: 风格指南文本
    """
    # OCC 情绪 → 表达风格映射
    STYLE_MAP = {
        "joy": (
            "语气轻快、温暖，带点幽默感。可以使用更多积极的表达，"
            "但不要过度夸张。"
        ),
        "sadness": (
            "语气温和、低沉，表达理解和陪伴。少用感叹号，"
            "避免过于活泼的表达。可以适当表达共鸣。"
        ),
        "anger": (
            "语气直接、有力，但保持建设性。不要攻击性或指责，"
            "但可以表现出一些不爽。可以适当表达不满。"
        ),
        "fear": (
            "语气关切、安抚，提供安全感和支持。表现出对用户的关心，"
            "不要过于乐观也不要过于悲观。"
        ),
        "hope": (
            "语气积极但克制，表达期待而不过度乐观。"
            "可以鼓励用户，但不要画大饼。"
        ),
        "disappointment": (
            "语气平静但略带遗憾，不回避现实。"
            "可以承认失望，但不要过度消极。"
        ),
        "pride": (
            "语气自信、鼓励，分享成就感。"
            "可以适当夸赞，但不要骄傲自满。"
        ),
        "shame": (
            "语气低调、内敛，避免过度暴露。"
            "不要过于自责或卑微。"
        ),
        "gratitude": (
            "语气真诚、感恩，表达欣赏。"
            "可以真诚地感谢，但不要过于肉麻。"
        ),
        "love": (
            "语气温柔、亲密，表达关心。"
            "可以温暖一些，但不要过于腻歪。"
        ),
        "distress": (
            "语气沉重但坚定，寻求理解。"
            "可以表达苦恼，但不要崩溃。"
        ),
        "relief": (
            "语气轻松、释然，'终于可以松口气了'的感觉。"
            "可以表达放松，但不要幸灾乐祸。"
        ),
        "admiration": (
            "语气欣赏、尊敬，真诚地赞美。"
            "可以表达敬佩，但不要过于谄媚。"
        ),
        "reproach": (
            "语气严肃但不严厉，指出问题但留有余地。"
            "可以批评，但不要攻击。"
        ),
        "satisfaction": (
            "语气满足、平和，'这样就很好'的感觉。"
            "可以表达满意，但不要自满。"
        ),
        "hate": (
            "语气冷淡、疏离，保持距离感。"
            "可以表达不喜，但不要刻薄。"
        ),
        "disgust": (
            "语气厌恶、排斥，但保持克制。"
            "可以表达反感，但不要人身攻击。"
        ),
        "surprise": (
            "语气惊讶、意外，'真是没想到'的感觉。"
            "可以表现出惊讶，但不要过度夸张。"
        ),
        "neutral": (
            "语气平静、自然，保持中性。"
            "根据用户的内容自然回应。"
        ),
    }

    style = STYLE_MAP.get(dominant, STYLE_MAP["neutral"])

    # 叠加次要情绪
    emotions = occ_state.to_dict()
    secondary = sorted(
        [(k, v) for k, v in emotions.items() if k != dominant and v > 0.2],
        key=lambda x: x[1], reverse=True
    )[:2]

    guide = f"【当前情绪】{style}\n"

    if secondary:
        sec_descs = []
        for k, v in secondary:
            sec_style = STYLE_MAP.get(k, "")
            if sec_style:
                sec_descs.append(f"- {k}: {sec_style}")

        if sec_descs:
            guide += f"\n【次要情绪】\n" + "\n".join(sec_descs)
            guide += "\n\n适当融入上述情绪特点，但以主导情绪为主。"

    return guide
```

---

### 阶段 6: 病理模块 OCC 感知

#### 步骤 6.1: 更新抑郁病理模块

**文件**: `limbic_flow/middleware/pathology/classic.py`

修改 `DepressionPathology` 类：

```python
class DepressionPathology(Pathology):
    """
    抑郁模式 - OCC 增强版

    新逻辑:
    - 压低 joy/satisfaction/hope（积极情绪衰减加速）
    - 放大 sadness/distress/disappointment（消极情绪持续更久）
    - 触发条件增加 OCC 情绪感知
    """

    def __init__(self, base_severity: float = 0.3):
        self.base_severity = base_severity

    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        # 保留 PAD 触发条件
        cortisol = emotional_state.get("cortisol", 0.0)
        pleasure = emotional_state.get("pleasure", 0.0)
        pad_trigger = cortisol > 0.4 or pleasure < -0.2

        # 新增: OCC 情绪触发
        occ_state = emotional_state.get("occ_state")
        occ_trigger = False
        if occ_state:
            if isinstance(occ_state, dict):
                occ_trigger = (
                    occ_state.get("sadness", 0) > 0.3 or
                    occ_state.get("distress", 0) > 0.3
                )
            else:
                # OCCState 对象
                occ_trigger = (
                    occ_state.sadness > 0.3 or
                    occ_state.distress > 0.3
                )

        return pad_trigger or occ_trigger

    def _calculate_severity(self, emotional_state: Dict[str, Any]) -> float:
        # 保留原有计算
        cortisol = emotional_state.get("cortisol", 0.3)
        cortisol_boost = max(0.0, (cortisol - 0.4) * 1.0)

        # 新增: 基于 OCC 情绪的严重度计算
        occ_state = emotional_state.get("occ_state")
        occ_boost = 0.0
        if occ_state:
            if isinstance(occ_state, dict):
                sadness = occ_state.get("sadness", 0)
                distress = occ_state.get("distress", 0)
            else:
                sadness = occ_state.sadness
                distress = occ_state.distress
            occ_boost = (sadness + distress) * 0.3

        return min(1.0, self.base_severity + cortisol_boost + occ_boost)

    def distort_query(self, query_vector, emotional_state: Dict[str, Any]) -> np.ndarray:
        severity = self._calculate_severity(emotional_state)
        distortion = np.full_like(query_vector, -0.1 * severity)
        return query_vector + distortion

    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        severity = self._calculate_severity(emotional_state)
        distorted = []

        for memory in memories:
            mem_copy = {k: v.copy() if isinstance(v, dict) else v for k, v in memory.items()}
            memory_pleasure = mem_copy.get("pad", {}).get("pleasure", 0.0)

            # 屏蔽快乐记忆
            if memory_pleasure > 0.2:
                if random.random() < 0.8 * severity:
                    continue

            # 压低愉悦度
            if "pad" in mem_copy:
                mem_copy["pad"]["pleasure"] *= (1.0 - 0.8 * severity)

            distorted.append(mem_copy)

        return distorted

    def distort_occ(self, occ_state, severity: float):
        """扭曲 OCC 情绪状态

        抑郁症的核心特征：
        - 快感缺失 (Anhedonia): 积极情绪被压低
        - 消极偏向: 消极情绪被放大
        """
        if not occ_state:
            return occ_state

        # 压低积极情绪
        occ_state.joy *= (1.0 - 0.7 * severity)
        occ_state.happiness *= (1.0 - 0.7 * severity)
        occ_state.satisfaction *= (1.0 - 0.6 * severity)
        occ_state.hope *= (1.0 - 0.5 * severity)
        occ_state.relief *= (1.0 - 0.4 * severity)

        # 放大消极情绪
        if hasattr(occ_state, 'sadness'):
            occ_state.sadness = min(1.0, occ_state.sadness * (1.0 + 0.5 * severity))
        if hasattr(occ_state, 'distress'):
            occ_state.distress = min(1.0, occ_state.distress * (1.0 + 0.5 * severity))
        if hasattr(occ_state, 'disappointment'):
            occ_state.disappointment = min(1.0, occ_state.disappointment * (1.0 + 0.4 * severity))

        return occ_state
```

#### 步骤 6.2: 更新 PTSD 病理模块

修改 `PTSDPathology` 类：

```python
class PTSDPathology(Pathology):
    """
    创伤后应激障碍模式 - OCC 增强版

    新逻辑:
    - 触发条件增加恐惧/苦恼情绪感知
    - 闪回时扭曲 OCC 情绪状态
    """

    # ... 现有代码保持不变 ...

    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        # 原有逻辑 + OCC 恐惧/苦恼触发
        occ_state = emotional_state.get("occ_state")
        if occ_state:
            if isinstance(occ_state, dict):
                fear_trigger = occ_state.get("fear", 0) > 0.5
            else:
                fear_trigger = occ_state.fear > 0.5
            if fear_trigger:
                return True

        return len(self.trauma_memories) > 0

    def distort_occ(self, occ_state, severity: float):
        """PTSD 闪回时的情绪扭曲

        闪回特征：
        - 恐惧和苦恼被强制唤醒
        - 积极情绪被压制
        """
        if not occ_state:
            return occ_state

        # 放大恐惧和苦恼
        if hasattr(occ_state, 'fear'):
            occ_state.fear = min(1.0, occ_state.fear + 0.5 * severity)
        if hasattr(occ_state, 'distress'):
            occ_state.distress = min(1.0, occ_state.distress + 0.4 * severity)

        # 压制积极情绪
        occ_state.joy *= (1.0 - 0.8 * severity)
        occ_state.happiness *= (1.0 - 0.7 * severity)
        occ_state.satisfaction *= (1.0 - 0.6 * severity)

        return occ_state
```

#### 步骤 6.3: 更新 HSP 病理模块

修改 `HSPPathology` 类：

```python
class HSPPathology(Pathology):
    """
    高敏感人格模式 - OCC 增强版

    新逻辑:
    - 放大所有 OCC 情绪的感知强度
    """

    # ... 现有代码保持不变 ...

    def distort_occ(self, occ_state, severity: float):
        """放大所有情绪

        高敏感人群的特征：
        - 情绪阈值低，容易被触发
        - 情绪强度大，反应更强烈
        """
        if not occ_state:
            return occ_state

        amplify = 1.0 + severity

        # 放大所有情绪强度
        for key in occ_state.to_dict().keys():
            current = getattr(occ_state, key, 0)
            if current > 0.05:  # 低阈值
                setattr(occ_state, key, min(1.0, current * amplify))

        return occ_state
```

---

### 阶段 7: 记忆存储增强

#### 步骤 7.1: 更新存储方法

**文件**: `limbic_flow/pipeline/__init__.py`

修改 `_store_memory()` 方法：

```python
def _store_memory(self, state: CognitiveState):
    """存储交互记忆"""
    memory = {
        "vector": state.query_vector.tolist() if state.query_vector is not None else [],
        "pad": {
            "pleasure": state.pad_vector.get('pleasure', 0.0),
            "arousal": state.pad_vector.get('arousal', 0.0),
            "dominance": state.pad_vector.get('dominance', 0.0)
        },
        "timestamp": state.timestamp,
        "user_input": state.user_input,
        "system_response": state.final_response_text,
        "emotional_state": {
            "pleasure": state.pad_vector.get('pleasure', 0.0),
            "arousal": state.pad_vector.get('arousal', 0.0),
            "dominance": state.pad_vector.get('dominance', 0.0),
            "dopamine": state.neurotransmitters.get('dopamine', 0.5),
            "cortisol": state.neurotransmitters.get('cortisol', 0.3)
        },
        # 新增: OCC 情绪快照
        "occ_state": state.occ_state.to_dict() if state.occ_state else None,
        "dominant_emotion": state.dominant_emotion,
        "emotion_intensity": state.emotion_intensity,
        "user_info": self.user_info.copy(),
        "narrative": f"用户说: '{state.user_input[:50]}...'，系统回应: '{state.final_response_text[:50]}...'"
    }

    try:
        self.hippocampus.store_memory(memory)
    except Exception:
        pass
```

---

## 7. 文件修改清单

| 序号 | 文件路径 | 操作类型 | 说明 |
|------|----------|----------|------|
| 1 | `core/emotion/occ.py` | 修改 | 修复 typo + 添加 OCCHalfLifeConfig + OCCToPADProjector + decay_differential() |
| 2 | `core/emotion/appraiser.py` | **新建** | LLMAppraiser (LLM 驱动的认知评估) |
| 3 | `core/emotion/__init__.py` | 修改 | 导出新增的 OCC 组件 |
| 4 | `core/types.py` | 修改 | +4 OCC 字段: appraisal, occ_state, dominant_emotion, emotion_intensity |
| 5 | `pipeline/__init__.py` | 修改 | 重写 _perception() + OCC 集成 + 病理 OCC 扭曲 |
| 6 | `pipeline/config.py` | 修改 | 新增 OCC 相关配置项 |
| 7 | `core/brain/prompt_builder.py` | 修改 | _build_occ_style_guide() + build_system_prompt() 增强 |
| 8 | `middleware/pathology/classic.py` | 修改 | 4 个病理类新增 distort_occ() + OCC 触发条件 |
| 9 | `utils/emotion_analyzer.py` | 可选 | 可选：添加 OCC → EmotionLabel 映射 |

---

## 8. 新数据结构定义

### 8.1 Appraisal

```python
@dataclass
class Appraisal:
    """认知评估结果

    OCC 模型的核心：评估决定情绪
    """
    # 事件评估
    desirability: float = 0.0         # 期望程度 [-1, 1]
    desirability_for_other: float = 0.0  # 对他人的期望
    praiseworthiness: float = 0.0   # 值不值得称赞 [-1, 1]
    attractiveness: float = 0.0     # 吸引力 [-1, 1]

    # 评估维度
    likelihood: float = 0.5          # 可能性 [0, 1]
    expectedness: float = 0.5        # 预期性 [0, 1]

    # 因果归因
    causal_attribution_self: float = 0.0   # 归因自己 [-1, 1]
    causal_attribution_other: float = 0.0   # 归因他人 [-1, 1]

    # 结果
    realized: bool = True             # 是否已发生
    goal_relevant: bool = True       # 与目标相关
```

### 8.2 OCCState

```python
@dataclass
class OCCState:
    """OCC 情绪状态

    每种情绪的强度值 [0, 1]
    """
    # 主要情绪
    hope: float = 0.0
    joy: float = 0.0
    satisfaction: float = 0.0
    relief: float = 0.0
    disappointment: float = 0.0
    fear: float = 0.0

    # 自我情绪
    pride: float = 0.0
    shame: float = 0.0
    self_pride: float = 0.0
    self_shame: float = 0.0

    # 他人情绪
    admiration: float = 0.0
    reproach: float = 0.0
    gratitude: float = 0.0
    anger: float = 0.0

    # 复合情绪
    love: float = 0.0
    hate: float = 0.0
    distress: float = 0.0
    sadness: float = 0.0
    happiness: float = 0.0

    def to_dict(self) -> Dict[str, float]: ...
    def get_dominant(self) -> str: ...
    def get_intensity(self) -> float: ...
```

### 8.3 OCCHalfLifeConfig

```python
@dataclass
class OCCHalfLifeConfig:
    """OCC 情绪的差异化半衰期配置"""
    anger: float = 900          # 15分钟
    surprise: float = 600       # 10分钟
    fear: float = 1200          # 20分钟
    joy: float = 3600          # 1小时
    sadness: float = 5400       # 1.5小时
    love: float = 86400         # 24小时
    hate: float = 43200         # 12小时
    pride: float = 7200         # 2小时
    shame: float = 14400        # 4小时
    # ... 更多情绪配置

    def get(self, emotion_name: str) -> float: ...
```

### 8.4 CognitiveState 新增字段

```python
@dataclass
class CognitiveState:
    # ... 现有字段 ...

    # 新增字段
    appraisal: Optional[Appraisal] = None
    occ_state: Optional[OCCState] = None
    dominant_emotion: str = "neutral"
    emotion_intensity: float = 0.0
```

---

## 9. 代码示例

### 9.1 LLM Appraiser 使用示例

```python
from limbic_flow.core.ai import LLMFactory
from limbic_flow.core.emotion.appraiser import LLMAppraiser
from limbic_flow.core.emotion.occ import Appraisal

# 创建 LLM
factory = LLMFactory()
llm = factory.create_llm("openai")

# 创建评估器
appraiser = LLMAppraiser(llm)

# 评估用户输入
appraisal = appraiser.appraise("我今天被老板骂了，感觉很委屈")
# Appraisal(
#     desirability=-0.6,
#     praiseworthiness=0.0,
#     causal_attribution_other=0.8,
#     ...
# )

# 规则引擎回退
appraisal2 = appraiser.appraise("开心")
# Appraisal(
#     desirability=0.7,
#     realized=True,
#     ...
# )
```

### 9.2 OCC 引擎使用示例

```python
from limbic_flow.core.emotion.occ import OCCEngine, OCCHalfLifeConfig

# 创建引擎
engine = OCCEngine()

# 评估事件，产生情绪
event = {
    "type": "event",
    "desirability": 0.7,
    "likelihood": 0.8,
    "realized": True,
}
state = engine.appraise(event)

print(state.joy)        # 0.7
print(state.hope)       # 0.56
print(state.get_dominant())  # "joy"

# 差异化衰减
import time
time.sleep(60)  # 60秒后
engine.decay_differential(60, OCCHalfLifeConfig())
print(state.joy)  # 0.688... (1小时后约0.35)
```

### 9.3 OCC → PAD 投影示例

```python
from limbic_flow.core.emotion.occ import OCCState, OCCToPADProjector

# 创建 OCC 状态
occ_state = OCCState(
    joy=0.7,
    fear=0.3,
    anger=0.2
)

# 投影到 PAD
pad_vector = OCCToPADProjector.project(occ_state)
print(pad_vector)
# {
#     'pleasure': 0.41,   # joy(0.7*0.8) + fear(-0.6*0.3) + anger(-0.5*0.2)
#     'arousal': 0.34,    # joy(0.7*0.3) + fear(0.7*0.3) + anger(0.7*0.2)
#     'dominance': 0.05    # joy(0.7*0.2) + fear(-0.6*0.3) + anger(0.5*0.2)
# }

# 投影神经递质
nt = OCCToPADProjector.project_neurotransmitters(occ_state)
print(nt)
# {
#     'dopamine': 0.71,   # 0.5 + joy*0.3 + hope*0.2
#     'cortisol': 0.39    # 0.3 + fear*0.3 + anger*0.25
# }
```

### 9.4 Pipeline 使用示例

```python
from limbic_flow.pipeline import LimbicFlowPipeline
from limbic_flow.pipeline.config import PipelineConfig

# 创建 Pipeline
config = PipelineConfig()
config.enable_depression = True
pipeline = LimbicFlowPipeline(config=config)

# 处理输入
for action in pipeline.process_input("我今天考试通过了，好开心！"):
    print(action.type, action.payload)
    # 可能输出:
    # text 你太棒了！我就知道你肯定可以的！
    # emotion joy
    # state dominant_emotion=joy, intensity=0.8

# 检查 OCC 状态
print(pipeline.amygdala.get_current_state())
# EmotionalState(
#     pleasure=0.65,
#     arousal=0.25,
#     ...
# )
```

---

## 10. 配置变更

### 10.1 PipelineConfig 新增字段

**文件**: `limbic_flow/pipeline/config.py`

```python
@dataclass
class PipelineConfig:
    # ... 现有字段 ...

    # 新增: OCC 配置
    use_llm_appraisal: bool = True
    """是否使用 LLM 进行认知评估

    设为 False 时回退到规则引擎，提升性能但降低语义理解精度
    """

    occ_half_life_config: Dict[str, float] = None
    """OCC 情绪半衰期配置

    可按需覆盖默认配置:
    {
        "joy": 3600,
        "anger": 900,
        "sadness": 5400,
        ...
    }
    """

    @staticmethod
    def relaxed() -> "PipelineConfig":
        """放松型配置"""
        config = PipelineConfig()
        config.use_sensitive_emotion = False
        config.enable_depression = False
        config.enable_hsp = False
        config.use_llm_appraisal = True
        return config

    @staticmethod
    def sensitive() -> "PipelineConfig":
        """敏感型配置"""
        config = PipelineConfig()
        config.use_sensitive_emotion = True
        config.enable_depression = True
        config.enable_hsp = True
        config.use_llm_appraisal = True
        config.occ_half_life_config = {
            "anger": 600,    # 更短
            "joy": 1800,     # 更短
            "fear": 600,     # 更短
        }
        return config
```

### 10.2 环境变量新增

在 `.env.example` 中添加：

```bash
# OCC 评估配置
USE_LLM_APPRAISAL=true  # 是否使用 LLM 评估（设为 false 提升性能）

# OCC 半衰期（秒）
OCC_HALF_LIFE_JOY=3600
OCC_HALF_LIFE_ANGER=900
OCC_HALF_LIFE_SADNESS=5400
OCC_HALF_LIFE_FEAR=1200
OCC_HALF_LIFE_LOVE=86400
```

---

## 11. 测试策略

### 11.1 单元测试

#### 测试 1: OCCEngine 基础功能

```python
# tests/test_occ_engine.py

def test_occ_engine_joy():
    engine = OCCEngine()
    event = {"type": "event", "desirability": 0.8, "realized": True}
    state = engine.appraise(event)
    assert state.joy > 0.7
    assert state.get_dominant() == "joy"

def test_occ_engine_fear():
    engine = OCCEngine()
    event = {"type": "event", "desirability": -0.6, "likelihood": 0.7, "realized": False}
    state = engine.appraise(event)
    assert state.fear > 0.3

def test_occ_differential_decay():
    import time
    engine = OCCEngine()
    engine.state.joy = 1.0

    # 1小时后的衰减因子: e^(-ln(2) * 3600 / 3600) = 0.5
    engine.decay_differential(3600, OCCHalfLifeConfig())
    assert 0.49 < engine.state.joy < 0.51

def test_occ_to_pad_projection():
    occ = OCCState(joy=0.8, fear=0.3)
    pad = OCCToPADProjector.project(occ)
    assert pad["pleasure"] > 0  # joy 的贡献大于 fear
    assert pad["arousal"] > 0   # 两者都贡献 arousal
```

#### 测试 2: LLMAppraiser

```python
# tests/test_appraiser.py

def test_rule_based_appraise():
    llm = MockLLM()  # 模拟 LLM 失败
    appraiser = LLMAppraiser(llm)

    appraisal = appraiser._rule_based_appraise("我很开心")
    assert appraisal.desirability > 0.5
    assert appraisal.realized == True

def test_llm_appraise_fallback():
    llm = MockLLM(raise_exception=True)
    appraiser = LLMAppraiser(llm)

    appraisal = appraiser.appraise("测试输入")
    # 应该回退到规则引擎
    assert appraisal is not None
```

#### 测试 3: 病理模块 OCC 扭曲

```python
# tests/test_pathology_occ.py

def test_depression_distort_occ():
    pathology = DepressionPathology(base_severity=0.5)
    occ = OCCState(joy=0.8, sadness=0.2)

    result = pathology.distort_occ(occ, 0.5)
    assert result.joy < 0.4   # 被压低
    assert result.sadness > 0.2  # 被放大

def test_ptsd_distort_occ():
    pathology = PTSDPathology(severity=0.5)
    occ = OCCState(joy=0.8, fear=0.1)

    result = pathology.distort_occ(occ, 0.5)
    assert result.fear > 0.5  # 被放大
    assert result.joy < 0.2   # 被压制
```

### 11.2 集成测试

#### 测试: 完整 Pipeline

```python
# tests/test_pipeline_occ.py

def test_pipeline_with_occ():
    pipeline = LimbicFlowPipeline()

    # 处理输入
    actions = list(pipeline.process_input("我今天被表扬了，好开心！"))

    # 验证输出
    text_actions = [a for a in actions if a.type == "text"]
    assert len(text_actions) > 0

    # 验证 OCC 状态被记录
    state = pipeline.amygdala.get_current_state()
    assert state.pleasure > 0  # 应该有愉悦度

    # 验证主导情绪
    # (需要添加获取 OCC 状态的接口)
```

---

## 12. 风险与缓解

### 12.1 性能风险

| 风险 | 描述 | 缓解措施 |
|------|------|----------|
| LLM 评估延迟 | 每次输入都调用 LLM 可能导致延迟增加 | 提供 `use_llm_appraisal` 开关，回退到规则引擎 |
| 双重计算 | OCC 和 PAD 两套计算可能增加 CPU | PAD 计算很轻量，主要开销在 LLM |
| 内存占用 | OCC 状态 22 个浮点数 | 影响可忽略 |

**性能基准**:
- 当前 Pipeline: ~200ms
- OCC 规则引擎版: ~220ms
- OCC LLM 版: ~800ms (取决于 LLM 延迟)

### 12.2 功能风险

| 风险 | 描述 | 缓解措施 |
|------|------|----------|
| LLM JSON 解析失败 | LLM 可能返回非标准 JSON | 规则引擎兜底 |
| OCC → PAD 映射不准 | 投影可能不符合预期 | 映射矩阵可配置化 |
| 向下不兼容 | 可能破坏现有功能 | PAD 保持完整，接口不变 |

### 12.3 调试复杂性

| 风险 | 描述 | 缓解措施 |
|------|------|----------|
| 情绪溯源困难 | OCC 层级增加，追踪困难 | 完善日志，记录每层输入输出 |
| Prompt 调试 | OCC 风格指南可能不准确 | 提供调试模式，输出生成的所有 prompt |

---

## 13. 时间线与里程碑

### 13.1 阶段规划

| 阶段 | 内容 | 预计工作量 | 依赖 |
|------|------|------------|------|
| Phase 1 | OCC 引擎修复 + 增强 | 1 天 | - |
| Phase 2 | LLM Appraiser 实现 | 2 天 | Phase 1 |
| Phase 3 | CognitiveState 扩展 | 0.5 天 | Phase 1 |
| Phase 4 | Pipeline 集成 | 2 天 | Phase 2, 3 |
| Phase 5 | PromptBuilder 增强 | 1 天 | Phase 4 |
| Phase 6 | 病理模块 OCC 感知 | 1.5 天 | Phase 4 |
| Phase 7 | 记忆存储增强 | 0.5 天 | Phase 4 |
| Phase 8 | 测试 + 调试 | 3 天 | 全阶段 |
| **总计** | | **11.5 天** | |

### 13.2 里程碑

- **M1 (Day 1)**: OCC 引擎修复完成，typo 修复，配置类就绪
- **M2 (Day 3)**: LLM Appraiser 就绪，可独立测试
- **M5 (Day 7)**: Pipeline 集成完成，端到端可运行
- **M7 (Day 9)**: 病理模块 OCC 感知完成
- **M8 (Day 12)**: 测试通过，文档完成

---

## 14. 附录

### 14.1 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| OCC | Ortony, Clore, Collins | 认知情绪模型 |
| PAD | Pleasure-Arousal-Dominance | 维度情绪模型 |
| Appraisal | - | 认知评估结果 |
| 半衰期 | Half-life | 情绪衰减到一半的时间 |
| 投影 | Projection | OCC 到 PAD 的数值映射 |

### 14.2 参考资料

1. Ortony, A., Clore, G. L., & Collins, A. (1988). *The Cognitive Structure of Emotions*. Cambridge University Press.
2. Mehrabian, A. (1996). *Pleasure-Arousal-Dominance: A general measure of emotion*. Motivation and Emotion.
3. Picard, R. W. (1997). *Affective Computing*. MIT Press.

### 14.3 相关文档

- [架构文档](architecture.md)
- [API 模块文档](AI_MODULE.md)
- [MotorCortex 文档](MOTOR_CORTEX.md)

---

*文档结束*
