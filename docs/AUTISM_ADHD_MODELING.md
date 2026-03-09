# Autism & ADHD Computational Modeling

This document covers computational models for autism spectrum conditions and ADHD within the Limbic-Flow architecture.

---

## 1. Autism Spectrum Modeling

### 1.1 Theory of Mind Deficits

**Theoretical Foundation**
Theory of Mind (ToM) refers to the ability to attribute mental states—beliefs, intentions, desires, knowledge—to oneself and others. Individuals on the autism spectrum often experience ToM challenges, which manifest as difficulties predicting behavior, understanding deception, or recognizing social expectations.

**Computational Approach**

```python
class TheoryOfMindModule:
    """
    Simulates Theory of Mind processing with configurable deficit modeling.
    """
    
    def __init__(self, tom_capacity=1.0, perspective_shift_cost=0.3):
        # tom_capacity: 0.0-1.0, represents ToM capability
        # perspective_shift_cost: cognitive load for perspective-taking
        self.tom_capacity = tom_capacity
        self.perspective_shift_cost = perspective_shift_cost
        self.belief_state = {}  # Agent's model of others' beliefs
    
    def predict_behavior(self, agent_id, context):
        """
        Predicts another agent's behavior based on inferred mental states.
        Returns prediction confidence based on ToM capacity.
        """
        if self.tom_capacity < 0.3:
            # Limited ToM: rely on behavioral patterns only
            return self._behavioral_prediction(agent_id, context)
        elif self.tom_capacity < 0.7:
            # Partial ToM: can infer basic beliefs
            return self._partial_tom_prediction(agent_id, context)
        else:
            # Full ToM: can model complex mental states
            return self._full_tom_prediction(agent_id, context)
    
    def infer_false_belief(self, scenario):
        """
        Simulates Sally-Anne test performance.
        Returns accuracy based on developmental level.
        """
        # Model typical vs. autistic performance
        accuracy = 0.2 + (0.6 * self.tom_capacity)
        return accuracy > 0.5
    
    def model_belief_update(self, agent_id, new_information):
        """
        Models how an agent updates their beliefs about another agent.
        Individuals with autism may show different update patterns.
        """
        # Reduced flexibility in belief updating
        update_rate = 0.5 * self.tom_capacity
        return BeliefState(agent_id, update_rate=update_rate)
```

**Modeling Parameters**
- **ToM Capacity**: 0.0-1.0 scale, affects mental state inference accuracy
- **Perspective-Taking Cost**: Cognitive load coefficient for shifting viewpoints
- **Belief Flexibility**: How readily beliefs update with new evidence

### 1.2 Perspective-Taking Algorithms

**Core Algorithm: Multi-Perspective Simulation**

```python
class PerspectiveTakingEngine:
    """
    Computes perspective-taking with configurable accuracy.
    """
    
    def __init__(self, egocentric_bias=0.5, perspective_accuracy=0.7):
        # egocentric_bias: tendency to assume others share your perspective
        # perspective_accuracy: how accurately you can model others' views
        self.egocentric_bias = egocentric_bias
        self.perspective_accuracy = perspective_accuracy
    
    def take_perspective(self, target_agent, situation):
        """
        Returns modeled perspective of target agent.
        """
        # Start with own perspective
        own_view = self.model_self_perspective(situation)
        
        # Apply egocentric bias
        biased_view = self._apply_egocentric_bias(own_view, target_agent)
        
        # Apply perspective-taking accuracy
        error = 1.0 - self.perspective_accuracy
        noise = random.gauss(0, error)
        
        return biased_view + noise
    
    def calculate_perspective_gap(self, agent_a, agent_b, situation):
        """
        Quantifies difference between two agents' perspectives.
        """
        view_a = self.take_perspective(agent_b, situation)
        view_b = self.take_perspective(agent_a, situation)
        return abs(view_a - view_b)
```

**Perspective-Taking Modes**
1. **Literal Mode**: Process exactly what others can perceive (no inference)
2. **Inferred Mode**: Infer mental states from behavior (requires ToM)
3. **Simulation Mode**: Mentally simulate being the other person

