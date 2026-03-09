# Bipolar Disorder Simulation

## Overview

Bipolar disorder involves dramatic mood swings between depression and mania/hypomania. In AI systems, this requires modeling **mood cycling dynamics**, **state-dependent cognitive changes**, and **energy-valence interactions**.

---

## 1. Mania/Hypomania Modeling

### Core Manic Features

| Feature | Hypomania | Mania |
|---------|-----------|-------|
| Mood | Elevated, expansive | Elevated, irritable |
| Duration | 4+ days | 1+ week |
| Function | Minimally impaired | Severely impaired |
| Psychomotor | Increased goal activity | Disorganized, rapid |
| Thought | Racing thoughts | Flight of ideas |
| Risk-taking | Increased | Impulsive, reckless |

### Implementation: Manic State

```python
class ManicStateModulator:
    def __init__(self, intensity=0.7):
        self.intensity = intensity  # 0.0-1.0 (hypomania to full mania)
        
        # Increased reward sensitivity
        self.reward_sensitivity = 1.5 + (intensity * 1.5)
        
        # Reduced punishment sensitivity
        self.punishment_sensitivity = 1.0 - (intensity * 0.6)
        
        # Reduced sleep need
        self.sleep_need_multiplier = 1.0 - (intensity * 0.7)
        
        # Increased goal-directed behavior
        self.goal_activation_threshold = 0.3 - (intensity * 0.2)
        
        # Reduced deliberation (impulsivity)
        self.decision_delay_factor = 1.0 - (intensity * 0.8)
    
    def process_reward(self, raw_reward):
        """Amplified reward response in manic states"""
        return raw_reward * self.reward_sensitivity
    
    def should_initiate_action(self, action_value, deliberation_time):
        """Rapid action initiation despite incomplete deliberation"""
        threshold = self.goal_activation_threshold
        return action_value > threshold
```

### Cognitive Changes in Mania

```python
class ManicCognition:
    def __init__(self):
        self.racing_thoughts_probability = 0.7
        self.attention_spread = 0.8  # Broad attention
        self.creativity_boost = 1.3
        self.judgment_impairment = 0.6
    
    def process_thought_stream(self, stimuli):
        """Manic thought processing: fast, associative, broad"""
        # Reduced filtering - more associations
        associations = self._generate_associations(stimuli)
        return {
            'thoughts': associations,
            'speed': 2.5,  # Accelerated
            'focus': self.attention_spread  # Less focused
        }
```

---

## 2. Mood Cycling in AI

### Basic Cycling Dynamics

```python
class MoodCycler:
    def __init__(self):
        self.mood_state = 0.0  # -1.0 (depressed) to +1.0 (manic)
        self.cycling_speed = 0.02  # Change per tick
        self.cycling_amplitude = 1.0
        
        # State-dependent parameters
        self.depressed_params = DepressedState()
        self.manic_params = ManicStateModulator()
    
    def update_mood(self, triggers, time_of_day):
        """
        triggers: environmental/stochastic mood influencers
        """
        # Base cycling (sinusoidal with individual variation)
        base_cycle = math.sin(time_of_day * self.cycling_speed)
        
        # Trigger impacts
        trigger_impact = sum(triggers)
        
        # Update mood
        self.mood_state += (base_cycle * 0.1 + trigger_impact * 0.2)
        self.mood_state = clamp(self.mood_state, -1.0, 1.0)
        
        return self.mood_state
    
    def get_current_parameters(self):
        """Interpolate parameters based on mood state"""
        if self.mood_state < -0.3:
            # Depressed range
            return self.depressed_params
        elif self.mood_state > 0.3:
            # Manic range
            return self.manic_params
        else:
            # Euthymic (normal) range
            return NormalState()
```

### Mood Phase Transitions

```python
class PhaseTransition:
    """
    Model for rapid vs gradual mood transitions
    """
    def __init__(self, transition_type='gradual'):
        self.transition_type = transition_type
        self.rapid_threshold = 0.5  # Mood change rate for "rapid"
    
    def compute_transition_rate(self, current_mood, target_mood):
        delta = abs(target_mood - current_mood)
        
        if self.transition_type == 'rapid':
            # Fast cycling - quick transitions
            return delta * 0.5
        else:
            # Gradual cycling
            return delta * 0.1
```

---

## 3. Rapid Cycling Algorithms

### Definition
Rapid cycling: 4+ mood episodes per year (≥4 major depressive, manic, or hypomanic episodes)

