# Stress Response & Social Bonding Systems

This document covers computational models for oxytocin-mediated social bonding and cortisol-driven stress response within the Limbic-Flow architecture.

---

## 3. Oxytocin & Trust Systems

### 3.1 Social Bonding

**Theoretical Foundation**
Oxytocin (OT) is a neuropeptide involved in social bonding, trust, and prosocial behavior. It plays crucial roles in pair bonding, parent-child attachment, and trust formation. The oxytocin system interacts with dopamine (reward), serotonin (mood), and cortisol (stress).

```python
class OxytocinSystem:
    """
    Models oxytocin-mediated social bonding and attachment.
    """
    
    def __init__(self, baseline_oxytocin=0.5, receptor_sensitivity=0.6,
                 bonding_rate=0.3, release_triggers=None):
        # baseline_oxytocin: resting OT levels (0-1 scale)
        # receptor_sensitivity: how responsive receptor system is
        # bonding_rate: speed of bond formation
        # release_triggers: contexts that cause OT release
        
        self.baseline = baseline_oxytocin
        self.receptor_sensitivity = receptor_sensitivity
        self.bonding_rate = bonding_rate
        self.release_triggers = release_triggers or self._default_triggers()
        
        self.current_levels = baseline_oxytocin
        self.active_bonds = {}  # bond_id -> Bond object
    
    def _default_triggers(self):
        return {
            'physical_affection': 0.3,
            'eye_contact': 0.15,
            'social_support': 0.25,
            'trust_game': 0.2,
            'parenting_behavior': 0.35,
            'pair_bonding_intimacy': 0.4
        }
    
    class Bond:
        def __init__(self, target_id, bond_type, strength, trust_level):
            self.target_id = target_id
            self.bond_type = bond_type
            self.strength = strength
            self.trust_level = trust_level
            self.oxytocin_investment = 0.0
    
    def process_stimulus(self, stimulus_type, context):
        if stimulus_type in self.release_triggers:
            release_amount = self.release_triggers[stimulus_type]
            effective_release = release_amount * self.receptor_sensitivity
            self.current_levels = min(1.0, self.current_levels + effective_release)
            return OxytocinResponse(
                released=effective_release,
                current_level=self.current_levels,
                triggered_by=stimulus_type
            )
        return None
    
    def form_bond(self, target_id, bond_type, initial_trust=0.2):
        if target_id in self.active_bonds:
            bond = self.active_bonds[target_id]
            bond.strength = min(1.0, bond.strength + self.bonding_rate)
        else:
            bond = self.Bond(target_id, bond_type, self.bonding_rate, initial_trust)
            self.active_bonds[target_id] = bond
        self.current_levels = min(1.0, self.current_levels + 0.1)
        return bond
    
    def strengthen_bond(self, target_id, positive_interaction):
        if target_id not in self.active_bonds:
            return None
        bond = self.active_bonds[target_id]
        strength_increase = self.bonding_rate * positive_interaction.intensity
        trust_increase = strength_increase * self.current_levels * self.receptor_sensitivity
        bond.strength = min(1.0, bond.strength + strength_increase)
        bond.trust_level = min(1.0, bond.trust_level + trust_increase)
        return bond
```

### 3.2 Trust Computation

