# Reward Learning & Motivation

## Overview

This document covers computational models of motivation and reward learning, drawing from dopamine neuroscience and reinforcement learning theory. These mechanisms are essential for modeling goal-directed behavior in AI agents.

---

## 1. Dopamine Systems

### The Reward Pathway

Dopamine is central to motivation and reward processing. Key pathways:

| Pathway | Function | Brain Region |
|---------|----------|--------------|
| Mesolimbic | Reward, motivation | VTA → Nucleus Accumbens |
| Mesocortical | Cognition, decision-making | VTA → Prefrontal Cortex |
| Nigrostriatal | Motor control | SN → Striatum |
| Tuberoinfundibular | Hormone regulation | Hypothalamus → Pituitary |

### Computational Dopamine Model

```python
class DopamineSystem:
    """
    Simplified dopamine modulation for reward learning
    """
    def __init__(self):
        # Baseline dopamine levels
        self.baseline_tonic = 0.5
        self.phasic_peak = 1.0
        
        # Dopamine parameters
        self.release_magnitude = 1.0
        self.reuptake_rate = 0.1
        self.degradation_rate = 0.05
    
    def compute_phasic_response(self, reward_prediction_error):
        """Phasic dopamine burst for unexpected rewards"""
        if reward_prediction_error > 0:
            # Unexpected reward → dopamine burst
            return self.phasic_peak * reward_prediction_error
        else:
            # Missed expected reward → dopamine dip
            return reward_prediction_error * 0.5
    
    def update_dopamine_level(self, current_level, prediction_error):
        """Update dopamine state"""
        phasic = self.compute_phasic_response(prediction_error)
        
        # Tonic baseline + phasic response - reuptake
        new_level = (self.baseline_tonic + phasic - 
                    current_level * self.reuptake_rate)
        
        return max(0.0, min(1.0, new_level))
```

---

## 2. Reward Prediction Error (RPE)

### The Temporal Difference Error

Reward Prediction Error is the difference between expected and actual reward:

```
RPE = Actual Reward - Expected Reward
```

This is the core teaching signal in reinforcement learning (δ in TD learning).

### Implementation

```python
class RewardPredictionError:
    """
    TD(λ) learning with eligibility traces
    """
    def __init__(self, alpha=0.1, gamma=0.9, lambda_=0.8):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.lambda_ = lambda_  # Eligibility trace decay
        
        self.value_function = {}  # State → value
        self.eligibility_traces = {}
    
    def compute_rpe(self, state, action, reward, next_state):
        """TD error: δ = r + γV(s') - V(s)"""
        current_value = self.get_value(state, action)
        next_value = self.get_value(next_state, None) or 0
        
        # RPE = actual - expected
        rpe = reward + self.gamma * next_value - current_value
        
        return rpe
    
    def update(self, state, action, rpe):
        """Update value function using RPE"""
        # Simple TD(0) update
        current = self.get_value(state, action)
        new_value = current + self.alpha * rpe
        self.set_value(state, action, new_value)
        
        return new_value
    
    def get_value(self, state, action):
        key = (state, action) if action else state
        return self.value_function.get(key, 0.0)
    
    def set_value(self, state, action, value):
        key = (state, action) if action else state
        self.value_function[key] = value
```

### RPE Signals in Different Scenarios

| Scenario | RPE Signal | Dopamine Response |
|----------|-----------|-------------------|
| Unexpected reward | Positive | Burst |
| Expected reward received | Zero | No change |
| Expected reward missed | Negative | Dip |
| Better-than-expected | Positive | Burst |
| Worse-than-expected | Negative | Dip |

---

## 3. Intrinsic vs Extrinsic Motivation

### Comparison

| Feature | Extrinsic | Intrinsic |
|---------|-----------|-----------|
| Source | External rewards | Internal satisfaction |
| Driver | Environmental feedback | Curiosity, mastery |
| Learning | Instrumental | Self-determination |
| Persistence | Dependent on rewards | Self-sustaining |
| Examples | Money, praise, food | Learning, exploration |