### 1.3 Social Cue Processing

**Visual/Contextual Social Cues**

```python
class SocialCueProcessor:
    """
    Processes social cues with autism-appropriate modeling.
    """
    
    def __init__(self, cue_integration_weight=0.8, facial_recognition_accuracy=0.6):
        self.cue_integration_weight = cue_integration_weight
        self.facial_recognition_accuracy = facial_recognition_accuracy
        self.cue_attention_weights = {
            'facial_expression': 0.3,
            'eye_gaze': 0.25,
            'body_language': 0.2,
            'verbal_tone': 0.15,
            'context': 0.1
        }
    
    def process_cue_bundle(self, sensory_input):
        """
        Integrates multiple social cues into coherent social interpretation.
        """
        # Check if all cue modalities are available
        available_cues = [k for k in self.cue_attention_weights.keys() 
                         if k in sensory_input]
        
        if len(available_cues) < 2:
            # Insufficient cue integration
            return self._fallback_interpretation(sensory_input)
        
        # Weighted integration
        integrated = 0.0
        weight_sum = 0.0
        
        for cue_type in available_cues:
            weight = self.cue_attention_weights[cue_type]
            cue_value = sensory_input[cue_type]
            integrated += cue_value * weight
            weight_sum += weight
        
        return integrated / weight_sum
    
    def process_implicit_social_meaning(self, statement, context):
        """
        Processes sarcasm, irony, white lies, and social norms.
        This is often challenging for autism modeling.
        """
        literal_meaning = self.extract_literal_meaning(statement)
        
        # Check for implicit meaning markers
        implicit_markers = self.detect_implicit_markers(statement, context)
        
        if implicit_markers.confidence > self.cue_integration_weight:
            return implicit_markers.meaning
        else:
            # Default to literal interpretation
            return literal_meaning
```

**Social Cue Processing Parameters**
- Cue integration weight (0-1): How well different cues combine
- Facial recognition accuracy (0-1): Ability to read faces
- Eye gaze processing (0-1): Attention to and interpretation of gaze
- Implicit meaning detection (0-1): Sarcasm, irony, white lies

### 1.4 Special Interests Modeling

```python
class SpecialInterestModule:
    """
    Models restricted, intense interests characteristic of autism.
    """
    
    def __init__(self):
        self.interests = []  # List of Interest objects
        self.interest_intensity_threshold = 0.7
        self.topic_flexibility = 0.3  # Low flexibility is typical
    
    class Interest:
        def __init__(self, topic, intensity, depth, exclusivity):
            self.topic = topic
            self.intensity = intensity  # 0-1, how consuming
            self.depth = depth          # 0-1, how detailed knowledge is
            self.exclusivity = exclusivity  # 0-1, preference for this over others
    
    def activate_interest(self, stimulus):
        """
        When stimulus matches an interest, trigger engagement.
        """
        for interest in self.interests:
            if self._stimulus_matches_interest(stimulus, interest):
                # High intensity interests capture attention
                attention_capture = interest.intensity * 0.8
                return AttentionCapture(
                    source='special_interest',
                    intensity=attention_capture,
                    duration=self._calculate_engagement_duration(interest)
                )
        return None
    
    def calculate_topic_flexibility(self, current_topic, new_topic):
        """
        Models difficulty transitioning away from special interests.
        """
        current_interest = self._find_interest(current_topic)
        new_interest = self._find_interest(new_topic)
        
        if current_interest and not new_interest:
            # Transitioning away from special interest
            transition_difficulty = (1.0 - self.topic_flexibility) * \
                                    current_interest.intensity
            return -transition_difficulty
        
        return 0.0
    
    def generate_expertise_output(self, interest):
        """
        When engaged with special interest, produce detailed knowledge.
        """
        if interest.depth > 0.7:
            return KnowledgeOutput(
                detail_level='expert',
                topics=self._generate_related_topics(interest),
                presentation_style='comprehensive'
            )
        return None
```

---

## 2. ADHD Simulation

### 2.1 Attention and Executive Function

**Core Attention Model**

