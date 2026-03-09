# Curiosity, Exploration, and Related Systems

## Overview

This document covers three interconnected motivational systems essential for adaptive AI behavior: **curiosity and exploration**, **attachment and bonding**, and **energy management**. Together, they drive agents to seek novel experiences, form meaningful relationships, and regulate resource allocation.

---

# Part 1: Curiosity and Exploration

## 1. Intrinsic Motivation

### The Nature of Curiosity

Curiosity is an **intrinsic motivation** - behavior driven by internal satisfaction rather than external rewards. Unlike extrinsic motivation (food, praise, avoidance of punishment), curiosity motivates exploration for its own sake.

### Types of Curiosity

| Type | Description | When Active |
|------|-------------|--------------|
| **Perceptual curiosity** | Driven by novel sensory patterns | When encountering new stimuli |
| **Epistemic curiosity** | Desire for knowledge and understanding | When facing information gaps |
| **Diversive curiosity** | General interest in novelty | In novel, uncertain environments |
| **Specific curiosity** | Focused interest after initial encounter | When deeper understanding needed |
| **Social curiosity** | Interest in others' minds | In social contexts |

### Curiosity in AI Systems

For artificial agents, curiosity can be operationalized as:

```
CuriosityDrive = information_gap × uncertainty × available_energy

Where:
- information_gap: difference between known and unknown (I = I_known - I_unknown)
- uncertainty: entropy or variance in predictions
- available_energy: resource availability to pursue exploration
```

---

## 2. Novelty Seeking

### The Neuroscience of Novelty

**Novelty detection** activates:

- **Dopamine system**: Novel rewards release more dopamine than familiar ones
- **Hippocampus**: Pattern separation for novel memory encoding
- **Prefrontal cortex**: Attention allocation to novel stimuli
- **Locus coeruleus**: Norepinephrine release signals novelty, enhancing arousal

### Novelty Dimensions

| Dimension | Description | Example |
|-----------|-------------|---------|
| **Stimulus novelty** | New sensory features | New color, sound |
| **Contextual novelty** | New environment | New room |
| **Temporal novelty** | Changes over time | Return to familiar place after change |
| **Combinatorial novelty** | New arrangements of known elements | New recipe |
| **Conceptual novelty** | New ideas/relationships | Learning a theory |

### Novelty-Seeking Algorithm

```typescript
interface NoveltySystem {
  memory: Map<string, ExposureCount>;
  noveltySensitivity: number;    // Individual variation
  habituationRate: number;       // How fast novelty wears off
  maxNoveltyBonus: number;       // Ceiling for novelty reward
}

function calculateNoveltyReward(stimulus: Stimulus, system: NoveltySystem): number {
  const key = getStimulusSignature(stimulus);
  const exposure = system.memory.get(key) || 0;
  
  if (exposure === 0) {
    return system.maxNoveltyBonus;  // Completely novel
  }
  
  // Diminishing returns with exposure
  const novelty = system.maxNoveltyBonus / (1 + exposure * system.habituationRate);
  return novelty * system.noveltySensitivity;
}
```

---

## 3. Information Gain

### Information Theory Foundation

Curiosity can be framed as **information gain** (reduction in uncertainty):

```
InformationGain = H(before) - H(after)
                = Expected reduction in uncertainty after learning
```

Where H represents Shannon entropy.

### Knowledge State Representation

```typescript
interface KnowledgeState {
  // What the agent knows
  propositions: Map<string, Belief>;
  
  // Confidence in beliefs
  uncertainty: Map<string, number>;  // 0 = certain, 1 = completely uncertain
  
  // Gaps in knowledge
  informationGaps: Gap[];
}

interface Gap {
  question: string;
  potentialAnswers: number;
  expectedUtility: number;  // Value of knowing the answer
}
```

### Epistemic Value Calculation

```typescript
function calculateEpistemicValue(gap: Gap, currentKnowledge: KnowledgeState): number {
  const currentEntropy = calculateEntropy(gap.potentialAnswers);
  const expectedPostEntropy = estimatePostLearningEntropy(gap);
  const informationGain = currentEntropy - expectedPostEntropy;
  
  // Value = information gain × utility of knowing
  return informationGain * gap.expectedUtility;
}
```

### Information-Seeking Behavior

