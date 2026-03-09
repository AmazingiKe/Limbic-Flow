"""
自动测试
"""

import unittest
from unittest.mock import Mock, patch
from limbic_flow.core.emotion.occ import OCCEngine, OCCState


class TestOCCEngine(unittest.TestCase):
    """OCC 引擎测试"""
    
    def setUp(self):
        self.engine = OCCEngine()
    
    def test_initial_state(self):
        """测试初始状态"""
        state = self.engine.state
        self.assertIsInstance(state, OCCState)
        self.assertEqual(state.joy, 0.0)
    
    def test_positive_event(self):
        """测试正面事件"""
        self.engine.appraise({
            "type": "event",
            "desirability": 0.8,
            "likelihood": 0.9,
            "realized": True
        })
        self.assertGreater(self.engine.state.joy, 0)
    
    def test_negative_event(self):
        """测试负面事件"""
        self.engine.appraise({
            "type": "event",
            "desirability": -0.7,
            "likelihood": 0.8,
            "realized": True
        })
        self.assertGreater(self.engine.state.sadness, 0)
    
    def test_decay(self):
        """测试情绪衰减"""
        self.engine.appraise({
            "type": "event",
            "desirability": 0.8,
            "realized": True
        })
        
        initial_joy = self.engine.state.joy
        self.engine.decay(3600)  # 1小时后
        self.assertLess(self.engine.state.joy, initial_joy)
    
    def test_reset(self):
        """测试重置"""
        self.engine.appraise({
            "type": "event", 
            "desirability": 0.8
        })
        self.engine.reset()
        
        emotions = self.engine.state.to_dict()
        for v in emotions.values():
            self.assertEqual(v, 0.0)


class TestEmotionProjection(unittest.TestCase):
    """测试 OCC → PAD 投影"""
    
    def test_joy_to_pad(self):
        """测试喜悦投影"""
        from limbic_flow.core.emotion.occ import OCCToPADProjector, OCCState
        
        state = OCCState(joy=0.8)
        pad = OCCToPADProjector.project(state)
        
        self.assertGreater(pad["pleasure"], 0)
    
    def test_fear_to_pad(self):
        """测试恐惧投影"""
        from limbic_flow.core.emotion.occ import OCCToPADProjector, OCCState
        
        state = OCCState(fear=0.7)
        pad = OCCToPADProjector.project(state)
        
        self.assertLess(pad["pleasure"], 0)
        self.assertGreater(pad["arousal"], 0)


if __name__ == '__main__':
    unittest.main()