```python
class TrustComputation:
    def __init__(self, base_trust=0.5, reliability_weight=0.4, 
                 benevolence_weight=0.3, competence_weight=0.2,
                 predictability_weight=0.1):
        self.base_trust = base_trust
        self.weights = {
            'reliability': reliability_weight,
            'benevolence': benevolence_weight,
            'competence': competence_weight,
            'predictability': predictability_weight
        }
        self.trust_history = {}
    
    def compute_trust(self, target_id, partner_model):
        reliability = partner_model.reliability_score
        benevolence = partner_model.benevolence_score
        competence = partner_model.competence_score
        predictability = partner_model.predictability_score
        
        trust = self.base_trust
        trust += reliability * self.weights['reliability']
        trust += benevolence * self.weights['benevolence']
        trust += competence * self.weights['competence']
        trust += predictability * self.weights['predictability']
        
        return min(1.0, max(0.0, trust))
    
    def update_trust(self, target_id, interaction_outcome):
        if target_id not in self.trust_history:
            self.trust_history[target_id] = []
        
        if interaction_outcome.positive:
            trust_delta = 0.05 * interaction_outcome.magnitude
        else:
            trust_delta = -0.1 * interaction_outcome.magnitude
        
        self.trust_history[target_id].append({
            'delta': trust_delta,
            'type': interaction_outcome.type,
            'timestamp': current_time()
        })
        return trust_delta
    
    def calculate_trust_decay(self, target_id, time_since_interaction):
        if target_id not in self.active_bonds:
            return 0.0
        bond = self.active_bonds[target_id]
        decay_rate = 0.01 * (1.0 - bond.strength)
        return min(bond.trust_level, decay_rate * time_since_interaction)
    
    def trust_risk_assessment(self, target_id, action_type, action_cost):
        if target_id not in self.active_bonds:
            return TrustDecision(accepted=False, risk_level=1.0, reason='no_bond')
        
        bond = self.active_bonds[target_id]
        risk_level = action_cost * (1.0 - bond.trust_level)
        threshold = 0.5
        
        if risk_level < threshold:
            return TrustDecision(accepted=True, risk_level=risk_level, trust_utilized=bond.trust_level)
        else:
            return TrustDecision(accepted=False, risk_level=risk_level, trust_utilized=bond.trust_level, reason='risk_too_high')
```

### 3.3 Social Attachment Modeling

```python
class SocialAttachmentSystem:
    def __init__(self, attachment_style='secure', attachment_anxiety=0.3,
                 attachment_avoidance=0.2):
        self.style = attachment_style
        self.anxiety = attachment_anxiety
        self.avoidance = attachment_avoidance
        self.attachment_figures = []
    
    def activate_attachment_behavior(self, threat_detected, available_figures):
        if threat_detected:
            if self.anxiety > self.avoidance:
                return self._anxious_proximity_seeking(available_figures)
            elif self.avoidance > self.anxiety:
                return self._avoidant_self-reliance()
            else:
                return self._secure_attachment_response(available_figures)
        return None
    
    def _anxious_proximity_seeking(self, figures):
        seeking_intensity = self.anxiety * 0.8
        return AttachmentBehavior(
            type='anxious_seeking',
            intensity=seeking_intensity,
            behaviors=['proximity_maintenance', 'separation_protest'],
            hypervigilance=self.anxiety * 0.6
        )
    
    def _avoidant_self-reliance(self):
        return AttachmentBehavior(
            type='avoidant',
            intensity=self.avoidance * 0.7,
            behaviors=['self_reliance', 'emotional_distance'],
            suppression=self.avoidance * 0.7
        )
    
    def _secure_attachment_response(self, figures):
        return AttachmentBehavior(type='secure', intensity=0.5, 
                                  behaviors=['healthy_proximity_seeking'], confidence=0.7)
    
    def process_relationship_event(self, event):
        if event.type == 'responsive_caregiver':
            self.anxiety = max(0, self.anxiety - 0.05)
            self.avoidance = max(0, self.avoidance - 0.05)
        elif event.type == 'unresponsive_caregiver':
            self.anxiety = min(1.0, self.anxiety + 0.1)
        elif event.type == 'rejection':
            self.avoidance = min(1.0, self.avoidance + 0.1)
        self._update_attachment_style()
    
    def _update_attachment_style(self):
        if self.anxiety < 0.3 and self.avoidance < 0.3:
            self.style = 'secure'
        elif self.anxiety > 0.5 and self.avoidance < 0.3:
            self.style = 'anxious'
        elif self.avoidance > 0.5 and self.anxiety < 0.3:
            self.style = 'avoidant'
        elif self.anxiety > 0.5 and self.avoidance > 0.5:
            self.style = 'disorganized'
```

