# Limbic-Flow AI 模块文档

## 📖 概述

`core/ai` 模块是 Limbic-Flow 的 LLM 抽象层，提供统一的接口来调用多种大语言模型（LLM）。该模块遵循**依赖倒置原则**和**开闭原则**，实现了高度解耦、可维护、可扩展的架构。

## 🏗️ 架构设计

### 目录结构

```
core/ai/
├── __init__.py          # 模块导出
├── base.py              # LLM 抽象基类
├── factory.py           # LLM 工厂类
└── adapters/            # 各厂商适配器
    ├── __init__.py
    ├── openai.py        # OpenAI 适配器
    ├── deepseek.py      # DeepSeek 适配器
    ├── anthropic.py     # Anthropic 适配器
    └── ollama.py        # Ollama 适配器
```

### 核心组件

#### 1. **BaseLLM（抽象基类）**

定义了所有 LLM 适配器必须实现的接口：

```python
class BaseLLM(ABC):
    @abstractmethod
    def chat(self, messages: List[Message], **kwargs) -> LLMResponse:
        """聊天接口 - 核心方法"""
        pass
```

**主要方法：**
- `chat()`: 多轮对话接口
- `chat_simple()`: 简化的单轮对话接口
- `health_check()`: 健康检查

#### 2. **LLMFactory（工厂类）**

负责创建和管理 LLM 实例：

```python
factory = LLMFactory()
llm = factory.create_llm("openai")
```

**主要方法：**
- `create_llm()`: 创建 LLM 实例
- `register_llm()`: 注册新的 LLM 提供商
- `get_supported_providers()`: 获取支持的提供商列表

#### 3. **适配器（Adapters）**

每个适配器负责对接一个厂商的 API：

- **OpenAILLM**: 支持 GPT-4、GPT-3.5-turbo
- **DeepSeekLLM**: 支持 deepseek-chat、deepseek-coder
- **AnthropicLLM**: 支持 Claude 3 系列
- **OllamaLLM**: 支持所有 Ollama 模型（本地运行）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -e .
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入 API Keys：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# DeepSeek
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat

# 默认提供商
DEFAULT_LLM_PROVIDER=openai
```

### 3. 基本使用

```python
from limbic_flow.core.ai import LLMFactory

# 创建工厂实例
factory = LLMFactory()

# 创建 LLM 实例（使用默认提供商）
llm = factory.create_llm()

# 发送消息
response = llm.chat_simple("你好！")
print(response.content)
```

### 4. 指定提供商

```python
# 使用 OpenAI
openai_llm = factory.create_llm("openai")

# 使用 DeepSeek
deepseek_llm = factory.create_llm("deepseek")

# 使用 Anthropic
anthropic_llm = factory.create_llm("anthropic")

# 使用 Ollama（本地）
ollama_llm = factory.create_llm("ollama")
```

## 📚 API 参考

### LLMConfig

LLM 配置类：

```python
@dataclass
class LLMConfig:
    model: str                      # 模型名称
    api_key: Optional[str] = None   # API Key
    base_url: Optional[str] = None  # API 基础 URL
    temperature: float = 0.7        # 温度参数
    max_tokens: Optional[int] = None # 最大 token 数
    timeout: int = 30               # 超时时间（秒）
    extra_params: Optional[Dict[str, Any]] = None  # 额外参数
```

### Message

消息类：

```python
@dataclass
class Message:
    role: MessageRole    # 消息角色（SYSTEM, USER, ASSISTANT）
    content: str         # 消息内容
```

### LLMResponse

LLM 响应类：

```python
@dataclass
class LLMResponse:
    content: str                        # 响应内容
    model: str                          # 使用的模型
    usage: Optional[Dict[str, int]]    # Token 使用情况
    raw_response: Optional[Dict[str, Any]]  # 原始响应
```

## 🔧 高级用法

### 1. 多轮对话

```python
from limbic_flow.core.ai import LLMFactory, Message, MessageRole