```python
class AttentionExecutiveModule:
    """
    Models ADHD attention and executive function characteristics.
    """
    
    def __init__(self, attention_variance=0.4, working_memory_capacity=3,
                 inhibition_control=0.5, task_switching_cost=0.4):
        # attention_variance: variability in attention over time
        # working_memory_capacity: items in working memory (typical: 4±1)
        # inhibition_control: ability to suppress impulses (0-1)
        # task_switching_cost: penalty for switching tasks
        
        self.attention_variance = attention_variance
        self.working_memory_capacity = working_memory_capacity
        self.inhibition_control = inhibition_control
        self.task_switching_cost = task_switching_cost
        
        self.current_attention_level = 1.0
        self.attention_drift_rate = 0.0
    
    def update_attention(self, task_engagement, environmental_stimuli, time_elapsed):
        """
        Updates attention level based on multiple factors.
        """
        # Base decay over time
        time_decay = time_elapsed * 0.05 * self.attention_variance
        
        # Engagement boost or decay
        engagement_effect = task_engagement * 0.3
        
        # Environmental capture (novel stimuli)
        capture_effect = self._calculate_stimulus_capture(environmental_stimuli)
        
        # Net attention change
        self.current_attention_level += engagement_effect - time_decay + capture_effect
        self.current_attention_level = max(0.1, min(1.0, self.current_attention_level))
        
        return self.current_attention_level
    
    def _calculate_stimulus_capture(self, stimuli):
        """
        Models how novel/salient stimuli capture attention.
        Higher ADHD = more capture.
        """
        total_capture = 0.0
        for stimulus in stimuli:
            salience = stimulus.salience
            # ADHD: more susceptible to bottom-up capture
            capture = salience * (1.0 - self.inhibition_control) * 0.3
            total_capture += capture
        return total_capture
    
    def check_working_memory_load(self, items):
        """
        Returns available working memory capacity.
        """
        used = len(items)
        available = self.working_memory_capacity - used
        return {
            'used': used,
            'available': max(0, available),
            'overload': used > self.working_memory_capacity
        }
```

### 2.2 Attention Drift Modeling

```python
class AttentionDriftModel:
    """
    Models the temporal dynamics of attention decay in ADHD.
    """
    
    def __init__(self, drift_base_rate=0.15, task_relevance_sensitivity=0.5,
                 arousal_baseline=0.5):
        # drift_base_rate: baseline attention decay per time unit
        # task_relevance_sensitivity: how much task relevance slows drift
        # arousal_baseline: default arousal level (affects focus)
        
        self.drift_base_rate = drift_base_rate
        self.task_relevance_sensitivity = task_relevance_sensitivity
        self.arousal_baseline = arousal_baseline
        
        self.drift_history = []
    
    def calculate_drift(self, current_task, time_on_task, internal_stimuli):
        """
        Calculates attention drift over time.
        """
        # Base drift
        drift = self.drift_base_rate * time_on_task
        
        # Task relevance effect (more relevant = slower drift)
        relevance_factor = 1.0 - (current_task.relevance * 
                                  self.task_relevance_sensitivity)
        drift *= relevance_factor
        
        # Internal stimulus competition
        internal_compete = sum(s.intensity * 0.1 for s in internal_stimuli)
        drift += internal_compete
        
        # Arousal modulation
        arousal_effect = 1.0 - (self.arousal_baseline * 0.2)
        drift *= arousal_effect
        
        self.drift_history.append(drift)
        return drift
    
    def predict_attention_loss_point(self, task):
        """
        Predicts when attention will drop below functional threshold.
        """
        threshold = 0.3  # Below this, task engagement fails
        
        # Simplified prediction
        base_duration = threshold / self.drift_base_rate
        relevance_boost = 1.0 + task.relevance
        
        return base_duration * relevance_boost
```

### 2.3 Hyperfocus Simulation

