# Memory Forgetting Mechanisms

## Overview

This document explores the science of memory forgetting and its applications in artificial intelligence systems. It covers theoretical frameworks, computational models, and implementation strategies for creating healthy forgetting mechanisms in AI systems.

---

## 1. Understanding Memory Forgetting

### 1.1 Why Forgetting Is Essential

Contrary to common assumption, forgetting is not a flaw—it is a feature of adaptive cognitive systems. Healthy forgetting serves several critical functions:

- **Cognitive Load Management**: Prevents overwhelming of limited mental resources
- **Emotional Regulation**: Allows painful memories to fade over time
- **Adaptation**: Enables flexible decision-making in changing environments
- **Privacy Protection**: Natural mechanism for sensitive information decay
- **Pattern Extraction**: Focuses attention on statistically relevant information

### 1.2 Types of Forgetting

| Type | Mechanism | Purpose | Example |
|------|-----------|---------|---------|
| Natural Decay | Time-based weakening of memory traces | Normal aging of memories | Forgetting a phone number after a few hours |
| Suppressive | Active inhibition of memory retrieval | Emotional regulation | Deliberately not thinking about a traumatic event |
| Interference | Other memories disrupt retrieval | Competition between memories | Mixing up two similar passwords |
| Adaptive | Context-dependent retention | Optimization | Forgetting where you parked yesterday (irrelevant today) |

---

## 2. The Ebbinghaus Forgetting Curve

### 2.1 Historical Foundation

Hermann Ebbinghaus (1885) discovered that memory retention follows a predictable decay curve:

```
Retention (%) = 100 × e^(-t/S)
```

Where:
- `t` = time since learning
- `S` = stability of the memory (varies by material)

### 2.2 Modern Extensions

Contemporary models incorporate additional factors:

- **Item Difficulty**: Harder items decay faster
- **Encoding Strength**: Deeper processing creates more durable memories
- **Spaced Repetition**: Interleaved practice slows decay
- **Emotional Valence**: Emotional memories decay more slowly

### 2.3 Computational Implementation

```python
class EbbinghausForgettingCurve:
    def __init__(self, stability_factor: float = 1.0):
        self.stability_factor = stability_factor
        self.baseline_decay_rate = 0.1
    
    def calculate_retention(self, 
                            time_elapsed: float, 
                            memory_strength: float = 1.0) -> float:
        """
        Calculate probability of memory retention after time elapsed.
        
        Args:
            time_elapsed: Time since memory was encoded (in arbitrary time units)
            memory_strength: Initial encoding strength (0.0 to 1.0)
        
        Returns:
            Probability of successful recall (0.0 to 1.0)
        """
        decay_rate = self.baseline_decay_rate / self.stability_factor
        retention = memory_strength * np.exp(-decay_rate * time_elapsed)
        return max(0.0, min(1.0, retention))
    
    def time_to_threshold(self, threshold: float = 0.5) -> float:
        """Calculate time to reach retention threshold."""
        if threshold <= 0:
            return float('inf')
        return -np.log(threshold) * self.stability_factor / self.baseline_decay_rate
```

---

## 3. Adaptive Forgetting for Mental Health

### 3.1 Healthy vs. Unhealthy Forgetting

| Healthy Forgetting | Unhealthy Forgetting |
|-------------------|---------------------|
| Gradual decay of neutral memories | Intrusive recollection of traumatic events |
| Emotional memories fade appropriately | Persistent rumination on negative content |
| Context-appropriate retention | Inability to forget fear-relevant stimuli |
| Flexible retrieval | Compulsive memory retrieval |

### 3.2 Computational Model of Adaptive Forgetting

