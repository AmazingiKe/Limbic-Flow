"""
工作流引擎
"""

from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Step:
    """工作流步骤"""
    name: str
    func: Callable
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)


class Workflow:
    """工作流引擎"""
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[Step] = []
        self.dependencies: Dict[str, List[str]] = {}
    
    def add_step(
        self, 
        name: str, 
        func: Callable,
        inputs: List[str] = None,
        outputs: List[str] = None,
        depends_on: List[str] = None
    ):
        """添加步骤"""
        step = Step(name, func, inputs or [], outputs or [])
        self.steps.append(step)
        
        if depends_on:
            self.dependencies[name] = depends_on
    
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """运行工作流"""
        results = {}
        
        for step in self.steps:
            # 准备输入
            inputs = {}
            for input_name in step.inputs:
                if input_name in context:
                    inputs[input_name] = context[input_name]
                elif input_name in results:
                    inputs[input_name] = results[input_name]
            
            # 执行步骤
            output = step.func(**inputs)
            
            # 收集输出
            for i, output_name in enumerate(step.outputs):
                if isinstance(output, tuple):
                    results[output_name] = output[i] if i < len(output) else None
                else:
                    results[output_name] = output
        
        return results