### 3.4 Bonding/Trust Decay

```python
class BondingDecayModel:
    def __init__(self, base_decay_rate=0.02, trust_penalty_multiplier=1.5, recovery_rate=0.1):
        self.base_decay = base_decay_rate
        self.penalty_mult = trust_penalty_multiplier
        self.recovery_rate = recovery_rate
        self.decay_events = {}
    
    def calculate_decay(self, bond, time_elapsed, recent_interactions):
        time_decay = self.base_decay * time_elapsed * (1.0 - bond.strength * 0.5)
        
        negative_decay = 0.0
        for interaction in recent_interactions:
            if not interaction.positive:
                negative_decay += self.penalty_mult * 0.1
        
        return min(bond.strength, time_decay + negative_decay)
    
    def apply_decay(self, bond, time_elapsed, recent_interactions):
        decay_amount = self.calculate_decay(bond, time_elapsed, recent_interactions)
        bond.strength = max(0.0, bond.strength - decay_amount)
        bond.trust_level = max(0.0, bond.trust_level - decay_amount)
        return bond
    
    def recover_bond(self, bond, positive_interaction):
        recovery = self.recovery_rate * positive_interaction.magnitude
        decay_severity = 1.0 - bond.strength
        recovery *= (1.0 - decay_severity * 0.5)
        bond.strength = min(1.0, bond.strength + recovery)
        bond.trust_level = min(1.0, bond.trust_level + recovery)
        return bond
```

---

## 4. Cortisol & Stress Response

### 4.1 HPA Axis Modeling

**Theoretical Foundation**
The Hypothalamic-Pituitary-Adrenal (HPA) axis is the central stress response system. When stress is perceived, the hypothalamus releases CRH, which triggers pituitary ACTH release, stimulating adrenal cortisol production.

```python
class HPAAxisModel:
    def __init__(self, baseline_cortisol=0.3, axis_sensitivity=0.6,
                 cortisol_response_gain=0.5, recovery_rate=0.1):
        self.baseline = baseline_cortisol
        self.sensitivity = axis_sensitivity
        self.response_gain = cortisol_response_gain
        self.recovery_rate = recovery_rate
        self.current_cortisol = baseline_cortisol
        self.cortisol_history = []
        self.stress_exposure_total = 0.0
        self.axis_state = 'baseline'
        self.crh_level = 0.0
        self.acth_level = 0.0
    
    def perceive_stress(self, stressor, intensity):
        appraisal = self._appraise_stressor(stressor)
        
        if appraisal.threatening:
            self.axis_state = 'activated'
            crh_release = intensity * self.sensitivity * 0.5
            self.crh_level = min(1.0, self.crh_level + crh_release)
            acth_release = self.crh_level * 0.8
            self.acth_level = min(1.0, self.acth_level + acth_release)
            cortisol_release = acth_release * self.response_gain
            self.current_cortisol = min(1.0, self.current_cortisol + cortisol_release)
            self.stress_exposure_total += intensity
            
            return StressResponse(
                axis_state='activated',
                cortisol_increase=cortisol_release,
                crh_level=self.crh_level,
                acth_level=self.acth_level,
                appraisal=appraisal
            )
        return StressResponse(axis_state='baseline', appraisal=appraisal)
    
    def _appraise_stressor(self, stressor):
        relevance = stressor.relevance_to_goals
        threat_level = relevance * stressor.potential_harm
        coping_ability = stressor.available_resources / stressor.demand
        
        if threat_level > 0.5 and coping_ability > 0.5:
            appraisal_type = 'challenge'
        elif threat_level > 0.5:
            appraisal_type = 'threat'
        else:
            appraisal_type = 'irrelevant'
        
        return StressAppraisal(
            threatening=appraisal_type in ['threat', 'challenge'],
            type=appraisal_type,
            threat_level=threat_level,
            coping_ability=coping_ability
        )
    
    def update_cortisol_level(self, time_step):
        if self.axis_state == 'activated':
            recovery = self.recovery_rate * time_step
            self.current_cortisol = max(self.baseline, self.current_cortisol - recovery)
            self.crh_level *= 0.8
            self.acth_level *= 0.9
            
            if self.current_cortisol <= self.baseline * 1.2:
                self.axis_state = 'baseline'
                self.crh_level = 0.0
                self.acth_level = 0.0
        
        self.cortisol_history.append({
            'cortisol': self.current_cortisol,
            'time': current_time(),
            'state': self.axis_state
        })
        return self.current_cortisol
    
    def circadian_cortisol_pattern(self, hour):
        return 0.3 + 0.2 * math.sin((hour - 6) * math.pi / 12)
```

