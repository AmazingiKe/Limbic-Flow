# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Limbic-Flow** 是一个计算精神病学引擎，模拟人类认知的不完美性。通过数学情感模型（PAD）和噪声注入的 RAG 中间件，在向量数据库环境中模拟情感衰减、记忆扭曲和病理特征。

- **Language**: Python 3.10+
- **Framework**: FastAPI + Uvicorn
- **Status**: Active Research & Development (Conceptual Architecture Phase)
- **Author**: Amazing_ike (灯光师 & TD Pipeline)

---

## Core Architecture

### 生物学隐喻架构 (Neuromorphic Design)

```
Input → Perception → Amygdala → Hippocampus → Pathology Middleware
       → Brain (Cognition) → MotorCortex → Output (ActionEvents)
```

**六个核心器官**:

1. **Brain** (`limbic_flow.core.brain.processor.Brain`)
   - 职责: 认知思考，根据情绪和记忆生成文本响应
   - 输入: 扭曲记忆 + 当前情绪状态 + 语义知识
   - 输出: 系统回应文本
   - 支持多个 LLM 提供商（OpenAI、Anthropic、DeepSeek、Ollama）

2. **Amygdala** (`limbic_flow.core.amygdala.Amygdala`)
   - 职责: 杏仁核，情绪状态管理与化学反应
   - 核心机制: PAD 模型（Pleasure、Arousal、Dominance）+ 神经递质（多巴胺、皮质醇）
   - 数据存储: SQLite (`amygdala.db`)
   - 特性: 半衰期衰减（情绪随时间自动衰退）

3. **Hippocampus** (`limbic_flow.core.hippocampus.FileHippocampus`)
   - 职责: 海马体，记忆存储与检索
   - 当前实现: JSON 文件存储 (`memory_store.json`)
   - 未来: 向量数据库（Chroma/Milvus）
   - 存储内容: 情景记忆、事件向量、时间戳、PAD 值

4. **PathologyMiddleware** (`limbic_flow.middleware.pathology`)
   - 职责: 病理中间件，扭曲记忆查询和记忆重构
   - 模块化设计: 支持多种病理模式
   - **抑郁模式**: 降低 Pleasure，屏蔽快乐记忆
   - **阿尔兹海默模式**: 高斯噪声注入、时间权重反转
   - **PTSD 模式**: 创伤记忆强制触发
   - **HSP 模式（高敏感性）**: 感觉信号放大

5. **MotorCortex** (`limbic_flow.core.articulation.motor_cortex.MotorCortex`)
   - 职责: 运动表达，将文本转换为分段动作流
   - 输出: ActionEvent 队列（支持流式输出）
   - 特性: 可配置的 WPM（Words Per Minute）

6. **Neocortex** (`limbic_flow.core.neocortex.MockNeocortex`)
   - 职责: 新皮层，语义知识存储（当前为 Mock）
   - 未来: 图数据库（Neo4j）

### Pipeline 数据流

`LimbicFlowPipeline` (`limbic_flow.pipeline.__init__.py`) 是认知总线调度器，协调器官间的数据流：

```
1. perception()          → 提取向量、计算初始 PAD 冲击
2. amygdala.process()    → 计算神经递质、更新情绪衰减
3. pathology_middleware  → 扭曲查询向量
4. hippocampus.retrieve_memories() → 检索记忆
5. pathology_middleware.process()  → 扭曲记忆内容
6. brain.process()       → 生成回应文本
7. motor_cortex.process() → 转换为动作流
8. hippocampus.store_memory() → 闭环存储
```

---

## Development Commands

### Setup

```bash
# 安装项目及开发依赖
pip install -e ".[dev]"

# 或使用 requirements.txt（不推荐，仅备用）
pip install -r requirements.txt
```

### Running

```bash
# 启动 API 服务器（开发模式，自动热加载）
uvicorn limbic_flow.api.main:app --reload --host 0.0.0.0 --port 8000

# 或直接运行
python -m limbic_flow.api.main
```

### Testing

```bash
# 运行全部测试
pytest -v

# 运行单个测试文件
pytest tests/test_emotion_engine.py -v

# 运行特定测试函数
pytest tests/test_emotion_engine.py::test_pad_decay -v

# 运行测试并显示覆盖率
pytest --cov=limbic_flow tests/
```