```python
class RapidCyclingMoodModel:
    def __init__(self):
        self.cycle_frequency = 0.1  # High frequency
        self.phase_duration_min = 4  # Minimum ticks per phase
        self.phase_duration_max = 20
        
        # Rapid cycling triggers
        self.triggers = {
            'sleep_deprivation': 0.3,
            'stress': 0.2,
            'medication_noncompliance': 0.25,
            'seasonal_factors': 0.1
        }
    
    def should_transition(self, current_phase_duration):
        """Determine if mood phase should change"""
        min_duration = self.phase_duration_min
        
        if current_phase_duration < min_duration:
            return False  # Too soon to transition
        
        # Probability increases with duration
        transition_prob = (current_phase_duration - min_duration) / \
                         (self.phase_duration_max - min_duration)
        
        return random() < transition_prob
    
    def get_next_phase(self, current_phase):
        """Random but weighted phase selection"""
        phases = ['depression', 'hypomania', 'mania', 'euthymia']
        # Usually alternate, but can cycle through any
        return random.choice([p for p in phases if p != current_phase])
```

### Ultra-Rapid Cycling
```python
# Ultra-rapid: mood changes within hours or days
class UltraRapidCycling:
    def __init__(self):
        self.cycle_period = 12  # Hours
        self.amplitude_modulation = True
    
    def compute_mood(self, time_hours):
        # Multiple overlapping cycles
        primary = math.sin(time_hours / self.cycle_period * 2 * math.pi)
        secondary = 0.3 * math.sin(time_hours / (self.cycle_period/3) * 2 * math.pi)
        return clamp(primary + secondary, -1.0, 1.0)
```

---

## 4. Mood Stability Metrics

### Stability Measurement

```python
class MoodStabilityMetrics:
    def __init__(self):
        self.mood_history = []
    
    def compute_stability_score(self):
        """0.0 (stable) to 1.0 (highly unstable)"""
        if len(self.mood_history) < 10:
            return 0.0
        
        # Variance-based stability
        variance = statistics.variance(self.mood_history)
        
        # Frequency of direction changes
        direction_changes = sum(1 for i in range(1, len(self.mood_history)) 
                                if (self.mood_history[i] - self.mood_history[i-1]) *
                                (self.mood_history[i-1] - self.mood_history[i-2]) < 0)
        
        change_rate = direction_changes / len(self.mood_history)
        
        return min(1.0, variance * 0.5 + change_rate * 0.5)
    
    def compute_cycle_characteristics(self):
        """Analyze mood pattern"""
        if len(self.mood_history) < 20:
            return None
        
        # Find peaks and troughs
        peaks = [i for i in range(1, len(self.mood_history)-1) 
                 if self.mood_history[i] > self.mood_history[i-1] 
                 and self.mood_history[i] > self.mood_history[i+1]]
        
        troughs = [i for i in range(1, len(self.mood_history)-1) 
                   if self.mood_history[i] < self.mood_history[i-1] 
                   and self.mood_history[i] < self.mood_history[i+1]]
        
        return {
            'cycle_count': len(peaks),
            'avg_cycle_length': len(self.mood_history) / max(1, len(peaks)),
            'amplitude': max(self.mood_history) - min(self.mood_history),
            'polarization': sum(abs(m) for m in self.mood_history) / len(self.mood_history)
        }
```

### Clinical Relevance Metrics
- **Mood variability index**: Standard deviation of mood states
- **Episode frequency**: Transitions per time unit
- **Episode severity**: Peak intensity of manic/depressive episodes
- **Inter-episode functioning**: Performance during stable periods

---

## 5. Mixed Features & Comorbidities

### Mixed State Modeling

```python
class MixedStateModel:
    """
    Simultaneous depressive and manic features
    """
    def __init__(self):
        self.depressive_features = {
            'anhedonia': 0.6,
            'fatigue': 0.7,
            'worthlessness': 0.5
        }
        self.manic_features = {
            'racing_thoughts': 0.7,
            'irritability': 0.8,
            'increased_goal_activity': 0.6
        }
    
    def get_mixed_severity(self):
        dep_score = sum(self.depressive_features.values()) / len(self.depressive_features)
        man_score = sum(self.manic_features.values()) / len(self.manic_features)
        
        # Mixed when both elevated
        if dep_score > 0.4 and man_score > 0.4:
            return (dep_score + man_score) / 2
        return 0.0
```

---

## References

- DSM-5 Bipolar and Related Disorders
- Computational Models of Mood and Emotion (Neuropsychopharmacology)
- Reinforcement Learning and Bipolar Disorder (学术研究)
- Dynamic Systems Theory Applied to Mood Disorders