### Implementation: Intrinsic Motivation

```python
class IntrinsicMotivation:
    """
    Intrinsic motivation based on:
    - Curiosity (novelty-seeking)
    - Competence (mastery)
    - Autonomy (self-direction)
    """
    def __init__(self):
        # Curiosity parameters
        self.novelty_weight = 0.3
        self.information_gain_weight = 0.2
        
        # Competence parameters
        self.mastery_threshold = 0.8
        self.challenge_seeking = 0.5
        
        # State tracking
        self.visited_states = set()
        self.skill_levels = {}
    
    def compute_intrinsic_reward(self, state, action, knowledge_state):
        """Combined intrinsic motivation signal"""
        # Novelty reward
        novelty = self.compute_novelty(state)
        
        # Information gain (curiosity)
        info_gain = self.compute_information_gain(state, knowledge_state)
        
        # Competence/flow (challenge-skill balance)
        competence = self.compute_competence_reward(state)
        
        total = (self.novelty_weight * novelty + 
                self.information_gain_weight * info_gain +
                competence)
        
        return total
    
    def compute_novelty(self, state):
        """Novelty as inverse of visit frequency"""
        visits = sum(1 for s in self.visited_states if s == state)
        return 1.0 / (1.0 + visits)
    
    def compute_information_gain(self, state, model):
        """Expected information gain from exploring this state"""
        # Simplified: uncertainty reduction
        uncertainty = model.get_uncertainty(state)
        return uncertainty
    
    def compute_competence_reward(self, state):
        """Flow state: challenge matches skill"""
        skill = self.skill_levels.get(state, 0.5)
        challenge = self.estimate_challenge(state)
        
        # Optimal flow when challenge ≈ skill
        gap = abs(challenge - skill)
        if gap < 0.1:
            return 0.5  # Flow state
        elif challenge > skill:
            return 0.2  # Anxiety
        else:
            return 0.1  # Boredom
```

### Combined Motivation System

```python
class MotivationSystem:
    """
    Integrates intrinsic and extrinsic motivation
    """
    def __init__(self):
        self.extrinsic = ExtrinsicMotivation()
        self.intrinsic = IntrinsicMotivation()
        
        # Balance parameters
        self.extrinsic_weight = 0.6
        self.intrinsic_weight = 0.4
        
        # Self-determination theory components
        self.autonomy_factor = 1.0
        self.relatedness_factor = 1.0
    
    def compute_total_reward(self, state, action, extrinsic_reward, knowledge):
        """Combined reward signal"""
        ext = self.extrinsic_weight * extrinsic_reward
        int_ = self.intrinsic_weight * self.intrinsic.compute_intrinsic_reward(
            state, action, knowledge
        )
        
        # Apply SDT factors
        sdt_multiplier = (self.autonomy_factor + self.relatedness_factor) / 2
        
        return (ext + int_) * sdt_multiplier
    
    def update_motivation_weights(self, feedback):
        """
        Adaptively adjust intrinsic/extrinsic balance
        Based on environmental feedback and depletion
        """
        if feedback.get('extrinsic_available', True):
            self.extrinsic_weight = min(0.9, self.extrinsic_weight + 0.05)
        else:
            self.intrinsic_weight = min(0.9, self.intrinsic_weight + 0.1)
        
        # Normalize
        total = self.extrinsic_weight + self.intrinsic_weight
        self.extrinsic_weight /= total
        self.intrinsic_weight /= total
```

---

## 4. Goal-Directed Behavior

### Behavior Types

| Type | Characteristic | Model |
|------|----------------|-------|
| Habitual | Stimulus-response, automatic | Model-free RL |
| Goal-directed | Outcome-based, deliberative | Model-based RL |

### Implementation: Goal-Directed Planning