### 4.2 Stress Accumulation Algorithms

```python
class StressAccumulationModel:
    def __init__(self, accumulation_rate=0.1, threshold_warning=0.6,
                 threshold_danger=0.8, max_capacity=1.0):
        self.accumulation_rate = accumulation_rate
        self.warning_threshold = threshold_warning
        self.danger_threshold = threshold_danger
        self.max_capacity = max_capacity
        self.current_stress = 0.0
        self.stress_episodes = []
    
    def add_stressor(self, stressor, duration=1.0):
        impact = stressor.intensity * duration * self.accumulation_rate
        self.current_stress = min(self.max_capacity, self.current_stress + impact)
        
        self.stress_episodes.append({
            'stressor': stressor.type,
            'impact': impact,
            'total_stress': self.current_stress,
            'timestamp': current_time()
        })
        
        return StressUpdate(new_level=self.current_stress, impact=impact, 
                          warnings=self._check_warnings())
    
    def _check_warnings(self):
        warnings = []
        if self.current_stress >= self.warning_threshold:
            warnings.append('stress_elevated')
        if self.current_stress >= self.danger_threshold:
            warnings.append('stress_critical')
        if self.current_stress >= self.max_capacity * 0.95:
            warnings.append('stress_overload')
        return warnings
    
    def calculate_stress_trajectory(self, upcoming_stressors):
        projected_stress = self.current_stress
        for stressor in upcoming_stressors:
            projected_stress += stressor.intensity * self.accumulation_rate
        
        return {
            'current': self.current_stress,
            'projected': min(1.0, projected_stress),
            'exceeds_warning': projected_stress > self.warning_threshold,
            'exceeds_danger': projected_stress > self.danger_threshold
        }
```

### 4.3 Allostatic Load

