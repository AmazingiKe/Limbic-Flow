# Emotion Regulation Algorithms

## Overview

Emotion regulation refers to the processes by which individuals influence which emotions they have, when they have them, and how they experience and express them. Implementing emotion regulation in AI involves modeling different strategies and their computational representations.

## Key Concepts

### 1. Cognitive Reappraisal

Cognitive reappraisal is an antecedent-focused strategy that involves changing the interpretation of an emotional stimulus to modify its emotional impact.

**Computational Model:**
- **Appraisal Decomposition**: Break down emotional meaning into appraisal dimensions
- **Reappraisal Operators**: Functions that transform appraisal values
- **Impact Calculator**: Predict emotional response after reappraisal

```python
class CognitiveReappraiser:
    def __init__(self):
        self.reappraisal_operators = {
            'reframing': self.reframe_meaning,
            'distancing': self.psychological_distance,
            'positive_refocusing': self.redirect_attention,
            'perspective_taking': self.alternative_viewpoint
        }
    
    def reappraise(self, emotion_state, strategy='reframing'):
        """Apply cognitive reappraisal to modify emotional state"""
        operator = self.reappraisal_operators.get(strategy)
        if operator:
            return operator(emotion_state)
        return emotion_state
    
    def reframe_meaning(self, state):
        """Change the meaning of emotional stimulus"""
        # Reduce threat appraisal, increase opportunity appraisal
        new_threat = state['threat_appraisal'] * 0.3
        new_opportunity = state.get('opportunity_appraisal', 0) + 0.3
        new_valence = state['valence'] + (new_opportunity - new_threat) * 0.5
        return {**state, 'threat_appraisal': new_threat, 'valence': new_valence}
```

### 2. Emotion Suppression vs Expression

Two response-focused strategies with different computational implications:

- **Expressive Suppression**: Inhibits behavioral/emotional expression
- **Emotion Expression**: Allows natural emotional response

```python
class SuppressionController:
    def __init__(self, suppression_cost=0.2):
        self.cost = suppression_cost  # Cognitive load penalty
    
    def suppress(self, emotional_response):
        """Suppress expressive output while maintaining internal state"""
        return {
            'external_output': 0.0,  # Suppressed
            'internal_state': emotional_response['internal'],
            'cognitive_load': self.cost,
            'suppression_flag': True
        }
    
    def express(self, emotional_response):
        """Allow natural emotional expression"""
        return {
            'external_output': emotional_response['external'],
            'internal_state': emotional_response['internal'],
            'cognitive_load': 0.0,
            'suppression_flag': False
        }
```

### 3. Mindfulness-Based Emotion Regulation

Mindfulness involves non-judgmental awareness of present-moment experience.

**Implementation Components:**
- **Attentional Deployment**: Directing attention to present moment
- **Decentering**: Observing emotions without identification
- **Acceptance**: Allowing emotions without suppression

```python
class MindfulnessRegulator:
    def __init__(self):
        self.present_moment_weight = 0.8
        self.acceptance_level = 0.7
    
    def regulate(self, emotional_state):
        """Apply mindfulness-based regulation"""
        # 1. Decentering: Observe emotion as temporary state
        decentered_state = {
            'emotion': emotional_state['emotion'],
            'observation': 'temporary_state',
            'identification': 'reduced'  # Less self-identification
        }
        
        # 2. Present focus: Reduce rumination about past/future
        present_focus = min(1.0, emotional_state.get('past_focus', 0) * 0.5 + 
                                 emotional_state.get('future_focus', 0) * 0.5)
        
        # 3. Acceptance: Allow emotion without resistance
        acceptance_modulation = (1 - self.acceptance_level) * emotional_state['intensity']
        
        return {
            **emotional_state,
            'decentered': decentered_state,
            'present_focus': 1 - present_focus,
            'intensity': emotional_state['intensity'] - acceptance_modulation,
            'regulation_strategy': 'mindfulness'
        }
```

## Emotion Regulation Strategy Selection

### Strategy Taxonomy

| Strategy Type | Example | Processing | Time Scale |
|--------------|---------|------------|------------|
| Antecedent-Focused | Reappraisal, Acceptance | Before emotion peaks | Slower |
| Response-Focused | Suppression, Expression | After emotion generated | Faster |
| Deployment | Distraction, Mindfulness | During processing | Real-time |

### Adaptive Strategy Selection