```python
class GoalDirectedBehavior:
    """
    Model-based RL for goal-directed behavior
    """
    def __init__(self):
        self.goal_state = None
        self.planning_horizon = 5
        
        # Mental simulation
        self.transition_model = {}  # (state, action) → [(next_state, prob)]
        self.reward_model = {}     # (state, action) → reward
    
    def plan(self, current_state, available_actions):
        """
        Forward planning to achieve goal
        Uses Monte Carlo Tree Search or lookahead
        """
        best_action = None
        best_value = float('-inf')
        
        for action in available_actions:
            value = self.simulate_action(current_state, action, 
                                         depth=0, 
                                         goal=self.goal_state)
            if value > best_value:
                best_value = value
                best_action = action
        
        return best_action
    
    def simulate_action(self, state, action, depth, goal):
        """Simulate future outcomes"""
        if depth >= self.planning_horizon or state == goal:
            return self.heuristic_estimate(state, goal)
        
        # Get predicted outcomes
        outcomes = self.transition_model.get((state, action), 
                                             [(state, 1.0)])
        
        total_value = 0
        for next_state, prob in outcomes:
            reward = self.reward_model.get((state, action), 0)
            future_value = self.simulate_action(next_state, action, 
                                                 depth + 1, goal)
            total_value += prob * (reward + 0.9 * future_value)
        
        return total_value
    
    def heuristic_estimate(self, state, goal):
        """Heuristic distance to goal"""
        if goal is None:
            return 0
        return -self.heuristic_distance(state, goal)
    
    def heuristic_distance(self, state, goal):
        """Simplified distance metric"""
        if isinstance(state, tuple) and isinstance(goal, tuple):
            return sum(abs(s - g) for s, g in zip(state, goal))
        return 0 if state == goal else 1
```

### Effort & Motivation

```python
class EffortModulation:
    """
    Effort-based decision making
    """
    def __init__(self):
        self.effort_cost = 0.2
        self.fatigue_rate = 0.01
        self.energy_level = 1.0
    
    def compute_motivation(self, outcome_value, effort_required, current_energy):
        """
        Motivation = (value - effort cost) * energy
        """
        net_value = outcome_value - (effort_required * self.effort_cost)
        
        # Energy depletion reduces motivation
        energy_factor = current_energy
        
        return net_value * energy_factor
    
    def update_energy(self, effort_spent, rest_available):
        """Update energy after action"""
        depletion = effort_spent * self.fatigue_rate
        
        if rest_available:
            recovery = 0.2
        else:
            recovery = 0
        
        self.energy_level = max(0.0, min(1.0, 
                                         self.energy_level - depletion + recovery))
```

---

## 5. Depression Effects on Reward Learning

### Anhedonia & Reward Processing

```python
class DepressionRewardEffects:
    """
    How depression affects reward learning
    """
    def __init__(self):
        self.anhedonia_factor = 0.3  # Reduced reward sensitivity
        self.negative_bias = 2.0     # Weight for negative outcomes
        self.prospection_impairment = 0.5  # Reduced future thinking
    
    def modulate_rpe(self, rpe, reward_type):
        """Modify RPE based on depression symptoms"""
        if reward_type == 'positive':
            # Reduced response to positive rewards
            return rpe * self.anhedonia_factor
        elif reward_type == 'negative':
            # Amplified response to negative rewards
            return rpe * self.negative_bias
        return rpe
    
    def reduce_goal_pursuit(self, goal_value):
        """Depression reduces pursuit of future rewards"""
        # Reduced prospection → discount future rewards more
        discount_factor = 0.5 + (1 - self.prospection_impairment) * 0.5
        return goal_value * discount_factor
```

---

## References

- Schultz, Dayan & Montague (1997) - Neural basis of reward prediction error
- Dayan & Berridge (2014) - Model-based and model-free reward learning
- Ryan & Deci (2000) - Self-Determination Theory
- Oudeyer & Kaplan (2007) - Intrinsic motivation systems
- Berridge (2007) - Neural bases of pleasure and wanting
- Affective Neuroscience (Panksepp)