```python
class AdaptiveForgetting:
    """
    Model that implements contextually appropriate forgetting
    for mental health applications.
    """
    
    def __init__(self):
        self.emotional_decay_rate = 0.02  # Slower for emotional content
        self.neutral_decay_rate = 0.15     # Faster for neutral content
        self.trauma_decay_rate = 0.005     # Very slow for trauma
        self.regulation_bonus = 0.5        # Active regulation effect
    
    def calculate_decay_rate(self, 
                             memory_type: str, 
                             emotional_intensity: float,
                             active_regulation: bool = False) -> float:
        """Calculate appropriate decay rate based on memory characteristics."""
        
        # Base decay rate
        if memory_type == "traumatic":
            base_rate = self.trauma_decay_rate
        elif memory_type == "emotional":
            base_rate = self.emotional_decay_rate
        else:
            base_rate = self.neutral_decay_rate
        
        # Emotional intensity increases retention (slower decay)
        intensity_modifier = 1.0 + (emotional_intensity * 2.0)
        
        # Active regulation (e.g., mindfulness, therapy) accelerates healthy forgetting
        if active_regulation:
            base_rate *= self.regulation_bonus
        
        return base_rate * intensity_modifier
    
    def should_forget(self, 
                       memory: dict, 
                       current_context: dict) -> bool:
        """Determine if a memory should be actively forgotten."""
        
        # Keep memories relevant to current context
        if memory.get("context") == current_context.get("active_context"):
            return False
        
        # Keep emotionally significant recent memories
        if memory.get("time_since") < 1.0 and memory.get("emotional_intensity") > 0.8:
            return False
        
        # Forget irrelevant, neutral older memories
        if (memory.get("context") != current_context.get("active_context") and
            memory.get("emotional_intensity") < 0.3):
            return True
        
        # Use decay calculation
        decay_rate = self.calculate_decay_rate(
            memory.get("type", "neutral"),
            memory.get("emotional_intensity", 0.0),
            memory.get("active_regulation", False)
        )
        
        retention = np.exp(-decay_rate * memory.get("time_since", 1.0))
        return retention < 0.3
```

---

## 4. Forgetting Curve Implementation

### 4.1 Spaced Repetition Integration

The forgetting curve is fundamental to spaced repetition systems (SRS), which optimize review schedules:

```python
class SpacedRepetitionScheduler:
    """
    Implements adaptive spaced repetition based on forgetting curves.
    Used in language learning and memory optimization.
    """
    
    def __init__(self):
        self.half_life_base = 1.0  # Days
        self.difficulty_modifier = 1.0
    
    def calculate_interval(self, 
                          performance: float, 
                          difficulty: float,
                          previous_interval: float = 1.0) -> float:
        """
        Calculate optimal next review interval based on performance.
        
        Args:
            performance: 0.0 (complete failure) to 1.0 (perfect recall)
            difficulty: 0.0 (easy) to 1.0 (hard)
            previous_interval: Previous review interval in days
        
        Returns:
            Next review interval in days
        """
        
        # Easiness factor (standard SM-2 algorithm)
        ease_factor = 1.3
        if performance < 0.5:
            ease_factor = max(1.3, ease_factor - 0.2)
        else:
            ease_factor = ease_factor + (0.1 - (0.08 * (1 - performance)))
        
        # Adjust for difficulty
        difficulty_factor = 1.0 + difficulty
        
        # Calculate new interval
        if performance >= 0.85:
            # Successful recall - increase interval
            if previous_interval == 1.0:
                new_interval = 1.0
            elif previous_interval == 6.0:
                new_interval = previous_interval * ease_factor
            else:
                new_interval = previous_interval * ease_factor * difficulty_factor
        else:
            # Failed recall - reset or decrease
            new_interval = max(1.0, previous_interval * 0.5)
        
        return new_interval
    
    def predict_recall_probability(self,
                                   time_since_review: float,
                                   half_life: float) -> float:
        """
        Predict probability of recall at given time point.
        Based on exponential forgetting curve.
        """
        return np.exp(-time_since_review / half_life)
```

### 4.2 Neural Network Approaches

Modern approaches use neural networks to model personalized forgetting:

```python
class NeuralForgettingCurve:
    """
    Neural network model for personalized forgetting curve estimation.
    Based on work by Zaidi et al. (2020) on adaptive forgetting curves.
    """
    
    def __init__(self, input_dim: int, hidden_dim: int = 32):
        self.model = NeuralNetwork(input_dim, hidden_dim, 1)
    
    def extract_features(self, 
                        item: dict, 
                        user: dict, 
                        history: dict) -> np.ndarray:
        """Extract features for forgetting prediction."""
        
        features = []
        
        # Item features
        features.append(item.get("complexity", 0.5))
        features.append(item.get("concreteness", 0.5))
        features.append(item.get("frequency", 0.5))
        
        # User features
        features.append(user.get("ability", 0.5))
        features.append(user.get("engagement", 0.5))
        
        # History features
        features.append(history.get("times_seen", 0))
        features.append(history.get("avg_score", 0.5))
        features.append(history.get("time_since_last", 0))
        
        return np.array(features)
    
    def predict_half_life(self, 
                          item: dict, 
                          user: dict, 
                          history: dict) -> float:
        """Predict personalized half-life for item-user combination."""
        
        features = self.extract_features(item, user, history)
        half_life = self.model.predict(features)
        
        return max(0.1, half_life)  # Minimum half-life of 0.1 days
```

