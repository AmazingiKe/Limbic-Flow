# Multi-Agent Emotional Systems

> Research document for Limbic-Flow emotional architecture

This document covers the dynamics of emotion in multi-agent systems—including group psychology, social contagion, collective emotional states, and ethical emotions that govern moral behavior and empathy.

---

## 1. Group Dynamics and Emotional Systems

### Foundations

Group dynamics refer to the patterns of interaction, influence, and emotional exchange within collectives. In multi-agent systems, understanding group dynamics is essential for:

- Coordinated decision-making
- Conflict detection and resolution
- Team cohesion maintenance
- Collective goal pursuit

### Key Theoretical Frameworks

#### Emotional Contagion Theory (Hatfield et al.)
The automatic and unconscious transfer of emotional states between individuals:

```
A's emotional state → A's expressive behaviors → B's mimicry → B's emotional experience
```

**Mechanisms:**
- Limbic resonance: synchronous emotional exchanges
- Limbic regulation: emotional co-regulation in relationships
- Mirror neuron activation (hypothesized)

#### Group Emotional Climate (GEC)
The shared emotional atmosphere of a group, characterized by:

- **Emotional valence**: positive vs. negative
- **Emotional intensity**: high vs. low arousal
- **Emotional homogeneity**: uniform vs. diverse across members
- **Emotional stability**: stable vs. volatile over time

### Computational Models

#### Emotional Contagion in Multi-Agent Systems

```
For each agent i in group G:
  For each neighbor j in G:
    influence = w_contagion × similarity(emotion_i, emotion_j)
    emotion_i ← emotion_i + influence × (emotion_j - emotion_i)
```

Parameters:
- `w_contagion`: contagion strength (varies by relationship trust)
- `similarity()`: emotional similarity function
- Temporal decay: older emotional states have less influence

#### Group Polarization (Casual Fragmentation Risk)
- Groups tend toward more extreme positions over time
- Emotional convergence can amplify this effect
- Counter-strategies: devil's advocate, diverse membership, cooling periods

### Implementation Considerations

| Factor | Modeling Approach | Impact on Emotional Dynamics |
|--------|-------------------|------------------------------|
| Group size | Sigmoid influence curve | Small groups: direct contagion; Large: opinion leaders matter more |
| Trust networks | Weighted adjacency matrix | High trust = stronger emotional contagion |
| Role hierarchy | Role-based influence weights | Leaders have disproportionate emotional impact |
| Task type | Task-emotion compatibility | Cooperative tasks increase positive contagion |

---

## 2. Social Emotional Contagion

### Mechanisms

Emotional contagion operates through multiple channels:

1. **Facial mimicry**: Seeing emotional expressions triggers corresponding muscle activity
2. **Vocal prosody**: Tonal quality conveys emotional information
3. **Body language**: Posture and movement express emotional states
4. **Behavioral synchrony**: Coordinated actions create emotional bonds
5. **Language content**: Verbal expression of emotions triggers understanding

### Computational Modeling

#### Contagion Strength Factors

```
contagion_strength(agent_i, agent_j) = 
  f(
    trust(i, j),           // Relationship quality
    exposure_time,         // Duration of interaction
    social_bond_strength,  // Historical connection
    power_distance,        // Hierarchical relationship
    cultural_context       // Collectivist vs. individualist
  )
```

#### Agent Architecture for Contagion

```
AgentEmotionalState:
  - current_emotions: Map<EmotionType, Intensity>
  - emotional_history: Queue[TimestampedEmotion]
  - susceptibility: Float  // Individual variation in contagion susceptibility
  - contagion_radius: Set<AgentID>  // Agents considered for contagion

ProcessContagion():
  for each target in contagion_radius:
    delta = calculate_emotional_delta(self, target)
    apply_emotional_change(delta)
    update_trust_based_on_contagion(target)
```

### Research Findings

- **Contagion is faster for negative emotions** (threat detection advantage)
- **Contagion strength correlates with social closeness**
- **Contagion can create feedback loops** leading to collective emotional states
- **Individual differences in susceptibility** range from 10-30% variance

### Applications in Multi-Agent Systems

- **Social robots**: Contagion used for human-robot emotional sync
- **Collaborative AI**: Agents align emotional states for better cooperation
- **Conflict detection**: Sudden emotional shifts may indicate group strain

---

## 3. Collective Mood

### Definition

Collective mood refers to the shared emotional state that emerges from group interaction, distinct from individual emotional states but influenced by them.

### Characteristics

| Property | Description |
|----------|-------------|
| **Emergence** | Not present in individuals; arises from interaction |
| **Persistence** | Can outlast individual emotional fluctuations |
| **Regulation** | Requires collective-level interventions |
| **Impact** | Shapes group behavior, decisions, performance |

### Measurement Approaches

#### Aggregate Metrics
- Mean emotional valence of group
- Emotional variance (cohesion vs. conflict)
- Rate of emotional change

#### Network Metrics
- Emotional clustering coefficient
- Centrality of emotional leaders
- Emotional synchronization indices

### Mathematical Representation