```python
class EmotionRegulationSelector:
    def __init__(self):
        self.strategies = {
            'cognitive_reappraisal': CognitiveReappraiser(),
            'suppression': SuppressionController(),
            'mindfulness': MindfulnessRegulator(),
            'distraction': DistractionRedirector()
        }
        self.context_weights = {
            'social': {'suppression': 0.3, 'reappraisal': 0.7},
            'solitary': {'suppression': 0.1, 'reappraisal': 0.9},
            'stressful': {'mindfulness': 0.6, 'reappraisal': 0.4}
        }
    
    def select_strategy(self, emotion, context):
        """Select optimal regulation strategy based on context"""
        context_type = context.get('type', 'solitary')
        weights = self.context_weights.get(context_type, {'reappraisal': 1.0})
        
        # Consider emotion intensity
        if emotion['intensity'] > 0.8:
            weights['mindfulness'] = weights.get('mindfulness', 0) + 0.3
        
        # Return weighted random selection
        return self.weighted_choice(weights)
```

## Implementation Architecture

### Regulation Pipeline

```
Emotional Stimulus → [Appraisal Module] → [Emotion Generation]
                                              ↓
                              [Regulation Selector]
                                              ↓
                    ┌───────────┬─────────────┼─────────────┐
                    ↓           ↓             ↓             ↓
              [Reappraisal] [Suppression] [Mindfulness] [Distraction]
                    ↓           ↓             ↓             ↓
                    └───────────┴─────────────┴─────────────┘
                                              ↓
                              [Regulated Response]
```

### Integration with Limbic-Flow

```python
class EmotionRegulationModule:
    """Main emotion regulation controller"""
    
    def __init__(self, config):
        self.selector = EmotionRegulationSelector()
        self.strategies = self.selector.strategies
        self.enabled_strategies = config.get('enabled', list(self.strategies.keys()))
        self.auto_regulate = config.get('auto_regulate', True)
        self.intensity_threshold = config.get('intensity_threshold', 0.6)
    
    def process(self, emotional_state, context):
        """Process emotional state through regulation"""
        # Check if regulation needed
        if not self.auto_regulate or emotional_state['intensity'] < self.intensity_threshold:
            return emotional_state, None
        
        # Select and apply strategy
        strategy_name = self.selector.select_strategy(emotional_state, context)
        strategy = self.strategies[strategy_name]
        
        # Apply regulation
        if hasattr(strategy, 'regulate'):
            regulated = strategy.regulate(emotional_state)
        elif hasattr(strategy, 'reappraise'):
            regulated = strategy.reappraise(emotional_state)
        else:
            regulated = strategy.apply(emotional_state)
        
        return regulated, strategy_name
```

## Research Basis

### Key Papers

1. **Gross (1998)**: Process model of emotion regulation - foundational framework
2. **Webb et al. (2012)**: Meta-analysis of emotion regulation strategies
3. **Aldao et al. (2010)**: Emotion regulation as a transdiagnostic process
4. **Siegle et al. (2002)**: Cognitive emotion regulation - attention deployment

### Computational Psychiatry Connections

- **Depression/Anxiety**: Dysregulated emotion processing
- **BPD**: Difficulty with emotional identification and regulation
- **PTSD**: Impaired regulation of trauma-related emotions

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `auto_regulate` | Enable automatic regulation | true |
| `intensity_threshold` | Emotion intensity to trigger regulation | 0.6 |
| `strategy_weights` | Default strategy preferences | balanced |
| `mindfulness_acceptance` | Acceptance level for mindfulness | 0.7 |
| `suppression_cost` | Cognitive cost of suppression | 0.2 |

## Usage Examples

### Example 1: Cognitive Reappraisal

```python
reappraiser = CognitiveReappraiser()
emotion_state = {'emotion': 'fear', 'intensity': 0.7, 'valence': -0.5, 'threat_appraisal': 0.8}
regulated = reappraiser.reappraise(emotion_state, 'reframing')
# Result: reduced threat appraisal, improved valence
```

### Example 2: Mindfulness Regulation

```python
mindfulness = MindfulnessRegulator()
emotion_state = {'emotion': 'anger', 'intensity': 0.8, 'rumination': 0.6}
regulated = mindfulness.regulate(emotion_state)
# Result: decentered observation, reduced intensity through acceptance
```

## Future Extensions

1. **Strategy Learning**: Learn optimal strategies from user feedback
2. **Individual Differences**: Model personality-based regulation styles
3. **Cultural Adaptations**: Different regulation norms across cultures
4. **Therapeutic Integration**: Connect to CBT/DBT treatment protocols
