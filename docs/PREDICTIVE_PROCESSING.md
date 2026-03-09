# Predictive Processing and Free Energy Principle

## Overview

Predictive processing represents a unifying theoretical framework in cognitive neuroscience that reframes the brain as a hierarchical prediction machine. This document covers the core concepts and their implications for Limbic-Flow's affective modeling architecture.

---

## 1. Free Energy Principle (FEP)

### Core Concept

Proposed by Karl Friston, the **Free Energy Principle** states that any self-organizing system that resists entropy must minimize its free energy. Free energy is a variational bound on surprise—essentially, the difference between what the system expects and what it experiences.

### Mathematical Foundation

```
Free Energy (F) = Expected Free Energy (EFE) + Surprise

F = E_q[ln q(φ|s) - ln p(s,φ)] 

Where:
- q(φ|s): posterior belief about hidden states
- p(s,φ): joint probability of observations and states
- Minimizing F ≈ maximizing model evidence
```

### Key Implications

- **Brain as prediction machine**: The brain constantly generates predictions about sensory inputs
- **Prediction errors**: Mismatches between predictions and actual input drive learning
- **Active inference**: The system acts to confirm its predictions (precision-weighted)

---

## 2. Predictive Coding

### Hierarchical Architecture

Predictive coding proposes a hierarchical neural architecture where:

1. **Higher levels** generate predictions about lower levels
2. **Lower levels** compute prediction errors (prediction - actual)
3. **Prediction errors** flow upward, predictions flow downward
4. **Cortical columns** implement this bidirectional message passing

### Neural Implementation

| Level | Brain Region | Function |
|-------|--------------|----------|
| Primary sensory | V1, A1, S1 | Low-level feature detection |
| Secondary | V2, S2 | Intermediate integration |
| Association | PPC, STG | Object/scene representation |
| Prefrontal | DLPFC, MPFC | Abstract goals, planning |
| Default mode | PCC, MPFC | Self-referential processing |

### Computational Model

```
Prediction_error = Sensory_input - Top-down_prediction
Update_weights = learning_rate × prediction_error × bottom-up_signal
Update_prediction = learning_rate × prediction_error × top-down_connection
```

---

## 3. Active Inference

### Definition

Active inference is the process by which an agent acts to minimize expected free energy by:

1. **Selecting actions** that bring observations in line with prior beliefs
2. **Seeking information** to resolve uncertainty
3. **Preflective planning** through imagined futures

### The Expected Free Energy (EFE)

```
EFE(s', a) = ∑_o' p(o'|s', a)[G(o') + H(Q)]

Where:
- G(o'): epistemic value (information gain)
- H(Q): pragmatic value (goal attainment)
- o': future observations
- s': future states
- a: action
```

### Applications to Affective Systems

For Limbic-Flow, active inference suggests:

- **Emotions as prediction signals**: Affective states represent predicted states of the world
- **Anxiety as uncertainty**: Heightened prediction error about threat
- **Depression as collapsed priors**: Overly negative baseline expectations

---

## 4. Hierarchical Prediction in Emotion

### Multi-Level Emotion Generation

| Level | Temporal Scale | Content |
|-------|----------------|---------|
| Physiological | < 100ms | Heart rate, skin conductance |
| Behavioral | 100ms - 1s | Facial expression, posture |
| Situational | 1s - 10s | Social context, meaning |
| Narrative | 10s - minutes | Life story, identity |

### Prediction Error Signals in Emotion

- **Surprise**: Unexpected observation (high PE)
- **Fear**: High PE for threat-related stimuli
- **Joy**: PE below expected (positive prediction)
- **Anger**: Blocked goal, high PE for agency

---

## 5. Implementation in Limbic-Flow

### Architecture Components

```
┌─────────────────────────────────────────────────┐
│           Hierarchical Predictor                 │
├─────────────────────────────────────────────────┤
│ Level 5: Narrative Goals (10s+)                 │
│ Level 4: Situational Models (1-10s)             │
│ Level 3: Behavioral Scripts (100ms-1s)           │
│ Level 2: Physiological Response (<1s)           │
│ Level 1: Sensory Processing (<100ms)            │
├─────────────────────────────────────────────────┤
│           Prediction Error Aggregator            │
│           (Surprise, Uncertainty, Valence)       │
└─────────────────────────────────────────────────┘
```

### Key Algorithms

#### Surprise Detection
```
Surprise = -log(p(observation | context))
           = -log(Belief_confidence × Feature_match)
```

#### Uncertainty Quantification
```
Uncertainty = Entropy(p(beliefs))
            = -∑ p_i × log(p_i)
```

#### Precision Weighting
```
Weighted_PE = Prediction_Error × Precision
Precision = 1 / Variance(noise_estimate)
```

---

## 6. Integration with Other Systems

### Neuromodulation Connection

- **Dopamine**: Signals reward prediction error (RPE)
- **Norepinephrine**: Adjusts precision weights (attention)
- **Acetylcholine**: Signals unexpected information (novelty)
- **Serotonin**: Modulates baseline expectations (mood)

### Memory Systems

- Predictive coding explains memory as:
  - Consolidation of prediction models
  - Schema formation from repeated predictions
  - Forgetting as precision reweighting

### Consciousness

- Predictive processing theories of consciousness:
  - Presence as maintained world-model
  - Emotion as interoceptive prediction
  - Self as hierarchical predictor

---

## 7. Research Directions

### Open Questions

1. **Precision weighting**: How does the brain estimate and adjust precision?
2. **Hierarchical timescales**: How are fast and slow predictions integrated?
3. **Neural implementation**: Detailed circuit mechanisms remain unclear

### Applications

- **Clinical**: Understanding anxiety, depression, psychosis
- **AI**: Hierarchical reinforcement learning, world models
- **VR/AR**: Predictive interfaces, adaptive environments

---

## References

- Friston, K. (2010). The free-energy principle: a unified brain theory? Nature Reviews Neuroscience.
- Rao, R.P.N., & Ballard, D.H. (1999). Predictive coding in the visual cortex. Nature Neuroscience.
- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. Behavioral and Brain Sciences.
- Friston, K. (2019). Publisher Correction: The free-energy principle: a rough guide to the brain. Nature Reviews Neuroscience.

---

*Document Version: 1.0*
*Last Updated: 2026-03-09*
*Project: Limbic-Flow*