```python
class HyperfocusModel:
    """
    Models intense, prolonged focus on high-interest tasks (ADHD hyperfocus).
    """
    
    def __init__(self, hyperfocus_threshold=0.8, hyperfocus_engagement_boost=2.0,
                 exit_difficulty=0.7):
        # hyperfocus_threshold: interest level that triggers hyperfocus
        # hyperfocus_engagement_boost: multiplier for engagement once triggered
        # exit_difficulty: how hard to break out of hyperfocus
        
        self.hyperfocus_threshold = hyperfocus_threshold
        self.engagement_boost = hyperfocus_engagement_boost
        self.exit_difficulty = exit_difficulty
        
        self.is_hyperfocused = False
        self.hyperfocus_start_time = None
        self.current_task = None
    
    def check_hyperfocus_trigger(self, task_interest, previous_attention):
        """
        Determines if hyperfocus should activate.
        """
        if (task_interest > self.hyperfocus_threshold and 
            previous_attention > 0.6 and
            not self.is_hyperfocused):
            
            self.is_hyperfocused = True
            self.hyperfocus_start_time = current_time()
            self.current_task = task
            
            return HyperfocusState(
                activated=True,
                engagement_multiplier=self.engagement_boost,
                external_interruption_resistance=self.exit_difficulty
            )
        
        return HyperfocusState(activated=False)
    
    def calculate_task_absorption(self, elapsed_time):
        """
        Models how absorption increases over hyperfocus duration.
        """
        if not self.is_hyperfocused:
            return 0.0
        
        # Absorption increases over time (up to a cap)
        absorption = min(1.0, elapsed_time * 0.1 * self.engagement_boost)
        return absorption
    
    def external_interruption_efficacy(self, interruption_strength):
        """
        Calculates whether external interruption breaks hyperfocus.
        """
        if not self.is_hyperfocused:
            return interruption_strength > 0.5
        
        # Higher exit_difficulty = more resistant to interruption
        resistance = self.exit_difficulty
        effective_strength = interruption_strength * (1.0 - resistance)
        
        return effective_strength > 0.7
```

### 2.4 Impulsivity Algorithms

```python
class ImpulsivityModel:
    """
    Models impulse control challenges in ADHD.
    """
    
    def __init__(self, delay_discounting_rate=0.3, response_inhibition=0.4,
                 reward_sensitivity=0.7, pre_potent_response_inhibition=0.5):
        # delay_discounting_rate: how quickly future rewards lose value
        # response_inhibition: ability to stop initiated response
        # reward_sensitivity: how attractive rewards are
        # pre_potent_response_inhibition: stop habitual responses
        
        self.delay_discounting_rate = delay_discounting_rate
        self.response_inhibition = response_inhibition
        self.reward_sensitivity = reward_sensitivity
        self.pre_potent_inhibition = pre_potent_response_inhibition
    
    def calculate_delay_discounting(self, reward_value, delay):
        """
        Models how much future rewards are discounted (hyperbolic).
        """
        # Hyperbolic discounting: V = A / (1 + k*D)
        discounted_value = reward_value / (1 + self.delay_discounting_rate * delay)
        return discounted_value
    
    def evaluate_impulse(self, impulse, context):
        """
        Evaluates whether an impulse is acted upon.
        """
        # Impulse strength
        impulse_strength = impulse.intensity * self.reward_sensitivity
        
        # Inhibition capacity
        inhibition_available = self.response_inhibition * context.fatigue_factor
        
        # Decision
        if impulse_strength > inhibition_available:
            return ImpulseDecision(
                acted=True,
                impulse_strength=impulse_strength,
                inhibition_used=inhibition_available
            )
        else:
            return ImpulseDecision(
                acted=False,
                impulse_strength=impulse_strength,
                inhibition_used=inhibition_available,
                suppressed=True
            )
    
    def pre_potent_response_override(self, habitual_response, new_demand):
        """
        Models stopping a pre-potent (automatic) response.
        """
        # Pre-potent responses are hard to inhibit
        override_strength = self.pre_potent_inhibition * 0.5
        
        return new_demand.strength > override_strength
    
    def generate_stop_signal_response(self, stop_signal_timing):
        """
        Models Stop-Signal Task performance.
        """
        # Earlier stop signals = harder to inhibit
        timing_factor = 1.0 - (stop_signal_timing / 1000)  # ms to factor
        success_probability = self.response_inhibition * timing_factor
        
        return random.random() < success_probability
```