```python
class AllostaticLoadModel:
    def __init__(self, initial_load=0.0, load_accumulation_rate=0.05,
                 recovery_drain_rate=0.02, system_count=6):
        self.total_load = initial_load
        self.accumulation_rate = load_accumulation_rate
        self.recovery_drain = recovery_drain_rate
        self.system_loads = {f'system_{i}': 0.0 for i in range(system_count)}
        self.system_names = ['cardiovascular', 'immune', 'metabolic', 
                           'neuroendocrine', 'central_nervous', 'musculoskeletal']
        self.total_stress_exposure = 0.0
    
    def add_stress_impact(self, stressor, affected_systems=None):
        if affected_systems is None:
            affected_systems = range(len(self.system_loads))
        
        impact = stressor.intensity * self.accumulation_rate
        
        for idx in affected_systems:
            system_key = f'system_{idx}'
            vulnerability = 0.5 + (idx * 0.1)
            self.system_loads[system_key] += impact * vulnerability
        
        self.total_load = sum(self.system_loads.values()) / len(self.system_loads)
        self.total_stress_exposure += stressor.intensity
        
        return AllostaticLoadUpdate(new_total=self.total_load)
    
    def apply_recovery(self, recovery_quality=0.5, duration=1.0):
        effective_recovery = recovery_quality * duration
        recovery_amount = effective_recovery * (1.0 - self.total_load)
        
        for key in self.system_loads:
            self.system_loads[key] = max(0, self.system_loads[key] - recovery_amount)
        
        self.total_load = sum(self.system_loads.values()) / len(self.system_loads)
        return RecoveryResult(load_reduced=recovery_amount, new_total=self.total_load)
    
    def calculate_health_impact(self):
        impacts = {}
        if self.system_loads['system_0'] > 0.6:
            impacts['cardiovascular_risk'] = 'elevated'
        if self.system_loads['system_1'] > 0.6:
            impacts['immune_suppression'] = 'elevated'
        
        if self.total_load > 0.8:
            impacts['overall'] = 'severe'
        elif self.total_load > 0.6:
            impacts['overall'] = 'moderate'
        elif self.total_load > 0.4:
            impacts['overall'] = 'mild'
        else:
            impacts['overall'] = 'minimal'
        return impacts
    
    def predict_allostatic_overload_risk(self, upcoming_stressors):
        projected_additional = sum(s.intensity * self.accumulation_rate for s in upcoming_stressors)
        projected_total = min(1.0, self.total_load + projected_additional)
        
        if projected_total > 0.9:
            risk_category = 'critical'
        elif projected_total > 0.75:
            risk_category = 'high'
        elif projected_total > 0.5:
            risk_category = 'moderate'
        else:
            risk_category = 'low'
        
        return OverloadRiskPrediction(current_load=self.total_load, 
                                     projected_load=projected_total,
                                     risk_category=risk_category)
```

### 4.4 Stress Recovery Curves

```python
class StressRecoveryCurve:
    def __init__(self, initial_stress=1.0, recovery_rate=0.15, recovery_type='exponential'):
        self.initial_stress = initial_stress
        self.recovery_rate = recovery_rate
        self.recovery_type = recovery_type
        self.current_level = initial_stress
        self.recovery_history = []
    
    def exponential_recovery(self, time):
        return self.initial_stress * math.exp(-self.recovery_rate * time)
    
    def logistic_recovery(self, time, carrying_capacity=0.0, midpoint=5.0):
        k = self.recovery_rate
        L = carrying_capacity
        return (self.initial_stress - L) / (1 + math.exp(-k * (time - midpoint))) + L
    
    def biphasic_recovery(self, time, fast_rate=0.3, slow_rate=0.05, transition_point=3.0):
        rate = fast_rate if time < transition_point else slow_rate
        return self.initial_stress * math.exp(-rate * time)
    
    def calculate_recovery(self, time):
        if self.recovery_type == 'exponential':
            recovered = self.exponential_recovery(time)
        elif self.recovery_type == 'logistic':
            recovered = self.logistic_recovery(time)
        elif self.recovery_type == 'biphasic':
            recovered = self.biphasic_recovery(time)
        else:
            recovered = self.exponential_recovery(time)
        
        self.recovery_history.append({'time': time, 'level': recovered})
        self.current_level = recovered
        return recovered
    
    def time_to_reach_level(self, target_level=0.1):
        if self.recovery_type == 'exponential':
            if target_level >= self.initial_stress:
                return 0
            return -math.log(target_level / self.initial_stress) / self.recovery_rate
        else:
            t = 0
            while self.calculate_recovery(t) > target_level:
                t += 0.1
            return t


class StressRecoveryWithSupport:
    def __init__(self, base_recovery=0.15, support_modifier=0.1):
        self.base_recovery = base_recovery
        self.support_modifier = support_modifier
    
    def calculate_supported_recovery(self, stress_level, available_support, time):
        effective_stress = stress_level * (1.0 - available_support * self.support_modifier)
        supported_rate = self.base_recovery * (1.0 + available_support * 0.5)
        return effective_stress * math.exp(-supported_rate * time)
    
    def support_buffering_effect(self, stress_intensity, support_level):
        if stress_intensity < 0.3:
            return 0.1 * support_level
        elif stress_intensity < 0.7:
            return 0.3 * support_level
        else:
            return 0.5 * support_level
```

