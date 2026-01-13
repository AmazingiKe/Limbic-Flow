# 运动皮层模块 (Motor Cortex / Articulation Core)

## 概述

运动皮层模块是 Limbic-Flow 架构中的表达核心，负责将 LLM 生成的完整文本转换为带有节奏感的动作流，模拟真人的打字速度、犹豫感和断句习惯。

### 生物学对应

- **运动皮层 (Motor Cortex)**: 负责语言产生的肌肉控制
- **布若卡氏区 (Broca's Area)**: 负责语言组织和表达

### 架构位置

```
LLM 表现层 → 运动皮层 → 最终输出接口
```

## 核心功能

### 1. 语义分段器 (The Segmenter)

将一大段话切碎为自然的语义块，支持：
- 按标点符号切分（句号、问号、感叹号等）
- 按逗号和逻辑连接词切分
- 长度启发式算法
- 情绪影响分段策略（犹豫状态切得更碎）

### 2. 节奏计算器 (The Rhythm Engine)

根据 PAD 情绪值计算打字速度和停顿时间：

- **Arousal (激活度)**: 
  - 高 (>0.5) → 打字快 (速度 x 1.5)
  - 低 (<0.0) → 打字慢 (速度 x 0.8)

- **Dominance (控制度)**:
  - 低 (不自信) → 发送前停顿更长
  - 高 (自信) → 发送前停顿更短

### 3. 动作队列 (The Action Queue)

输出不再是简单的 String，而是 Event List：

```python
[
  {"type": "typing", "duration": 1.5},  # 显示正在输入
  {"type": "message", "content": "我觉得..."}, # 发送第一段
  {"type": "wait", "duration": 2.0},          # 停顿（模拟思考/犹豫）
  {"type": "typing", "duration": 0.5},
  {"type": "message", "content": "还是算了吧。"} # 发送第二段
]
```

## 快速开始

### 基本使用

```python
from limbic_flow.core.articulation import MotorCortex

# 创建运动皮层实例
motor = MotorCortex(base_wpm=60)

# 输入文本和情绪状态
text = "那个，我其实不太想去，因为最近真的太累了...下次吧？"
pad_state = {"pleasure": -0.5, "arousal": 0.8, "dominance": -0.8}

# 生成动作流
actions = motor.articulate(text, pad_state)

# 执行动作流
for action in actions:
    if action.action_type.value == "message":
        print(action.content)
```

### 实时执行（带时间控制）

```python
from limbic_flow.core.articulation import create_articulation_executor

# 定义动作回调函数
def action_callback(action):
    action_type = action.action_type.value
    
    if action_type == "typing":
        print("[正在输入...]", end="", flush=True)
    elif action_type == "message":
        print(f"\n{action.content}", end="", flush=True)
    elif action_type == "wait":
        print("[...]", end="", flush=True)

# 创建执行器
executor = create_articulation_executor(
    action_callback=action_callback,
    enable_timing=True  # 启用时间控制
)

# 执行动作流
executor.execute(actions)
```

### 与情绪引擎集成

```python
from limbic_flow.core.articulation import MotorCortex
from limbic_flow.core.emotion_engine import EmotionEngine

# 创建情绪引擎和运动皮层
emotion_engine = EmotionEngine()
motor = MotorCortex(base_wpm=60)

# 更新情绪状态
emotion_engine.update(input_pleasure=0.3, input_arousal=0.5, input_dominance=-0.2)
emotion_state = emotion_engine.get_state()

# 转换为 PAD 格式
pad_state = {
    "pleasure": emotion_state["pleasure"],
    "arousal": emotion_state["arousal"],
    "dominance": emotion_state["dominance"]
}

# 生成动作流
text = "我觉得这个想法很有意思！"
actions = motor.articulate(text, pad_state)
```

## API 文档

### MotorCortex

运动皮层核心类，负责文本分段和节奏计算。

#### 构造函数

```python
MotorCortex(
    base_wpm: int = 60,
    min_segment_length: int = 2,
    max_segment_length: int = 30,
    hesitation_base: float = 0.5,
    hesitation_multiplier: float = 1.5
)
```

**参数:**
- `base_wpm`: 基础打字速度 (Words Per Minute)，默认 60 字/分钟
- `min_segment_length`: 最小分段长度（字符数），防止过度切分
- `max_segment_length`: 最大分段长度（字符数），防止分段过长
- `hesitation_base`: 基础犹豫时间（秒）
- `hesitation_multiplier`: 犹豫时间乘数，用于情绪调节

#### 主要方法

##### articulate()

```python
articulate(
    full_response_text: str,
    pad_state: Dict[str, float],
    metadata: Optional[Dict[str, Any]] = None
) -> List[ActionEvent]
```

核心接口：接收完整文本，返回动作流。

**参数:**
- `full_response_text`: LLM 生成的完整回复文本
- `pad_state`: PAD 情绪状态，包含 pleasure, arousal, dominance
- `metadata`: 额外的元数据（如调试信息）

**返回:**
- `List[ActionEvent]`: 动作事件列表

### ActionEvent

动作事件数据类，表示一个原子动作。

#### 属性

- `action_type`: 动作类型 (ActionType 枚举)
- `content`: 动作内容（如消息文本）
- `duration`: 持续时间（秒）
- `metadata`: 额外的元数据

#### 工厂方法

```python
# 创建正在输入动作
ActionEvent.create_typing(duration: float, metadata: Optional[Dict] = None)

# 创建发送消息动作
ActionEvent.create_message(content: str, metadata: Optional[Dict] = None)

# 创建等待动作
ActionEvent.create_wait(duration: float, metadata: Optional[Dict] = None)
```

#### 序列化方法

```python
# 转换为字典
event.to_dict() -> Dict[str, Any]

# 转换为 JSON
event.to_json() -> str

# 从字典创建
ActionEvent.from_dict(data: Dict[str, Any]) -> ActionEvent
```

### ActionType

动作类型枚举：

- `TYPING`: 显示正在输入状态
- `MESSAGE`: 发送消息内容
- `WAIT`: 等待/停顿
- `THINKING`: 思考状态（可选扩展）

### ArticulationExecutor

运动皮层执行器，负责协调 MotorCortex 和 StreamingOutput。

#### 构造函数

```python
ArticulationExecutor(
    action_callback: Callable[[ActionEvent], None],
    enable_timing: bool = True,
    enable_logging: bool = False
)
```

**参数:**
- `action_callback`: 动作回调函数，接收 ActionEvent
- `enable_timing`: 是否启用时间控制（模拟打字速度和停顿）
- `enable_logging`: 是否启用日志输出

#### 主要方法

```python
# 执行动作流
execute(actions: List[ActionEvent], metadata: Optional[Dict] = None) -> None

# 使用自定义回调执行动作流
execute_with_callback(
    actions: List[ActionEvent],
    callback: Callable[[ActionEvent], None],
    metadata: Optional[Dict] = None
) -> None
```

## 配置选项

### 分段策略

通过调整 `min_segment_length` 和 `max_segment_length` 可以控制分段粒度：

```python
# 精细分段（适合犹豫状态）
motor_fine = MotorCortex(
    min_segment_length=2,
    max_segment_length=15
)

# 粗略分段（适合自信状态）
motor_coarse = MotorCortex(
    min_segment_length=5,
    max_segment_length=50
)
```

### 节奏控制

通过调整 `base_wpm` 和 `hesitation_base` 可以控制整体节奏：

```python
# 快节奏（适合急躁状态）
motor_fast = MotorCortex(
    base_wpm=100,
    hesitation_base=0.3
)

# 慢节奏（适合慵懒状态）
motor_slow = MotorCortex(
    base_wpm=40,
    hesitation_base=0.8
)
```

## 情绪耦合示例

### 不同情绪状态下的表达

```python
motor = MotorCortex(base_wpm=60)
text = "我觉得这个方案还不错，可以考虑一下。"

# 冷静自信
state_calm = {"pleasure": 0.3, "arousal": 0.0, "dominance": 0.5}
actions_calm = motor.articulate(text, state_calm)

# 紧张焦虑
state_anxious = {"pleasure": -0.5, "arousal": 0.8, "dominance": -0.8}
actions_anxious = motor.articulate(text, state_anxious)

# 慵懒放松
state_relaxed = {"pleasure": 0.5, "arousal": -0.5, "dominance": 0.0}
actions_relaxed = motor.articulate(text, state_relaxed)
```

**效果对比:**

| 情绪状态 | 分段数 | 总时长 | 特征 |
|---------|--------|--------|------|
| 冷静自信 | 2 | 4.13s | 节奏平稳，停顿适中 |
| 紧张焦虑 | 2 | 3.14s | 打字快，停顿短 |
| 慵懒放松 | 2 | 5.07s | 打字慢，停顿长 |

## 测试

运行测试套件：

```bash
python test_motor_cortex.py
```

运行示例：

```bash
python example_motor_cortex.py
```

## 设计原则

1. **职责单一**: 不关心"说什么"（那是 LLM 的事），只关心"怎么发"
2. **情绪耦合**: PAD 情绪值直接影响输出节奏
3. **可配置**: 支持不同的分段策略和节奏参数
4. **可扩展**: 易于添加新的动作类型和分段策略
5. **解耦设计**: 以后如果想换 LLM 或语音输出（TTS），此模块完全不用动

## 架构影响

这个模块的加入，标志着架构从 "Request-Response" (一问一答) 模式，进化到了 "Streaming Interaction" (流式交互) 模式。

### 前端/客户端要求

UI 界面必须支持接收这种动作流，不能等到所有字都生成完了再显示。需要能实时显示"对方正在输入"。

### 解耦优势

- 换 LLM → 此模块不用动
- 换语音输出（TTS）→ 此模块不用动
- 只负责"节奏"，不关心内容

## 文件结构

```
limbic_flow/core/articulation/
├── __init__.py                 # 模块导出
├── action_event.py            # 动作事件数据模型
├── motor_cortex.py            # 运动皮层核心类
└── streaming_integration.py   # 与流式输出的集成
```

## 许可证

MIT License