factory = LLMFactory()
llm = factory.create_llm("openai")

messages = [
    Message(role=MessageRole.SYSTEM, content="你是一个有帮助的助手。"),
    Message(role=MessageRole.USER, content="什么是 Python？"),
    Message(role=MessageRole.ASSISTANT, content="Python 是一种编程语言..."),
    Message(role=MessageRole.USER, content="它有什么特点？"),
]

response = llm.chat(messages)
print(response.content)
```

### 2. 自定义参数

```python
response = llm.chat_simple(
    prompt="写一个故事",
    temperature=0.9,      # 更有创意
    max_tokens=1000       # 更长的输出
)
```

### 3. 注册新的 LLM 提供商

```python
from limbic_flow.core.ai import BaseLLM, LLMFactory, LLMConfig

class CustomLLM(BaseLLM):
    def _initialize_client(self):
        # 初始化你的客户端
        pass
    
    def chat(self, messages, **kwargs):
        # 实现聊天逻辑
        pass

# 注册新提供商
LLMFactory.register_llm("custom", CustomLLM)

# 使用新提供商
factory = LLMFactory()
custom_llm = factory.create_llm("custom")
```

### 4. 在 Limbic-Flow Pipeline 中使用

```python
from limbic_flow.pipeline import LimbicFlowPipeline

# 使用 OpenAI
pipeline = LimbicFlowPipeline(llm_provider="openai")

# 使用 DeepSeek
pipeline = LimbicFlowPipeline(llm_provider="deepseek")

# 处理输入
result = pipeline.process_input("我今天感觉很开心！")
print(result["response"])
```

## 🎯 支持的 LLM 提供商

| 提供商 | 模型 | 需要的配置 |
|--------|------|------------|
| OpenAI | gpt-4-turbo-preview, gpt-3.5-turbo | `OPENAI_API_KEY` |
| DeepSeek | deepseek-chat, deepseek-coder | `DEEPSEEK_API_KEY` |
| Anthropic | claude-3-opus-20240229, claude-3-sonnet-20240229 | `ANTHROPIC_API_KEY` |
| Ollama | llama2, mistral, codellama 等 | 无需 API Key（本地运行） |

## 🔒 安全最佳实践

1. **永远不要将 API Key 提交到版本控制系统**
   - 使用 `.env` 文件
   - 将 `.env` 添加到 `.gitignore`

2. **使用环境变量管理敏感信息**
   ```python
   import os
   api_key = os.getenv("OPENAI_API_KEY")
   ```

3. **在生产环境使用密钥管理服务**
   - AWS Secrets Manager
   - Azure Key Vault
   - HashiCorp Vault

## 🐛 故障排查

### 1. API Key 错误

```
ValueError: OpenAI API Key 不能为空
```

**解决方案**：检查 `.env` 文件中的 API Key 是否正确配置。

### 2. 连接超时

```
Exception: API 调用失败: timeout
```

**解决方案**：
- 检查网络连接
- 增加 `timeout` 参数
- 检查 API 基础 URL 是否正确

### 3. 模型不存在

```
Exception: Model not found
```

**解决方案**：检查模型名称是否正确，参考支持的模型列表。

## 📈 性能优化

1. **使用合适的模型**：
   - 简单任务使用较小的模型（如 gpt-3.5-turbo）
   - 复杂任务使用较大的模型（如 gpt-4-turbo-preview）

2. **调整温度参数**：
   - 创意任务使用较高的温度（0.8-1.0）
   - 精确任务使用较低的温度（0.1-0.3）

3. **限制输出长度**：
   - 设置合理的 `max_tokens` 以控制成本

## 🤝 贡献指南

如果你想要添加新的 LLM 提供商支持：

1. 在 `core/ai/adapters/` 目录下创建新的适配器文件
2. 继承 `BaseLLM` 类
3. 实现必需的方法
4. 在 `factory.py` 中注册新的提供商
5. 更新文档

## 📝 许可证

MIT License
