"""
Pipeline 测试
"""

import unittest
from unittest.mock import Mock, patch
from limbic_flow.pipeline import LimbicFlowPipeline
from limbic_flow.pipeline.config import PipelineConfig


class TestPipeline(unittest.TestCase):
    """Pipeline 测试"""
    
    def setUp(self):
        self.config = PipelineConfig()
        self.pipeline = LimbicFlowPipeline(config=self.config)
    
    def test_initialization(self):
        """测试初始化"""
        self.assertIsNotNone(self.pipeline.amygdala)
        self.assertIsNotNone(self.pipeline.brain)
        self.assertIsNotNone(self.pipeline.motor_cortex)
    
    def test_process_input(self):
        """测试输入处理"""
        # 使用 mock 避免实际调用 LLM
        with patch.object(self.pipeline.brain, 'process') as mock_brain:
            mock_brain.return_value = Mock(
                final_response_text="Hello!",
                content="Hello!",
                action_queue=[]
            )
            
            results = list(self.pipeline.process_input("Hello"))
            self.assertIsInstance(results, list)


class TestPipelineConfig(unittest.TestCase):
    """Pipeline 配置测试"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = PipelineConfig()
        
        self.assertEqual(config.llm_provider, None)
        self.assertEqual(config.memory_limit, 5)
        self.assertFalse(config.enable_depression)
    
    def test_relaxed_config(self):
        """测试放松配置"""
        config = PipelineConfig.relaxed()
        
        self.assertFalse(config.use_sensitive_emotion)
        self.assertFalse(config.enable_depression)
    
    def test_sensitive_config(self):
        """测试敏感配置"""
        config = PipelineConfig.sensitive()
        
        self.assertTrue(config.use_sensitive_emotion)
        self.assertTrue(config.enable_depression)


if __name__ == '__main__':
    unittest.main()
