# 日志系统使用指南

## 概述

Limbic-Flow 使用统一的日志系统，基于 Python 标准库 `logging` 模块，支持控制台和文件输出。

## 功能特性

- 统一的日志格式
- 支持多种日志级别（DEBUG、INFO、WARNING、ERROR、CRITICAL）
- 支持控制台和文件双输出
- 自动创建日志目录
- 支持自定义日志格式和输出目标

## 配置

### 环境变量配置

在 `.env` 文件中配置日志参数：

```bash
# 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# 日志格式
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# 是否启用控制台日志输出
LOG_ENABLE_CONSOLE=true

# 是否启用文件日志输出
LOG_ENABLE_FILE=true

# 日志文件路径（相对于项目根目录的 logs 目录）
LOG_FILE=limbic_flow.log
```

### 日志级别说明

| 级别 | 用途 | 示例 |
|--------|------|------|
| DEBUG | 调试信息，详细的程序执行流程 | "成功保存 10 条记忆到文件" |
| INFO | 一般信息，程序正常运行的关键步骤 | "大脑初始化完成，使用 LLM 提供商: openai" |
| WARNING | 警告信息，不影响程序运行但需要注意 | "未配置 DEEPSEEK_API_KEY 环境变量，将使用默认配置" |
| ERROR | 错误信息，程序出现异常但可以继续运行 | "LLM 调用失败: Connection timeout" |
| CRITICAL | 严重错误，程序无法继续运行 | "数据库连接失败，程序终止" |

## 使用方法

### 基本使用

在模块中导入并使用日志记录器：

```python
from limbic_flow.utils.logger import get_logger

# 获取日志记录器
logger = get_logger("MyModule")

# 记录不同级别的日志
logger.debug("这是一条调试信息")
logger.info("这是一条普通信息")
logger.warning("这是一条警告信息")
logger.error("这是一条错误信息")
logger.critical("这是一条严重错误信息")
```

### 在类中使用

推荐在类的 `__init__` 方法中初始化日志记录器：

```python
from limbic_flow.utils.logger import get_logger

class MyClass:
    def __init__(self):
        self.logger = get_logger("MyClass")
        self.logger.info("类已初始化")
    
    def do_something(self):
        self.logger.debug("开始执行操作")
        try:
            # 执行操作
            self.logger.info("操作执行成功")
        except Exception as e:
            self.logger.error(f"操作执行失败: {e}", exc_info=True)
```

### 使用 LoggerMixin

对于需要日志功能的类，可以继承 `LoggerMixin`：

```python
from limbic_flow.utils.logger import LoggerMixin

class MyClass(LoggerMixin):
    def __init__(self):
        super().__init__()
        # 通过 self.logger 访问日志记录器
        self.logger.info("类已初始化")
    
    def do_something(self):
        self.logger.debug("开始执行操作")
```

### 异常处理

在异常处理中使用日志，并记录完整的堆栈信息：

```python
try:
    # 执行操作
    result = some_operation()
except Exception as e:
    # 记录错误和堆栈信息
    logger.error(f"操作失败: {e}", exc_info=True)
```

`exc_info=True` 参数会自动记录完整的异常堆栈信息，便于调试。

## 日志输出

### 控制台输出

日志会按照配置的格式输出到控制台：

```
2026-01-19 01:05:00 - LimbicFlowPipeline - INFO - Limbic-Flow Pipeline 初始化完成
2026-01-19 01:05:00 - Brain - INFO - 大脑初始化完成，使用 LLM 提供商: openai
2026-01-19 01:05:01 - FileHippocampus - INFO - 成功从文件加载 5 条记忆
```

### 文件输出

日志文件保存在 `logs/` 目录下，文件名由 `LOG_FILE` 环境变量指定。日志文件会自动创建，无需手动创建。

日志文件示例：

```
2026-01-19 01:05:00 - LimbicFlowPipeline - INFO - Limbic-Flow Pipeline 初始化完成
2026-01-19 01:05:00 - Brain - INFO - 大脑初始化完成，使用 LLM 提供商: openai
2026-01-19 01:05:01 - FileHippocampus - INFO - 成功从文件加载 5 条记忆
2026-01-19 01:05:02 - Amygdala - DEBUG - 处理情绪状态: {'pleasure': 0.0, 'arousal': 0.0, 'dominance': 0.0}
```

## 最佳实践

### 1. 选择合适的日志级别

- **DEBUG**: 仅用于开发调试，生产环境通常不启用
- **INFO**: 记录程序正常运行的关键步骤，生产环境推荐使用
- **WARNING**: 记录潜在问题，不影响程序运行但需要注意
- **ERROR**: 记录错误信息，程序出现异常但可以继续运行
- **CRITICAL**: 记录严重错误，程序无法继续运行

### 2. 使用有意义的日志消息

```python
# 好的日志消息
logger.info(f"成功从文件加载 {len(memories)} 条记忆")
logger.error(f"LLM 调用失败: {e}", exc_info=True)

# 不好的日志消息
logger.info("加载完成")
logger.error("出错了")
```

### 3. 避免在日志中记录敏感信息

```python
# 好的做法
logger.info(f"使用 LLM 提供商: {provider}")

# 不好的做法（可能泄露 API Key）
logger.info(f"使用 API Key: {api_key}")
```

### 4. 使用结构化日志

对于复杂的日志信息，使用结构化格式：

```python
logger.info(f"处理用户输入: user_input='{user_input}', context_keys={list(context.keys())}")
```

### 5. 在关键操作前后记录日志

```python
def process_data(self, data):
    self.logger.debug(f"开始处理数据，数据量: {len(data)}")
    
    try:
        # 处理数据
        result = self._process(data)
        self.logger.info(f"数据处理完成，结果量: {len(result)}")
        return result
    except Exception as e:
        self.logger.error(f"数据处理失败: {e}", exc_info=True)
        raise
```

## 故障排查

### 日志文件未生成

1. 检查 `LOG_ENABLE_FILE` 环境变量是否设置为 `true`
2. 检查 `logs/` 目录是否有写入权限
3. 检查 `LOG_FILE` 环境变量是否正确配置

### 日志级别不生效

1. 检查 `LOG_LEVEL` 环境变量是否正确设置
2. 检查环境变量是否正确加载（确保 `.env` 文件存在）
3. 重启程序以使配置生效

### 日志格式不符合预期

1. 检查 `LOG_FORMAT` 环境变量是否正确设置
2. 确保格式字符串符合 Python logging 模块的格式要求

## 示例

完整的日志使用示例：

```python
from limbic_flow.utils.logger import get_logger

class ExampleService:
    """示例服务类"""
    
    def __init__(self):
        self.logger = get_logger("ExampleService")
        self.logger.info("示例服务初始化完成")
    
    def process_data(self, data):
        """
        处理数据
        
        Args:
            data: 要处理的数据
        """
        self.logger.debug(f"开始处理数据，数据量: {len(data)}")
        
        try:
            # 模拟数据处理
            result = []
            for item in data:
                processed = self._process_item(item)
                result.append(processed)
            
            self.logger.info(f"数据处理完成，结果量: {len(result)}")
            return result
            
        except Exception as e:
            self.logger.error(f"数据处理失败: {e}", exc_info=True)
            raise
    
    def _process_item(self, item):
        """处理单个数据项"""
        self.logger.debug(f"处理数据项: {item}")
        
        # 模拟处理逻辑
        if not item:
            self.logger.warning("数据项为空，跳过处理")
            return None
        
        return item.upper()
```

## 相关文档

- [架构文档](./architecture.md)
- [API 文档](./api.md)
- [使用指南](./usage.md)