```
CollectiveMood(t) = 
  α × mean_individual_emotions(t) 
  + β × environmental_context(t) 
  + γ × historical_mood(t-1)
  + δ × external_shocks(t)
```

Where weights reflect:
- α: current group emotional state
- β: situational factors
- γ: mood persistence
- δ: disruption events

### Types of Collective Mood

#### Positive Collective Mood
- Optimism, enthusiasm, shared purpose
- Enhanced creativity and risk-taking
- Stronger social bonds

#### Negative Collective Mood  
- Anxiety, fear, despair
- Risk aversion, conflict escalation
- Withdrawal and disengagement

#### Ambivalent Collective Mood
- Mixed emotional signals
- Unstable, prone to rapid shifts
- Complex decision-making dynamics

### Agent Implementation

```
class GroupEmotionalState:
  members: List[Agent]
  collective_valence: float
  collective_arousal: float
  mood_stability: float  // How resistant to change
  mood_inertia: float   // How much past mood persists
  
  update_collective_mood():
    # Weighted average with recency bias
    recent_emotions = get_emotions_last_n_steps(5)
    weights = exponential_decay_weights()
    collective_valence = weighted_average(recent_emotions, weights)
    collective_arousal = weighted_std_dev(recent_emotions)
```

---

## 4. Ethical Emotions

Ethical emotions are moral affective responses that guide prosocial behavior, enforce social norms, and maintain cooperative relationships. They are essential for agents operating in social environments.

### 4.1 Guilt and Shame Modeling

#### Theoretical Distinction

| Aspect | Guilt | Shame |
|--------|-------|-------|
| **Focus** | Behavior (I did something bad) | Self (I am bad) |
| **Social dimension** | Private; relates to others' judgment | Public; relates to exposed identity |
| **Behavioral outcome** | Reparation, apology | Withdrawal, hiding |
| **Trigger** | Violation of personal standards | Exposure of violation |

#### Computational Models

##### Guilt Schema

```
GuiltTrigger(condition):
  violation = detect_norm_violation(agent, action)
  if violation AND agent.has_standards():
    severity = calculate_severity(violation)
    victim_impact = assess_damage(violation)
    guilt_intensity = f(severity, victim_impact, relationship_importance)
    trigger_reparation_behavior(guilt_intensity)
```

##### Shame Schema

```
ShameTrigger(condition):
  violation = detect_norm_violation(agent, action)
  if violation AND violation_is_observed():
    public_exposure = check_visibility(violation)
    if public_exposure > threshold:
      shame_intensity = f(severity, audience_importance)
      trigger_withdrawal_behavior(shame_intensity)
```

#### Implementation in Agents

```python
class EthicalEmotionProcessor:
    def process_guilt(self, violation, context):
        # Check if agent has internal standards
        if not self.agent.moral_frameworks:
            return 0.0
            
        # Calculate guilt based on multiple factors
        harm_assessment = self.assess_harm(violation)
        standard_violation = self.check_standard_alignment(violation)
        repair_possible = self.can_repair(violation)
        
        guilt = (
            0.4 * harm_assessment +
            0.3 * standard_violation +
            0.3 * (1.0 if repair_possible else 0.0)
        )
        
        # Guilt may motivate apology, compensation, or behavior change
        if guilt > self.threshold:
            self.agent.queue_action("apologize", guilt)
            self.agent.queue_action("compensate", guilt)
            
        return guilt
    
    def process_shame(self, violation, context):
        # Shame requires public exposure
        if not context.is_public:
            return 0.0
            
        audience_size = context.observer_count
        audience_importance = self.assess_audience(context.observers)
        
        shame = audience_size * audience_importance * violation_severity
        
        # Shame may cause withdrawal or cover-up
        if shame > self.threshold:
            self.agent.queue_action("withdraw", shame)
            
        return shame
```

### 4.2 Moral Emotions

Moral emotions are those directly tied to the welfare, rights, or dignity of others. They motivate prosocial behavior and deter antisocial behavior.

#### Taxonomy of Moral Emotions

| Category | Emotions | Function |
|----------|----------|----------|
| **Other-condemning** | Contempt, anger, disgust | Enforce social norms, punish violators |
| **Self-conscious** | Guilt, shame, pride | Regulate personal conduct |
| **Other-suffering** | Compassion, empathy, sympathy | Prosocial motivation |
| **Other-praising** | Gratitude, admiration, reverence | Reinforce moral behavior |

#### Modeling Moral Emotions in Agents

```
MoralEmotionGenerator:
  inputs:
    - observed_behavior: Action
    - moral_standards: Set[Rule]
    - victim_identification: Agent
    - relationship_context: Context
    
  process:
    1. Check if observed_behavior violates moral_standards
    2. Identify affected parties
    3. Calculate moral emotional response based on:
       - Violation severity
       - Relationship to violator/victim
       - Cultural/moral framework
    4. Generate action tendencies
    
  outputs:
    - moral_emotion: Emotion
    - action_tendency: Action
    - intensity: float
```

### 4.3 Empathic Concern

#### Definition

Empathic concern (or empathy) is the ability to understand and share the emotional states of others. It involves:

- **Cognitive empathy**: Understanding another's perspective
- **Affective empathy**: Sharing their emotional state
- **Empathic concern**: Motivation to help based on empathy