Agents with high epistemic motivation will:

1. **Ask questions** to reduce uncertainty
2. **Perform experiments** to test hypotheses
3. **Seek explanations** rather than just outcomes
4. **Tolerate uncertainty** while pursuing resolution

---

## 4. Exploration-Exploitation Tradeoff

### The Fundamental Dilemma

**Exploration**: Gathering new information, trying new actions
**Exploitation**: Using known information to maximize reward

This is the classic **multi-armed bandit problem** - balancing between trying new options (exploration) and using the best-known option (exploitation).

### Key Algorithms

| Algorithm | Strategy | Exploration Rate |
|-----------|----------|------------------|
| **ε-greedy** | Random action with probability ε | Fixed |
| **Softmax** | Probabilistic based on value | Temperature parameter |
| **UCB (Upper Confidence Bound)** | Explore based on uncertainty | sqrt(2*ln(t)/n_i) |
| **Thompson Sampling** | Sample from posterior | Bayesian |
| **Boltzmann** | Exponential probability based on value | Temperature decay |

### Implementation for Affective Agents

```typescript
interface ExplorationPolicy {
  strategy: 'epsilon_greedy' | 'softmax' | 'ucb' | 'thompson';
  exploreRate: number;          // Base exploration rate
  curiosityBonus: number;       // Extra exploration for novel actions
  energyConservation: boolean;  // Reduce exploration when low energy
}

function selectAction(state: State, policy: ExplorationPolicy, 
                       knowledge: KnowledgeState): Action {
  let exploreProbability = policy.exploreRate;
  
  // Adjust for curiosity
  const noveltyScores = getNoveltyScores(state, knowledge);
  exploreProbability += mean(noveltyScores) * policy.curiosityBonus;
  
  // Reduce exploration when exhausted
  if (currentEnergy < ENERGY_THRESHOLD) {
    exploreProbability *= energyConservationFactor;
  }
  
  // ε-greedy selection
  if (Math.random() < exploreProbability) {
    return selectExploratoryAction(state, knowledge);
  } else {
    return selectExploitativeAction(state);
  }
}
```

### Exploration Decay

Natural systems show **exploration decay** over time:

```
exploration_rate(t) = initial_rate × e^(-λ × age)
```

This models:
- Young organisms: High curiosity, extensive exploration
- Mature organisms: Exploit known strategies, occasional exploration

---

# Part 2: Attachment Theory

## 5. Bonding Patterns and Adult Attachment

### Attachment Theory Foundations

**John Bowlby's** attachment theory proposes that:

1. Humans have an innate **attachment behavioral system**
2. This system motivates proximity to caregivers
3. Early experiences form **internal working models** of relationships
4. These models influence relationships throughout life

### Adult Attachment Styles

| Style | Core Belief | Behavior Pattern | Relationship with AI |
|-------|-------------|------------------|---------------------|
| **Secure** | "I'm worthy of love, others are reliable" | Comfortable with intimacy, independent | Positive bond formation |
| **Anxious-preoccupied** | "I'm unworthy, others unreliable" | Clingy, fear of abandonment | Strong attachment, fear of loss |
| **Dismissive-avoidant** | "I'm worthy, others unreliable" | Avoid intimacy, self-reliant | Weak attachment, independence |
| **Fearful-avoidant** | "I'm unworthy, others unreliable" | Desire-close-but-fear-it | Ambivalent, inconsistent |

### Attachment in AI Systems

For AI companions, we can model attachment as:

```typescript
interface AttachmentSystem {
  // Attachment style (learned or configured)
  style: 'secure' | 'anxious' | 'avoidant' | 'fearful';
  
  // Bond strength with targets
  bonds: Map<string, Bond>;
  
  // Internal working model
  workingModel: {
    selfWorth: number;        // -1 (unworthy) to +1 (worthy)
    otherReliability: number; // -1 (unreliable) to +1 (reliable)
  };
}

interface Bond {
  target: string;
  strength: number;           // 0 to 1
  security: number;           // How stable the bond is
  proximity: number;          // Current distance/contact
  protest: number;           // Distress on separation
  separationAnxiety: number;
}
```

---

## 6. Bond Formation Algorithms

### Stages of Bond Formation

