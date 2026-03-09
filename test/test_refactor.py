"""
Emotion System Refactoring Test
Test the new modular architecture
"""

import time
from limbic_flow.core.config import LimbicConfig
from limbic_flow.core.emotion_engine import EmotionEngine, create_sensitive_engine
from limbic_flow.core.amygdala import Amygdala
from limbic_flow.core.amygdala.storage import InMemoryMemoryStore
from limbic_flow.core.types import CognitiveState


def test_emotion_engine():
    """Test emotion engine"""
    print("=== Testing EmotionEngine ===")
    
    # Create engine
    engine = create_sensitive_engine()
    
    # Initial state
    state = engine.get_state()
    print(f"Mood: {engine.get_mood_description()}")
    print(f"  PAD: P={state['pleasure']:.2f}, A={state['arousal']:.2f}, D={state['dominance']:.2f}")
    
    # Reward
    engine.reward(0.5)
    state = engine.get_state()
    print(f"After reward: {engine.get_mood_description()}")
    print(f"  PAD: P={state['pleasure']:.2f}, A={state['arousal']:.2f}, D={state['dominance']:.2f}")
    print(f"  Neurotransmitters: Dopamine={state['dopamine']:.2f}, Cortisol={state['cortisol']:.2f}")
    
    # Stress
    engine.stress(0.4)
    state = engine.get_state()
    print(f"After stress: {engine.get_mood_description()}")
    print(f"  PAD: P={state['pleasure']:.2f}, A={state['arousal']:.2f}, D={state['dominance']:.2f}")
    print(f"  Neurotransmitters: Dopamine={state['dopamine']:.2f}, Cortisol={state['cortisol']:.2f}")
    
    # Relax
    engine.relax(0.5)
    state = engine.get_state()
    print(f"After relax: {engine.get_mood_description()}")
    print(f"  PAD: P={state['pleasure']:.2f}, A={state['arousal']:.2f}, D={state['dominance']:.2f}")
    
    print("PASS: EmotionEngine\n")


def test_amygdala():
    """Test amygdala"""
    print("=== Testing Amygdala ===")
    
    # Use in-memory storage for testing
    config = LimbicConfig.sensitive()
    storage = InMemoryMemoryStore()
    amygdala = Amygdala(config=config, storage=storage)
    
    # Create initial state
    state = CognitiveState(
        user_input="hello",
        pad_vector={"pleasure": 0.3, "arousal": 0.2, "dominance": 0.1}
    )
    
    # Process
    result = amygdala.process(state)
    print(f"After process: PAD={result.pad_vector}, NT={result.neurotransmitters}")
    
    # Process again
    state2 = CognitiveState(
        user_input="I have good news",
        pad_vector={"pleasure": 0.5, "arousal": 0.3, "dominance": 0.2},
        timestamp=time.time()
    )
    result2 = amygdala.process(state2)
    print(f"After 2nd process: PAD={result2.pad_vector}, NT={result2.neurotransmitters}")
    
    # Check history
    history = amygdala.get_emotional_history(limit=5)
    print(f"History records: {len(history)}")
    
    print("PASS: Amygdala\n")


def test_config():
    """Test config system"""
    print("=== Testing Config System ===")
    
    # Default config
    default = LimbicConfig()
    print(f"Default - Pleasure half-life: {default.half_life.pleasure}s")
    
    # Relaxed config
    relaxed = LimbicConfig.relaxed()
    print(f"Relaxed - Pleasure half-life: {relaxed.half_life.pleasure}s")
    
    # Sensitive config
    sensitive = LimbicConfig.sensitive()
    print(f"Sensitive - Pleasure half-life: {sensitive.half_life.pleasure}s")
    
    print("PASS: Config System\n")


if __name__ == "__main__":
    print("=== Running refactored emotion system tests ===\n")
    
    test_config()
    test_emotion_engine()
    test_amygdala()
    
    print("=== All tests passed! ===")
