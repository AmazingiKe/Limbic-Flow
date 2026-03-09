"""
Pipeline Config Test
"""

from limbic_flow.pipeline.config import PipelineConfig


def test_default_config():
    """Test default config"""
    config = PipelineConfig()
    
    assert config.llm_provider is None
    assert config.memory_limit == 5
    assert config.enable_depression == True
    assert config.enable_alzheimer == False
    assert config.base_wpm == 60
    
    print("PASS: Default config")


def test_relaxed_config():
    """Test relaxed config"""
    config = PipelineConfig.relaxed()
    
    assert config.use_sensitive_emotion == False
    assert config.enable_depression == False
    assert config.enable_hsp == False
    
    print("PASS: Relaxed config")


def test_sensitive_config():
    """Test sensitive config"""
    config = PipelineConfig.sensitive()
    
    assert config.use_sensitive_emotion == True
    assert config.enable_depression == True
    assert config.enable_hsp == True
    assert config.depression_severity == 0.5
    assert config.hsp_sensitivity == 0.7
    
    print("PASS: Sensitive config")


def test_alzheimer_config():
    """Test alzheimer config"""
    config = PipelineConfig.alzheimer_mode()
    
    assert config.enable_alzheimer == True
    assert config.alzheimer_severity == 0.7
    
    print("PASS: Alzheimer config")


if __name__ == "__main__":
    print("=== Testing Pipeline Config ===\n")
    
    test_default_config()
    test_relaxed_config()
    test_sensitive_config()
    test_alzheimer_config()
    
    print("\n=== All tests passed! ===")