---

## Integration: Combined ASD-ADHD Model

```python
class NeurodevelopmentalProfile:
    """
    Combined model for agents with autism and/or ADHD characteristics.
    """
    
    def __init__(self, autism_traits=None, adhd_traits=None):
        self.autism = autism_traits or AutismTraits()
        self.adhd = adhd_traits or ADHDTraits()
        
        # Comorbidity interaction effects
        self.comorbidity_modifiers = self._calculate_comorbidity_effects()
    
    def _calculate_comorbidity_effects(self):
        """
        Models how autism and ADHD traits interact.
        """
        return {
            # ADHD can mask autism social difficulties
            'social_compensation': self.adhd.inhibition_control * 0.2,
            # Autism special interests may align with ADHD hyperfocus
            'interest_alignment': self.autism.interest_depth * 0.3,
            # Combined executive function challenges
            'executive_drain': (1.0 - self.adhd.inhibition_control) * 
                              (1.0 - self.autism.flexibility) * 0.4
        }
    
    def process_social_situation(self, situation):
        """
        Combined processing with trait interactions.
        """
        # Autism-based processing
        autism_result = self.autism.process_social(situation)
        
        # ADHD distraction effects
        if self.adhd.current_attention_level < 0.5:
            # Attention lapses affect social processing
            autism_result.confidence *= self.adhd.current_attention_level
        
        return autism_result
    
    def select_behavior(self, options):
        """
        Behavior selection with neurodevelopmental profile.
        """
        # Calculate activation for each option
        for option in options:
            base_activation = option.activation
            
            # Autism: favor familiar/preferred
            autism_mod = self.autism.interest_match(option) * 0.3
            
            # ADHD: favor immediate reward
            adhd_mod = self.adhd.immediate_reward_boost(option)
            
            option.final_activation = base_activation + autism_mod + adhd_mod
        
        # Apply impulsivity filter
        selected = max(options, key=lambda x: x.final_activation)
        
        # Check if impulse control allows selection
        decision = self.adhd.evaluate_impulse(selected.impulse)
        
        return selected if decision.acted else None
```

---

## Configuration Examples

```python
# Autism-only profile (high-functioning)
autism_profile = NeurodevelopmentalProfile(
    autism_traits=AutismTraits(
        tom_capacity=0.6,
        perspective_accuracy=0.7,
        cue_integration=0.75,
        special_interest_intensity=0.8,
        flexibility=0.4
    ),
    adhd_traits=None
)

# ADHD-only profile
adhd_profile = NeurodevelopmentalProfile(
    autism_traits=None,
    adhd_traits=ADHDTraits(
        attention_variance=0.5,
        working_memory_capacity=3,
        inhibition_control=0.4,
        delay_discounting=0.4,
        hyperfocus_threshold=0.75
    )
)

# Combined ASD-ADHD profile
combined_profile = NeurodevelopmentalProfile(
    autism_traits=AutismTraits(
        tom_capacity=0.45,
        perspective_accuracy=0.55,
        cue_integration=0.6,
        special_interest_intensity=0.85,
        flexibility=0.3
    ),
    adhd_traits=ADHDTraits(
        attention_variance=0.6,
        working_memory_capacity=2,
        inhibition_control=0.35,
        delay_discounting=0.5,
        hyperfocus_threshold=0.7
    )
)
```

---

## Research Considerations

### Validation Approaches
- Compare model behavior against empirical data from ASD/ADHD populations
- Use established cognitive tasks (ToM tasks, continuous performance tests, go/no-go tasks)
- Consider self-report and observer ratings for calibration

### Ethical Considerations
- Avoid pathologizing neurodiversity; model as variant cognitive styles
- Ensure models don't reinforce harmful stereotypes
- Consider accessibility benefits when modeling differences

### Extensions
- Temporal dynamics: How traits manifest across development
- Context sensitivity: Situational variation in trait expression
- Individual differences: Within-group variation modeling
- Intervention simulation: Modeling effects of supports/strategies
