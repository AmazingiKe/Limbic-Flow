"""
管道系统
"""

from typing import Any, Callable, List


class EmotionPipeline:
    """情绪处理管道"""
    
    def __init__(self):
        self.stages: List[Callable] = []
    
    def add_stage(self, stage: Callable):
        """添加阶段"""
        self.stages.append(stage)
    
    def process(self, data: Any) -> Any:
        """处理数据"""
        result = data
        for stage in self.stages:
            result = stage(result)
        return result
    
    def clear(self):
        """清空管道"""
        self.stages.clear()


class PipelineBuilder:
    """管道构建器"""
    
    def __init__(self):
        self.pipeline = EmotionPipeline()
    
    def add(self, stage: Callable) -> "PipelineBuilder":
        self.pipeline.add_stage(stage)
        return self
    
    def build(self) -> EmotionPipeline:
        return self.pipeline


# 示例
def stage1(data):
    return data + " -> stage1"

def stage2(data):
    return data + " -> stage2"

if __name__ == "__main__":
    pipeline = (
        PipelineBuilder()
        .add(stage1)
        .add(stage2)
        .build()
    )
    print(pipeline.process("start"))
