# Depression Modeling in AI

## Overview

Depression modeling in AI systems involves computational approaches to simulate depressive symptoms and cognitive patterns. This document covers key mechanisms for implementing depression-like states in artificial agents.

---

## 1. Anhedonia Simulation

### What is Anhedonia?
Anhedonia is the inability to feel pleasure — a core symptom of depression. In AI terms, this translates to **diminished reward sensitivity** and **reduced reinforcement learning rates**.

### Implementation Approaches

```python
# Anhedonia: Reduced reward sensitivity
class AnhedonicRewardModulator:
    def __init__(self, base_sensitivity=1.0, anhedonia_factor=0.3):
        self.sensitivity = base_sensitivity * anhedonia_factor
    
    def compute_reward_signal(self, raw_reward):
        # Compress the reward range (diminished pleasure response)
        return self.sensitivity * raw_reward
    
    def update_sensitivity(self, reward_history):
        # Gradual decay based on recent negative outcomes
        recent_negativity = sum(1 for r in reward_history if r < 0)
        decay = min(1.0, recent_negativity * 0.05)
        self.sensitivity *= (1 - decay)
```

### Key Parameters
- **Reward sensitivity multiplier**: 0.2-0.5 for moderate anhedonia
- **Learning rate depression**: Reduce RL learning rate by 30-50%
- **Pleasure compression**: Compress positive reward signals

---

## 2. Negative Bias Algorithms

### Cognitive Negative Bias
Depressed individuals exhibit negativity bias — they weight negative experiences more heavily than positive ones.

### Implementation

```python
class NegativeBiasProcessor:
    def __init__(self, negative_weight=2.0, positive_weight=0.5):
        self.negative_weight = negative_weight
        self.positive_weight = positive_weight
    
    def process_experience(self, event_valence, event_intensity):
        """
        valence: -1 (negative) to +1 (positive)
        intensity: 0.0 to 1.0
        """
        if event_valence < 0:
            # Negative events weighted more heavily
            weighted = event_valence * event_intensity * self.negative_weight
        else:
            # Positive events dampened
            weighted = event_valence * event_intensity * self.positive_weight
        
        return weighted
```

### Effects on Learning
- **Negative memory buffer**: Increase retention of negative memories
- **Attentional bias**: Higher probability of attending to negative stimuli
- **Interpretation bias**: Neutral events interpreted negatively

---

## 3. Melancholy vs Typical Depression

### Distinction

| Feature | Typical Depression | Melancholic Depression |
|---------|-------------------|------------------------|
| Mood | Low, pervasive | Severe, persistent |
| Anhedonia | Partial (lost interest) | Complete (cannot enjoy) |
| Motor function | Mild retardation | Severe psychomotor retardation |
| Diurnal variation | Worse morning | Usually worse morning |
| Weight loss | Variable | Common |
| Guilt | Common | Severe, pervasive |

### Modeling Melancholy

```python
class MelancholicState:
    def __init__(self):
        self.anhedonia_depth = 0.9  # Near-complete
        self.psychomotor_slowdown = 0.8
        self.diurnal_mood_swing = 0.4  # Worse in morning
        self.cognitive_execution_delay = 2.0  # Slowed thinking
    
    def compute_action_potential(self, action_value, current_energy):
        # Reduced initiation despite knowing value
        initiation_cost = self.psychomotor_slowdown * 0.3
        return max(0, action_value - initiation_cost) * current_energy
```

### Typical Depression Features
- **Sleep dysregulation**: Either hypersomnia or insomnia modeling
- **Energy depletion**: Gradual fatigue accumulation
- **Hopelessness**: Reduced future-oriented planning
- **Rumination**: Recurrent negative thought loops

---

## 4. Additional Depression Mechanisms

### Rumination Loop
```python
class RuminationModule:
    def __init__(self):
        self.rumination_probability = 0.3
        self.negative_thought_pool = []
    
    def process_negative_event(self, event):
        # High probability of repetitive negative thinking
        if random() < self.rumination_probability:
            self.negative_thought_pool.append(event)
            return self.generate_ruminative_thought()
        return None
    
    def generate_ruminative_thought(self):
        # Iterative negative interpretation
        return f"Rumination: {self.negative_thought_pool[-1]} → worse interpretation"
```

### Sleep-Energy Coupling
```python
# Depression: poor sleep → poor function → worse sleep
class SleepMoodCoupling:
    def update(self, sleep_quality, current_mood):
        # Poor sleep degrades next-day mood
        mood_impact = (1 - sleep_quality) * 0.3
        return current_mood - mood_impact
```

---

## 5. Measurement & Metrics

### Depression Severity Indicators
- **Anhedonia index**: Ratio of positive to negative reward sensitivity
- **Negativity bias score**: Weighted negative memory vs positive memory
- **Behavioral activation**: Action initiation frequency
- **Response latency**: Decision speed degradation

### Recovery Indicators
- Increasing reward sensitivity over time
- Normalization of negative bias
- Increased behavioral activation
- Reduced rumination frequency

---

## References

- APA Diagnostic and Statistical Manual of Mental Disorders
- Computational Psychiatry: Reinforcement Learning Approaches (Schultz, Dayan, Montague)
- Affective Computing: Modeling Emotion in Artificial Agents