### Code Quality

```bash
# Linting（自动修复）
ruff check . --fix

# 代码格式化
black limbic_flow tests

# Type checking
mypy limbic_flow --ignore-missing-imports
```

---

## Configuration

### Environment Variables (`.env`)

详见 `.env.example`，关键配置：

```bash
# LLM 提供商选择
DEFAULT_LLM_PROVIDER=mock  # openai | anthropic | deepseek | ollama | mock

# LLM API Keys（按需填写）
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
DEEPSEEK_API_KEY=...

# API 服务器
API_HOST=0.0.0.0
API_PORT=8000

# 情绪引擎半衰期参数（秒）
HALF_LIFE_PLEASURE=3600
HALF_LIFE_AROUSAL=1800
HALF_LIFE_DOMINANCE=2700
HALF_LIFE_DOPAMINE=300
HALF_LIFE_CORTISOL=600
```

### Pipeline Configuration

`limbic_flow.pipeline.config.PipelineConfig` 中的关键配置项：

```python
use_sensitive_emotion: bool        # 是否使用敏感人格配置
enable_depression: bool            # 启用抑郁模式
enable_alzheimer: bool             # 启用阿尔兹海默模式
enable_ptsd: bool                  # 启用 PTSD 模式
enable_hsp: bool                   # 启用高敏感性模式
memory_limit: int                  # 每次检索的记忆数量
llm_provider: str                  # LLM 提供商
```

---

## Key Data Types

### CognitiveState (`limbic_flow.core.types.CognitiveState`)

核心状态对象，贯穿整个 Pipeline：

```python
class CognitiveState:
    user_input: str                    # 用户输入
    query_vector: np.ndarray           # 语义向量（1536D）
    pad_vector: Dict[str, float]       # 情绪向量 {pleasure, arousal, dominance}
    neurotransmitters: Dict[str, float] # 神经递质 {dopamine, cortisol}
    memories: List[Dict]               # 检索到的记忆
    final_response_text: str           # 最终回应文本
    action_queue: List[ActionEvent]    # 动作队列
    context: Dict[str, Any]            # 上下文（用户信息、语义知识等）
    timestamp: float                   # 时间戳
```

### ActionEvent (`limbic_flow.core.articulation.action_event.ActionEvent`)

动作事件，由 MotorCortex 生成，通过 SSE 流式返回：

```python
class ActionEvent:
    type: str                  # "text" | "emotion" | "memory" | "state"
    payload: str              # 事件内容
    timestamp: float          # 时间戳
```

### EmotionalState (`limbic_flow.core.amygdala.decay.EmotionalState`)

情绪状态快照，存储在 Amygdala（SQLite）：

```python
class EmotionalState:
    pleasure: float
    arousal: float
    dominance: float
    dopamine: float
    cortisol: float
    timestamp: float
```

---

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/process` | 同步处理输入，返回完整的 ActionEvent 列表 |
| `POST` | `/process/stream` | 异步流式处理，SSE 输出 |
| `GET` | `/health` | 健康检查 |

### Emotion Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/emotion/current` | 获取当前情绪状态 |
| `GET` | `/emotion/history` | 获取情绪历史记录 |
| `POST` | `/emotion/reset` | 重置情绪状态（清空历史） |

### Configuration Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/config` | 获取当前配置 |
| `POST` | `/config` | 切换人格与病理模式 |
| `POST` | `/llm-config` | 更新 LLM 配置与提供商 |

---

## Common Development Tasks

### 1. 调整情绪衰减参数

编辑 `.env` 中的 `HALF_LIFE_*` 参数，或在 `limbic_flow.core.config.HalfLifeConfig` 中配置。

半衰期越短，情绪恢复越快；越长，情绪持续越久。

### 2. 添加新的病理模式

1. 在 `limbic_flow.middleware.pathology` 中创建新的 Pathology 类（继承 `BasePathology`）
2. 实现 `distort_query()` 和 `process()` 方法
3. 在 `create_pathology_middleware()` 中注册新模式

**示例**:
```python
class MyPathology(BasePathology):
    def distort_query(self, query_vector, emotional_state):
        # 扭曲查询
        return distorted_vector

    def process(self, state: CognitiveState):
        # 重构记忆
        return state
```

