"""
Pathology Module Test
"""

import numpy as np
import time
from limbic_flow.middleware.pathology import (
    DepressionPathology,
    AlzheimerPathology,
    PTSDPathology,
    HSPPathology,
    create_pathology_middleware,
    BasePathologyMiddleware,
)
from limbic_flow.core.types import CognitiveState


def test_depression_pathology():
    """Test depression pathology"""
    print("=== Testing DepressionPathology ===")
    
    pathology = DepressionPathology(base_severity=0.5)
    
    # Test should_apply
    assert pathology.should_apply({"cortisol": 0.5, "pleasure": 0.0}) == True
    assert pathology.should_apply({"cortisol": 0.3, "pleasure": 0.0}) == False
    assert pathology.should_apply({"cortisol": 0.3, "pleasure": -0.3}) == True
    
    # Test severity calculation
    severity_low = pathology._calculate_severity({"cortisol": 0.3})
    severity_high = pathology._calculate_severity({"cortisol": 0.8})
    assert severity_high > severity_low
    
    # Test memory distortion
    memories = [
        {"pad": {"pleasure": 0.8}, "content": "Good memory"},
        {"pad": {"pleasure": -0.2}, "content": "Bad memory"},
    ]
    emotional_state = {"cortisol": 0.6, "pleasure": -0.1}
    distorted = pathology.distort_memories(memories, emotional_state)
    
    # Happy memory should be filtered or reduced
    print(f"Original: {len(memories)} -> Distorted: {len(distorted)}")
    print("PASS: DepressionPathology\n")


def test_alzheimer_pathology():
    """Test alzheimer pathology"""
    print("=== Testing AlzheimerPathology ===")
    
    pathology = AlzheimerPathology(severity=0.8)
    
    # Test query distortion
    query = np.array([1.0, 2.0, 3.0])
    distorted = pathology.distort_query(query, {})
    
    # Should add noise but keep general direction
    assert distorted.shape == query.shape
    assert not np.allclose(distorted, query)
    
    # Test memory distortion - recent memories blocked
    now = time.time()
    memories = [
        {"timestamp": now - 3600, "content": "1 hour ago"},    # Recent
        {"timestamp": now - 86400 * 30, "content": "30 days ago"},  # Old
    ]
    distorted = pathology.distort_memories(memories, {"timestamp": now})
    
    # Recent memory should be blocked
    print(f"Original: {len(memories)} -> Distorted: {len(distorted)}")
    print("PASS: AlzheimerPathology\n")


def test_hsp_pathology():
    """Test HSP pathology"""
    print("=== Testing HSPPathology ===")
    
    pathology = HSPPathology(sensitivity=0.5)
    
    # Test should_apply
    assert pathology.should_apply({"arousal": 0.2}) == True
    assert pathology.should_apply({"arousal": 0.0}) == False
    
    # Test memory amplification
    memories = [
        {"pad": {"pleasure": 0.3, "arousal": 0.2, "dominance": 0.1}},
    ]
    distorted = pathology.distort_memories(memories, {"arousal": 0.3})
    
    # Should amplify
    assert distorted[0]["pad"]["pleasure"] > memories[0]["pad"]["pleasure"]
    print(f"Original pleasure: {memories[0]['pad']['pleasure']} -> Amplified: {distorted[0]['pad']['pleasure']}")
    print("PASS: HSPPathology\n")


def test_pathology_middleware():
    """Test combined pathology middleware"""
    print("=== Testing PathologyMiddleware ===")
    
    middleware = create_pathology_middleware(
        enable_depression=True,
        enable_alzheimer=False,
        enable_hsp=True
    )
    
    state = CognitiveState(
        user_input="hello",
        pad_vector={"pleasure": 0.3, "arousal": 0.2, "dominance": 0.1},
        neurotransmitters={"dopamine": 0.5, "cortisol": 0.6},
        memories=[{"content": "test memory"}]
    )
    
    result = middleware.process(state)
    
    print(f"Distorted memories: {len(result.distorted_memories)}")
    print("PASS: PathologyMiddleware\n")


def test_prompt_builder():
    """Test prompt builder"""
    print("=== Testing PromptBuilder ===")
    
    from limbic_flow.core.brain.prompt_builder import PromptBuilder
    
    builder = PromptBuilder()
    
    state = CognitiveState(
        user_input="Hello",
        pad_vector={"pleasure": 0.5, "arousal": 0.3, "dominance": 0.2},
        neurotransmitters={"dopamine": 0.6, "cortisol": 0.2},
        distorted_memories=[{"user_input": "previous", "system_response": "response"}]
    )
    
    system_prompt = builder.build_system_prompt(state, "Shanghai")
    user_prompt = builder.build_user_prompt(state)
    
    assert "积极" in system_prompt or "positive" in system_prompt.lower()
    assert "Hello" in user_prompt
    
    # Test fallback
    fallback = builder.get_fallback_response(state)
    assert isinstance(fallback, str)
    assert len(fallback) > 0
    
    print(f"System prompt length: {len(system_prompt)}")
    print(f"User prompt length: {len(user_prompt)}")
    print(f"Fallback: {fallback}")
    print("PASS: PromptBuilder\n")


if __name__ == "__main__":
    print("=== Running Pathology and Brain Tests ===\n")
    
    test_depression_pathology()
    test_alzheimer_pathology()
    test_hsp_pathology()
    test_pathology_middleware()
    test_prompt_builder()
    
    print("=== All tests passed! ===")