---

## 5. Natural Decay vs. Suppressive Forgetting

### 5.1 Natural Decay

Natural forgetting occurs passively over time without conscious effort:

```python
class NaturalDecay:
    """
    Implements natural, passive forgetting through decay.
    Memory traces weaken simply with the passage of time.
    """
    
    def __init__(self, base_decay: float = 0.1):
        self.base_decay = base_decay
    
    def decay_memory(self, memory: dict, delta_time: float) -> dict:
        """
        Apply natural decay to a memory.
        
        Memory strength decreases exponentially with time:
        strength(t) = strength(0) * e^(-decay_rate * time)
        """
        
        # Memory-specific decay rate
        decay_rate = self.base_decay * memory.get("stability_modifier", 1.0)
        
        # Calculate new strength
        old_strength = memory.get("strength", 1.0)
        new_strength = old_strength * np.exp(-decay_rate * delta_time)
        
        # Update memory
        memory["strength"] = new_strength
        memory["last_decay"] = delta_time
        
        return memory
```

### 5.2 Suppressive Forgetting

Active suppression involves deliberate inhibition of memory retrieval:

```python
class SuppressiveForgetting:
    """
    Implements active, suppressive forgetting mechanisms.
    Based on psychological theories of memory suppression and thought suppression.
    """
    
    def __init__(self):
        self.suppression_strength = 0.0
        self.rebound_threshold = 0.8
    
    def suppress_memory(self, memory: dict, suppression_effort: float) -> dict:
        """
        Actively suppress a memory.
        
        Note: Thought suppression often leads to rebound effects
        (ironic rebound theory - Wegner et al.)
        """
        
        # Active suppression reduces retrieval probability
        retrieval_inhibition = suppression_effort * 0.3
        
        # Store suppression state
        memory["suppression_attempts"] = memory.get("suppression_attempts", 0) + 1
        memory["last_suppression"] = suppression_effort
        memory["retrieval_inhibition"] = max(
            memory.get("retrieval_inhibition", 0),
            retrieval_inhibition
        )
        
        return memory
    
    def check_rebound_risk(self, memory: dict) -> float:
        """
        Calculate risk of rebound (return of suppressed thought).
        
        Higher suppression attempts = higher rebound risk
        """
        
        attempts = memory.get("suppression_attempts", 0)
        time_since_suppression = memory.get("time_since_suppression", float('inf'))
        
        # Rebound risk increases with attempts and decreases with time
        if time_since_suppression > 24:  # Hours
            return 0.0
        
        risk = min(1.0, attempts * 0.2 * (1 - time_since_suppression / 24))
        return risk
```

---

## 6. Forgetting in AI Systems

### 6.1 Right to Be Forgotten

AI systems increasingly need to implement forgetting for privacy:

```python
class PrivacyForgetting:
    """
    Implements privacy-focused forgetting mechanisms.
    For compliance with GDPR and similar regulations.
    """
    
    def __init__(self):
        self.data_categories = {
            "personal": {"decay_days": 365, "priority": "high"},
            "behavioral": {"decay_days": 180, "priority": "medium"},
            "analytical": {"decay_days": 730, "priority": "low"}
        }
    
    def schedule_deletion(self, 
                         data_type: str, 
                         sensitivity: float) -> datetime:
        """Schedule data for forgetting based on type and sensitivity."""
        
        config = self.data_categories.get(data_type, {"decay_days": 365})
        
        # Higher sensitivity = faster deletion
        adjusted_days = config["decay_days"] * (1.0 - sensitivity * 0.5)
        
        return datetime.now() + timedelta(days=adjusted_days)
    
    def apply_forgetting(self, user_data: dict, current_time: datetime) -> dict:
        """Apply forgetting to user data, returning anonymized/aggregated version."""
        
        forgotten_data = {}
        
        for key, value in user_data.items():
            data_age = (current_time - value.get("timestamp", current_time)).days
            decay_rate = value.get("decay_rate", 0.1)
            
            retention = np.exp(-decay_rate * data_age)
            
            if retention < 0.1:
                # Below threshold - forget completely
                forgotten_data[key] = None
            elif retention < 0.5:
                # Partial retention - anonymize
                forgotten_data[key] = self.anonymize(value)
            else:
                # Full retention
                forgotten_data[key] = value
        
        return forgotten_data
```