#### Computational Models

##### Empathy Calculation

```
Empathy(agent_i, agent_j) =
  perspective_taking(agent_i, agent_j) × 
  emotional_similarity(emotion_i, emotion_j) × 
  relationship_bond(agent_i, agent_j)
```

##### Empathic Concern Generation

```
EmpathicConcern(agent_i, victim_j):
  1. Detect distress_signal(victim_j)
  2. Calculate empathy = Empathy(agent_i, victim_j)
  3. Calculate victim_vulnerability = assess_vulnerability(victim_j)
  4. Calculate cost_to_help = assess_costs(agent_i, action)
  
  concern = empathy × victim_vulnerability
  
  if concern > help_threshold AND cost_to_help < refusal_threshold:
    generate_help_behavior(concern, victim_vulnerability)
```

#### Agent Architecture

```python
class EmpathicConcernModule:
    def __init__(self, agent):
        self.agent = agent
        self.empathy_capacity = 0.8  # Max emotional load from others
        self.perspective_ability = 0.7  # Accuracy of perspective-taking
    
    def process_observed_emotion(self, other_agent, other_emotion):
        # Step 1: Perspective-taking (cognitive empathy)
        inferred_state = self.perspective_take(other_agent)
        
        # Step 2: Affective resonance (emotional contagion)
        emotional_resonance = self.emotional_contagion(other_emotion)
        
        # Step 3: Empathic concern calculation
        concern = (
            self.agent.empathy_factor * 
            inferred_state.intensity * 
            emotional_resonance
        )
        
        # Step 4: Generate prosocial action tendency
        if concern > self.agent.help_threshold:
            return self.generate_help_action(concern, other_agent)
        
        return None
```

---

## 5. Integration: Multi-Agent Ethical Emotional System

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Agent Emotional System                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │Individual│    │  Group   │    │ Ethical  │                  │
│  │Emotional │◄──►│ Dynamics │◄──►│ Emotions │                  │
│  │ State    │    │          │    │          │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
│       │               │               │                       │
│       ▼               ▼               ▼                       │
│  ┌─────────────────────────────────────────────┐               │
│  │         Emotional Contagion Network         │               │
│  │  (Weighted edges based on trust/influence)  │               │
│  └─────────────────────────────────────────────┘               │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────┐               │
│  │         Collective Mood State               │               │
│  │  (Valence, Arousal, Stability, Homogeneity) │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Interaction Flow

1. **Individual emotions** influence and are influenced by group dynamics
2. **Social contagion** transfers emotional states between agents
3. **Collective mood** emerges and feeds back to individuals
4. **Ethical emotions** modulate behavior based on group norms and empathy
5. **Moral emotions** trigger prosocial or sanctioning behaviors

### Key Algorithms

#### Emotional Sync Algorithm
```python
def emotional_sync(group, dt):
    for i in group.agents:
        for j in group.agents:
            if i == j: continue
            
            trust = group.trust_matrix[i.id][j.id]
            similarity = cosine_similarity(i.emotions, j.emotions)
            
            influence = trust * similarity * group.contagion_rate
            
            # Apply emotional influence
            i.emotions += influence * (j.emotions - i.emotions) * dt
```

#### Ethical Response Generator
```python
def ethical_response(agent, event, group_norms):
    violation = check_violation(event, group_norms)
    
    if violation:
        # Determine ethical emotions
        guilt = agent.process_guilt(violation)
        shame = agent.process_shame(violation, event.is_public)
        anger = agent.process_moral_outrage(violation, event.victim)
        
        # Generate response based on emotion intensities
        response = select_ethical_response(
            [guilt, shame, anger], 
            agent.empathic_capability
        )
        return response
    
    return None
```

---

## 6. Summary & Recommendations

### Key Takeaways

1. **Emotional contagion is fundamental** to group emotional dynamics—agents must model both receiving and transmitting emotions

2. **Collective mood is emergent**—it cannot be reduced to individual emotions but requires group-level representation

3. **Ethical emotions are essential for social agents**:
   - Guilt/shame prevent harmful behavior
   - Moral emotions enforce group norms
   - Empathic concern drives prosocial action

4. **Cultural variation matters**—emotional expression norms, guilt/shame distinctions, and empathy patterns vary across cultures

### Implementation Priorities

| Priority | Component | Rationale |
|----------|-----------|-----------|
| 1 | Emotional contagion | Foundation for group dynamics |
| 2 | Collective mood tracking | Enable group-level emotional awareness |
| 3 | Basic guilt/shame | Essential for moral agent behavior |
| 4 | Empathic concern | Enables prosocial responses |
| 5 | Moral emotion taxonomy | Rich ethical behavior |

### Future Research Directions

- [ ] Cross-cultural emotional norms modeling
- [ ] Long-term trust evolution and its impact on contagion
- [ ] Ethical emotion resolution (competing moral emotions)
- [ ] Collective mood intervention strategies
- [ ] Emotional memory and its influence on group dynamics

---

*Document Version: 1.0*
*Related: LANGUAGE_THOUGHT.md, DECISION_MAKING.md*