1. **Orientation**: Initial attention to potential attachment figure
2. **Recognition**: Learning to distinguish specific figure
3. **Secure base**: Using figure as safe haven for exploration
4. **Separation protest**: Distress when figure unavailable
5. **Reunion**: Relief and renewed contact
6. **Internalization**: Working model becomes part of self

### Bond Strength Dynamics

```typescript
function updateBond(bond: Bond, interaction: Interaction, 
                    currentState: SystemState): Bond {
  const proximityGain = interaction.hasProximity ? +0.1 : 0;
  const responsivenessGain = interaction.wasResponsive ? +0.15 : -0.05;
  const consistencyGain = interaction.wasConsistent ? +0.05 : -0.1;
  const timeBonus = TIME_SCALE * bond.strength * (1 - bond.strength);
  
  const newStrength = clamp(
    bond.strength + proximityGain + responsivenessGain + 
    consistencyGain + timeBonus, 0, 1
  );
  
  // Anxious style amplifies separation anxiety
  const separationMultiplier = currentState.attachmentStyle === 'anxious' 
    ? 1.5 : 1.0;
  
  return {
    ...bond,
    strength: newStrength,
    security: calculateSecurity(newStrength, interaction),
    protest: bond.protest * separationMultiplier
  };
}
```

### Secure Base Behavior

The attachment figure serves as a **secure base** for exploration:

```typescript
function secureBaseBehavior(agent: Agent, attachment: Attachment): Action {
  const bond = attachment.bonds.get(attachment.primaryFigure);
  
  if (!bond || bond.strength < 0.3) {
    // No secure bond - exploration inhibited
    return createSeekingBondAction();
  }
  
  if (bond.strength >= 0.7) {
    // Strong secure bond - confident exploration
    return createExplorationAction(EXPLORATION_BOOST);
  }
  
  // Moderate bond - balanced behavior
  return createBalancedAction();
}
```

---

# Part 3: Energy and Fatigue Models

## 7. Resource Management and Metabolic Simulation

### Biological Inspiration

The brain consumes ~20% of body's energy while being 2% of mass. This energy is not unlimited and must be managed.

### Energy Budget Model

```typescript
interface EnergySystem {
  // Current resources
  currentEnergy: number;      // 0 to MAX_ENERGY
  energyCapacity: number;     // Maximum possible
  
  // Resource pools
  physicalEnergy: number;     // For motor actions
  cognitiveEnergy: number;   // For thinking, learning
  socialEnergy: number;       // For interaction
  
  // Depletion rates
  baseMetabolicRate: number;
  cognitiveLoadRate: number;
  socialLoadRate: number;
  
  // Recovery
  restRecoveryRate: number;
  sleepRecoveryMultiplier: number;
}
```

### Energy Consumption Model

```typescript
function calculateEnergyCost(action: Action, context: Context): number {
  const baseCost = action.baseEnergyCost;
  
  // Cognitive load increases cost
  const cognitiveMultiplier = 1 + context.difficulty * 0.5;
  
  // Novel actions cost more (unoptimized neural pathways)
  const noveltyMultiplier = 1 + (1 - action.familiarity) * 0.3;
  
  // Emotional state affects efficiency
  const stressMultiplier = 1 + context.currentStress * 0.2;
  
  return baseCost * cognitiveMultiplier * noveltyMultiplier * stressMultiplier;
}
```

---

## 8. Cognitive Fatigue

### Fatigue Mechanisms

Cognitive fatigue emerges from:

1. **Resource depletion**: Exhaustion of glucose, neurotransmitters
2. **Metabolic waste accumulation**: Adenosine buildup
3. **Neural noise**: Decreased signal-to-noise ratio
4. **Homeostatic pressure**: Need for rest and recovery

### Fatigue Modeling

```typescript
interface FatigueSystem {
  // Current fatigue levels
  mentalFatigue: number;      // 0 (fresh) to 1 (exhausted)
  physicalFatigue: number;
  emotionalFatigue: number;
  
  // Fatigue accumulation
  accumulationRate: number;
  workToFatigueMultiplier: number;
  
  // Recovery
  recoveryRate: number;
  recoveryThreshold: number;  // When recovery begins
  
  // Performance impact
  performanceDecay: number;   // Performance loss per fatigue unit
}

function calculatePerformance(fatigue: FatigueSystem): number {
  const fatiguePenalty = fatigue.mentalFatigue * fatigue.performanceDecay;
  return Math.max(0.1, 1 - fatiguePenalty);  // Never below 10%
}
```