### 6.2 Cognitive Load Management

Forgetting also serves to manage cognitive resources:

```python
class CognitiveLoadForgetting:
    """
    Implements forgetting to manage cognitive load in AI systems.
    Prevents memory overflow while preserving important information.
    """
    
    def __init__(self, max_memory_items: int = 1000):
        self.max_memory_items = max_memory_items
        self.priority_weights = {
            "recency": 0.3,
            "importance": 0.4,
            "frequency": 0.2,
            "context_relevance": 0.1
        }
    
    def calculate_priority(self, memory: dict, current_context: dict) -> float:
        """Calculate priority score for memory retention."""
        
        priority = 0.0
        
        # Recency score
        priority += self.priority_weights["recency"] * memory.get("recency_score", 0.0)
        
        # Importance score
        priority += self.priority_weights["importance"] * memory.get("importance", 0.0)
        
        # Frequency score
        priority += self.priority_weights["frequency"] * memory.get("access_frequency", 0.0)
        
        # Context relevance
        if memory.get("context") == current_context.get("active_context"):
            priority += self.priority_weights["context_relevance"]
        
        return priority
    
    def forget_low_priority(self, memory_store: dict, context: dict) -> dict:
        """Remove lowest priority memories when capacity exceeded."""
        
        if len(memory_store) <= self.max_memory_items:
            return memory_store
        
        # Calculate priorities
        priorities = [
            (key, self.calculate_priority(memory, context))
            for key, memory in memory_store.items()
        ]
        
        # Sort by priority (ascending)
        priorities.sort(key=lambda x: x[1])
        
        # Remove lowest priority items
        items_to_remove = len(memory_store) - self.max_memory_items
        for i in range(items_to_remove):
            key_to_remove = priorities[i][0]
            del memory_store[key_to_remove]
        
        return memory_store
```

---

## 7. Applications in Limbic-Flow

### 7.1 Integration Points

For the Limbic-Flow project, consider implementing:

1. **Emotional Memory Decay**: Sensitive handling of emotionally-charged memories
2. **Context-Switching**: Forgetting irrelevant context when switching focus
3. **Privacy Compliance**: User-controlled forgetting for personal data
4. **Cognitive Health**: Mimicking healthy human forgetting patterns

### 7.2 Configuration Example

```python
# Recommended configuration for mental-health-aware forgetting
limbic_forgetting_config = {
    "natural_decay": {
        "enabled": True,
        "base_decay_rate": 0.1,
        "emotional_buffer": True,  # Slow decay for emotional content
    },
    "suppressive_forgetting": {
        "enabled": True,
        "rebound_prevention": True,
        "max_suppression_cycles": 3,
    },
    "adaptive_forgetting": {
        "enabled": True,
        "context_tracking": True,
        "importance_weighting": True,
    },
    "privacy_forgetting": {
        "enabled": True,
        "user_controlled": True,
        "gdpr_compliance": True,
    }
}
```

---

## 8. References and Further Reading

- Ebbinghaus, H. (1885). *Über das Gedächtnis*.
- Zaidi, A., et al. (2020). Adaptive Forgetting Curves for Spaced Repetition Language Learning. *AI in Education*.
- Rubin, D.C., & Wenzel, A.E. (1996). One hundred years of forgetting: A quantitative description of retention.
- Averell, L., & Heathcote, A. (2011). The form of the forgetting curve and the fate of memories. *J. Math. Psychol.*
- Settles, B., & Meeder, B. (2016). A Trainable Spaced Repetition Model for Language Learning.
- Tabibian, B., et al. (2019). Enhancing human learning via spaced repetition optimization. *PNAS*.

---

## 9. Implementation Guidelines

1. **Start Simple**: Begin with basic exponential decay
2. **Add Personalization**: Allow user-specific parameters
3. **Monitor Health**: Track forgetting patterns for well-being indicators
4. **Respect Boundaries**: Always allow user control over their data
5. **Test Thoroughly**: Verify forgetting doesn't remove critical information