---

## Integration: Combined Social Bonding & Stress System

```python
class SocialStressIntegration:
    def __init__(self, oxytocin_system, hpa_axis, trust_system):
        self.oxytocin = oxytocin_system
        self.cortisol = hpa_axis
        self.trust = trust_system
        self.oxytocin_cortisol_interaction = True
    
    def process_social_stress(self, social_situation):
        results = {}
        
        if hasattr(social_situation, 'trust_challenge'):
            trust_response = self.trust.process_trust_decision(
                social_situation.partner, social_situation.trust_challenge
            )
            results['trust_decision'] = trust_response
            if not trust_response.accepted:
                stress_response = self.cortisol.perceive_stress(
                    Stressor('trust_violation', intensity=0.6), intensity=0.6
                )
                results['stress_response'] = stress_response
        
        if hasattr(social_situation, 'bonding_opportunity'):
            ot_response = self.oxytocin.process_stimulus(
                social_situation.bonding_opportunity, social_situation
            )
            results['oxytocin_response'] = ot_response
            if ot_response and self.oxytocin_cortisol_interaction:
                results['stress_buffer'] = ot_response.released * 0.3
        
        return IntegratedResponse(**results)
    
    def calculate_social_stress_resilience(self):
        ot_factor = self.oxytocin.current_levels
        cortisol_factor = 1.0 - self.cortisol.current_cortisol
        trust_factor = self.trust.average_trust_level()
        
        resilience = (ot_factor * 0.3 + cortisol_factor * 0.4 + trust_factor * 0.3)
        
        return ResilienceScore(
            overall=resilience,
            oxytocin_contribution=ot_factor * 0.3,
            cortisol_contribution=cortisol_factor * 0.4,
            trust_contribution=trust_factor * 0.3
        )
```

---

## Configuration Examples

```python
# High trust, secure attachment profile
social_profile = SocialStressIntegration(
    oxytocin_system=OxytocinSystem(
        baseline_oxytocin=0.6,
        receptor_sensitivity=0.7,
        bonding_rate=0.4
    ),
    hpa_axis=HPAAxisModel(
        baseline_cortisol=0.3,
        axis_sensitivity=0.4,
        recovery_rate=0.15
    ),
    trust_system=TrustComputation(
        base_trust=0.6,
        reliability_weight=0.5
    )
)

# High stress reactivity, low trust profile
stressed_profile = SocialStressIntegration(
    oxytocin_system=OxytocinSystem(
        baseline_oxytocin=0.3,
        receptor_sensitivity=0.4,
        bonding_rate=0.2
    ),
    hpa_axis=HPAAxisModel(
        baseline_cortisol=0.4,
        axis_sensitivity=0.8,
        recovery_rate=0.08
    ),
    trust_system=TrustComputation(
        base_trust=0.3,
        reliability_weight=0.3
    )
)
```

---

## Research Considerations

### Validation Approaches
- Measure cortisol levels (salivary, blood) to calibrate HPA axis models
- Use trust games (investment, ultimatum) to validate trust computation
- Assess attachment style through validated questionnaires (ECR, AAQ)

### Ethical Considerations
- Avoid oversimplifying complex neurochemical systems
- Consider individual variation in baseline hormone levels
- Model differences as variations, not deficits

### Extensions
- Seasonal variation in oxytocin/cortisol
- Development across lifespan (childhood, adolescence, aging)
- Interaction with other neurotransmitters (dopamine, serotonin)
- Context-dependent modulation (social vs. physical stress)