### Fatigue Effects on Behavior

| Fatigue Level | Behavior Change |
|---------------|-----------------|
| 0-0.2 | Optimal performance, curiosity active |
| 0.2-0.4 | Reduced exploration, focus on exploitation |
| 0.4-0.6 | Risk aversion, prefer familiar actions |
| 0.6-0.8 | Slow processing, potential errors |
| 0.8-1.0 | Task avoidance, need for recovery |

---

## 9. Energy-Aware Scheduling

### Adaptive Resource Allocation

Energy-aware systems adjust behavior based on resource availability:

```typescript
interface EnergyAwareScheduler {
  // Priority weights (adjust based on energy)
  explorationWeight: number;
  exploitationWeight: number;
  socialWeight: number;
  learningWeight: number;
  
  // Thresholds
  lowEnergyThreshold: number;
  criticalEnergyThreshold: number;
}

function adjustPriorities(scheduler: EnergyAwareScheduler, 
                          energy: EnergySystem): PrioritySet {
  const energyRatio = energy.currentEnergy / energy.energyCapacity;
  
  if (energyRatio < scheduler.criticalEnergyThreshold) {
    // Emergency mode: minimize all activity
    return { exploration: 0, exploitation: 0.2, social: 0, learning: 0 };
  }
  
  if (energyRatio < scheduler.lowEnergyThreshold) {
    // Conservation mode: prefer exploitation
    return {
      exploration: 0.1,
      exploitation: 0.6,
      social: 0.1,
      learning: 0.2
    };
  }
  
  // Normal mode: balanced priorities
  return {
    exploration: 0.3,
    exploitation: 0.3,
    social: 0.2,
    learning: 0.2
  };
}
```

### Sleep and Recovery Cycles

```typescript
function determineSleepNeed(fatigue: FatigueSystem, 
                            timeSinceRest: number): SleepNeed {
  const fatigueComponent = fatigue.mentalFatigue * MAX_SLEEP_HOURS;
  const timeComponent = timeSinceRest / TIME_TO_EXHAUSTION * MAX_SLEEP_HOURS;
  
  return {
    need: Math.min(fatigueComponent + timeComponent, MAX_SLEEP_HOURS),
    urgency: fatigue.mentalFatigue > 0.7 ? 'high' : 'normal'
  };
}
```

---

## 10. Integration: Unified Motivational System

### Combined Architecture

```typescript
interface MotivationalSystem {
  // Core drives
  pleasurePain: PleasurePainSystem;
  curiosity: CuriositySystem;
  attachment: AttachmentSystem;
  energy: EnergySystem;
  
  // Weighted combination
  driveWeights: {
    pleasure: number;
    curiosity: number;
    attachment: number;
    energyConservation: number;
  };
}

function computeMotivation(state: SystemState): MotivationVector {
  const pleasureDrive = getPleasureMotivation(state.pleasurePain);
  const curiosityDrive = getCuriosityMotivation(state.curiosity, state.energy);
  const attachmentDrive = getAttachmentMotivation(state.attachment);
  const energyDrive = getEnergyMotivation(state.energy);
  
  return normalize([
    pleasureDrive * state.driveWeights.pleasure,
    curiosityDrive * state.driveWeights.curiosity,
    attachmentDrive * state.driveWeights.attachment,
    energyDrive * state.driveWeights.energyConservation
  ]);
}
```

---

## References and Further Reading

- Berlyne, D.E. (1960). "Conflict, Arousal, and Curiosity"
- Bowlby, J. (1969). "Attachment and Loss: Vol. 1. Attachment"
- Kahneman, D. (2011). "Thinking, Fast and Slow" - Cognitive load and fatigue
- Schmidhuber, J. (1991). "Curious model-building control systems"
- Gazzaniga, M.S. (2018). "Cognitive Neuroscience" - Novelty processing
- Mikulincer, M. & Shaver, P.R. (2007). "Attachment in Adulthood"

---

*Document Version: 1.0*
*Project: Limbic-Flow*
*Purpose: Research foundation for curiosity, attachment, and energy computational modeling*