### 3. 集成不同的 LLM 提供商

1. 在 `limbic_flow.core.ai.factory.LLMFactory` 中检查支持的提供商
2. 创建对应的 Adapter（参见 `limbic_flow.core.ai.adapters`）
3. 在环境变量或 API 调用时指定 `provider`

### 4. 替换存储后端

- **Hippocampus**: 从 `FileHippocampus` 替换为向量数据库（Chroma、Milvus）
- **Amygdala**: 可扩展为其他数据库（PostgreSQL、MongoDB）
- **Neocortex**: 从 `MockNeocortex` 替换为实际的图数据库（Neo4j）

接口保持不变，便于无缝切换。

---

## Code Organization

```
limbic_flow/
├── api/
│   └── main.py              # FastAPI 应用
├── core/
│   ├── brain/               # 认知处理器
│   ├── amygdala/            # 情绪管理（SQLite）
│   ├── hippocampus/         # 记忆存储（JSON/向量DB）
│   ├── articulation/        # 动作生成（MotorCortex）
│   ├── ai/
│   │   ├── adapters/        # LLM 适配器（OpenAI、Anthropic 等）
│   │   ├── factory.py       # LLM 工厂
│   │   └── embedding.py     # 嵌入服务
│   ├── emotion/             # PAD 模型基础
│   ├── neocortex/           # 语义知识存储（当前 Mock）
│   ├── location/            # 地理位置与时间信息
│   ├── config.py            # 全局配置
│   └── types.py             # 核心数据类型
├── middleware/
│   └── pathology/           # 病理中间件（模块化）
├── pipeline/
│   ├── __init__.py          # LimbicFlowPipeline（核心调度器）
│   └── config.py            # Pipeline 配置
├── utils/
│   ├── logger.py            # 日志
│   ├── event_bus.py         # 事件总线（可选）
│   ├── emotion_analyzer.py  # 情绪分析工具
│   └── ...
└── tools/
    └── emotion_chat.py      # 聊天工具（支持历史持久化）

tests/                        # 单元测试与集成测试
```

---

## Architectural Decisions

### 为什么采用生物学隐喻？

- 提高可理解性: 开发者能快速理解各组件的"角色"
- 增强可扩展性: 新增器官（如Cerebellum）不会破坏现有架构
- 支持模块化: 各器官独立实现接口，便于替换

### 为什么 Pipeline 中存储 user_info？

为了模拟"记忆中的个人信息"：系统能从历史交互中提取用户名字、偏好等，自动注入到上下文中。

### 为什么有两层"情绪"？

- **Amygdala**: 生理情绪曲线（实时状态、衰减）
- **PathologyMiddleware**: 认知扭曲（记忆如何被感知）

二者结合模拟："我在抑郁状态，所以看到的世界是灰色的"。

---

## Testing Guidelines

- 新增功能必须附带单测（≥80% 覆盖率）
- 病理模块测试: 验证扭曲前后的差异
- Pipeline 集成测试: 测试完整的输入→输出流程
- Mock 对象: 使用 `MockNeocortex` 和 `MockLLM` 隔离外部依赖

---

## Debugging Tips

### 查看完整的认知状态

在 `Pipeline.process_input_stream()` 中添加日志：
```python
self.logger.info(f"State after brain: {state.pad_vector}, neurotransmitters: {state.neurotransmitters}")
```

### 诊断病理模式

检查 `state.raw_memories` vs `state.memories`，对比扭曲前后的差异。

### 性能分析

使用 `cProfile`:
```bash
python -m cProfile -s cumtime -m limbic_flow.api.main > profile.txt
```

---

## Known Limitations & Future Work

1. **Hippocampus**: 当前为文件存储，大规模数据会性能下降
2. **Neocortex**: 当前为 Mock，缺乏真实语义知识图谱
3. **LLM 流式输出**: 需要优化 token-level streaming
4. **多并发**: SQLite 并发写入限制，未来需迁移到 PostgreSQL

---

## References

- [Architecture Doc](docs/architecture.md)
- [PAD Model](https://en.wikipedia.org/wiki/PAD_emotional_dimension)
- [Half-Life Decay](https://en.wikipedia.org/wiki/Half-life)
- [RAG Pattern](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

---

**Last Updated**: 2026-03-09
