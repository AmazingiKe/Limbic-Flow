# Limbic-Flow Implementation Roadmap

> **Version:** 1.0  
> **Date:** 2026-03-09  
> **Status:** Planning

---

## Executive Summary

This roadmap outlines the phased development of Limbic-Flow, an experimental cognitive architecture that simulates human emotional decay, memory distortion, and pathological states. The implementation is structured across four major phases, building from a core emotion engine to advanced cross-platform memory integration.

---

## Part 1: Integration with Obsidian/FlowUs

### 1.1 Bidirectional Note Sync

#### Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Obsidian      │────▶│  Limbic-Flow    │────▶│    FlowUs       │
│   (Local JSON)  │◀────│  Sync Engine     │◀────│  (Cloud API)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

#### Implementation Strategy

**Phase A: Core Sync Protocol**
- Implement `NoteSyncAdapter` base class
- Define unified note format (Markdown + YAML frontmatter)
- Create conflict resolution algorithm (last-write-wins with timestamp + merge for emotional metadata)

**Phase B: Obsidian Integration**
- Use Obsidian's REST API or dataview-style JSON export
- Watch vault for changes via file system observer
- Support both pull (read notes) and push (write annotations)

**Phase C: FlowUs Integration**
- Leverage FlowUs API for page CRUD operations
- Handle rate limiting with exponential backoff
- Map FlowUs blocks ↔ Markdown conversions

#### Sync Conflict Resolution

```python
class NoteSyncConflict:
    def resolve(local: Note, remote: Note) -> Note:
        # Priority: emotional_metadata > content > timestamps
        merged.content = merge_markdown(local.content, remote.content)
        merged.emotional_metadata = remote.emotional_metadata  # Always prefer emotional data
        merged.last_modified = max(local.last_modified, remote.last_modified)
        return merged
```

### 1.2 Emotional Metadata in Notes

#### Metadata Schema

```yaml
---
limbic-flow:
  emotion:
    pleasure: 0.7      # -1.0 to 1.0
    arousal: 0.3       # -1.0 to 1.0
    dominance: 0.5    # -1.0 to 1.0
  neurotransmitters:
    dopamine: 0.6
    cortisol: 0.2
  last_emotion_update: "2026-03-09T23:00:00Z"
  emotional_context: "User expressed excitement about new project"
  attachments:
    - type: "memory_fragment"
      vector_id: "mem_001"
      relevance: 0.85
    - type: "trauma_trigger"
      trigger_id: "trig_042"
      intensity: 0.7
---
```

#### Features

1. **Automatic Emotion Tagging**
   - Analyze note content using LLM
   - Extract implicit emotions from writing tone
   - Update metadata on note read/write

2. **Mood-Contingent Recall**
   - Notes tagged with emotional states become retrieval cues
   - Depressive state → grey filter applied to positive notes
   - Anxious state → amplify threat-related annotations

3. **Emotional Annotations**
   - Add margin notes with emotional commentary
   - Example: "This memory feels distant now (P=-0.3, A=0.1)"

### 1.3 Cross-Platform Memory

#### Unified Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Limbic-Flow Memory Core                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Hippocampus│  │   Amygdala  │  │     Neocortex       │ │
│  │  (Vectors)  │  │  (SQLite)   │  │     (Graph DB)      │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         │                │                     │            │
│         └────────────────┼─────────────────────┘            │
│                          ▼                                   │
│              ┌───────────────────────┐                       │
│              │   Memory Gateway      │                       │
│              │  (Unified Interface)  │                       │
│              └───────────┬───────────┘                       │
└──────────────────────────┼──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   Obsidian    │  │    FlowUs     │  │   Web/Cloud   │
│   Local Vault │  │   Workspace   │  │   Storage     │
└───────────────┘  └───────────────┘  └───────────────┘
```

#### Cross-Platform Features

1. **Unified Memory Interface**
   - Single API for reading/writing to any platform
   - Platform-specific adapters with common interface
   - Offline-first with sync queue

2. **Emotional Continuity**
   - Mood state persists across platforms
   - Notes from any platform contribute to emotional context
   - Cross-referencing emotional patterns

3. **Privacy-Preserving Sync**
   - Local-first: emotional data stays on device
   - Selective sync: user controls what gets shared
   - End-to-end encryption for sensitive annotations

---

## Part 2: Implementation Phases

### Phase 1: Core Emotion Engine (Weeks 1-4)

#### Goals
- Establish PAD emotion model foundation
- Implement neurotransmitter simulation
- Create basic emotional decay/half-life system

#### Deliverables

| Component | Description | Priority |
|-----------|-------------|----------|
| `PADCalculator` | Core emotion vector math | P0 |
| `NeurotransmitterSystem` | Dopamine/Cortisol dynamics | P0 |
| `EmotionDecayEngine` | Half-life emotional decay | P0 |
| `EmotionalState` | State management | P1 |
| `EmotionRenderer` | LLM prompt injection | P1 |

#### Technical Details

**PAD Model Implementation:**
```python
class PADState:
    pleasure: float    # -1.0 to 1.0
    arousal: float    # -1.0 to 1.0
    dominance: float  # -1.0 to 1.0
    
    def decay(half_life_minutes: int, elapsed_minutes: int) -> PADState:
        decay_factor = 0.5 ** (elapsed_minutes / half_life_minutes)
        # Decay toward neutral (0, 0, 0)
        return self * decay_factor + Neutral * (1 - decay_factor)
```

**Neurotransmitter Dynamics:**
```python
class Neurotransmitter:
    dopamine: float    # Reward, excitement (0-1)
    cortisol: float   # Stress, anxiety (0-1)
    
    def update(stimulus: EmotionStimulus, current: Neurotransmitter):
        # Dopamine: fast rise, exponential decay
        # Cortisol: slow rise, sustained release
```

#### Milestones
- [ ] Week 1: PAD calculator and basic state management
- [ ] Week 2: Neurotransmitter system with stimulus response
- [ ] Week 3: Half-life decay engine integration
- [ ] [ ] Week 4: Emotion → LLM prompt injection pipeline

---

### Phase 2: Memory Systems (Weeks 5-10)

#### Goals
- Implement episodic memory storage and retrieval
- Create pathological memory distortion middleware
- Build memory consolidation algorithms

#### Deliverables

| Component | Description | Priority |
|-----------|-------------|----------|
| `Hippocampus` | Vector-based episodic memory | P0 |
| `MemoryRetrieval` | Context-aware recall | P0 |
| `PathologyMiddleware` | Memory distortion layer | P0 |
| `MemoryConsolidation` | Sleep/dream simulation | P1 |
| `ForgettingMechanisms` | Natural memory decay | P1 |

#### Pathology Middleware Modules

**Alzheimer's Mode:**
```python
class AlzheimerMiddleware:
    def distort_query(query_vector: np.ndarray) -> np.ndarray:
        # Inject Gaussian noise
        noise = np.random.normal(0, self.severity, query_vector.shape)
        return query_vector + noise
        
    def block_recent_memories(memory_list: List[Memory]) -> List[Memory]:
        # Invert time weights: block recent, favor distant
        return sorted(memory_list, key=lambda m: -m.age)
```

**PTSD Mode:**
```python
class PTSDMiddleware:
    def detect_triggers(text: str) -> List[str]:
        # Match against trauma vocabulary
        return [trigger for trigger in self.trauma_triggers 
                if trigger in text.lower()]
                
    def force_retrieval(triggers: List[str]) -> List[Memory]:
        # Hard attention: override normal retrieval
        return self.get_trauma_memories(triggers)
```

**Depression Mode:**
```python
class DepressionMiddleware:
    def apply_grey_filter(memories: List[Memory]) -> List[Memory]:
        # Lower pleasure values, block positive memories
        for mem in memories:
            if mem.pleasure > 0:
                mem.pleasure *= 0.3  # Attenuate positive
        return memories
```

#### Milestones
- [ ] Week 5: Vector database integration (Chroma)
- [ ] Week 6: Memory retrieval with emotional weighting
- [ ] Week 7: Pathology middleware framework
- [ ] Week 8: Alzheimer's mode implementation
- [ ] Week 9: PTSD mode implementation
- [ ] Week 10: Memory consolidation & forgetting

---

### Phase 3: Pathology Modules (Weeks 11-16)

#### Goals
- Deepen existing pathology simulations
- Add new pathology modules
- Implement psychotherapy response systems

#### Deliverables

| Component | Description | Priority |
|-----------|-------------|----------|
| `BipolarModule` | Mood cycling simulation | P0 |
| `AnxietyDisorderModule` | Generalized anxiety | P1 |
| `AutismADHDModule` | Neurodivergent patterns | P1 |
| `TraumaRecoveryModule` | PTSD therapy simulation | P1 |
| `PsychotherapyEngine` | Therapeutic responses | P2 |

#### Pathology Specifications

**Bipolar Disorder:**
- Manic state: Elevated P+A, reduced D
- Depressive state: Low P, variable A, reduced D
- Cycling: Configurable period (hours/days/weeks)
- Trigger support: Sleep deprivation, stress events

**Anxiety Disorders:**
- Generalized: Elevated baseline cortisol
- Social: Hyper-vigilance to rejection cues
- Panic: Acute arousal spikes with physiological cascade

**Autism/ADHD:**
- Monotropic attention: Intense focus on special interests
- Emotional intensity: Raw, unfiltered expressions
- Executive function: Working memory constraints
- ADHD: Reward sensitivity, delay discounting

#### Milestones
- [ ] Week 11: Bipolar module (full cycling)
- [ ] Week 12: Anxiety disorder module
- [ ] Week 13: Autism/ADHD module
- [ ] Week 14: Trauma recovery simulation
- [ ] Week 15: Psychotherapy engine
- [ ] Week 16: Pathology module testing & refinement

---

### Phase 4: Advanced Features (Weeks 17-24)

#### Goals
- Cross-platform memory integration
- Embodied cognition
- Advanced consciousness simulation
- Production deployment

#### Deliverables

| Component | Description | Priority |
|-----------|-------------|----------|
| `ObsidianAdapter` | Vault sync | P0 |
| `FlowUsAdapter` | Workspace sync | P0 |
| `EmbodiedCognition` | Sensorimotor integration | P1 |
| `Metacognition` | Self-awareness layer | P1 |
| `ConsciousnessModel` | Phenomenal experience sim | P2 |
| `ProductionAPI` | REST API with auth | P0 |

#### Cross-Platform Integration Details

**Obsidian Adapter:**
```python
class ObsidianAdapter:
    def __init__(self, vault_path: str):
        self.vault = Vault(vault_path)
        self.observer = FileObserver(vault_path)
        
    async def sync_notes(self) -> SyncResult:
        # Pull changes
        local_changes = self.vault.get_changed_files()
        remote_changes = await self.api.get_changes()
        
        # Merge with conflict resolution
        merged = self.merge(local_changes, remote_changes)
        
        # Push merged state
        await self.vault.write(merged)
        await self.api.write(merged)
        
        return merged
```

**FlowUs Adapter:**
```python
class FlowUsAdapter:
    def __init__(self, workspace_id: str, token: str):
        self.workspace_id = workspace_id
        self.api = FlowUsAPI(token)
        
    async def sync_page(self, page_id: str) -> Page:
        page = await self.api.get_page(page_id)
        # Convert FlowUs blocks → Markdown
        markdown = self.blocks_to_markdown(page.blocks)
        # Inject emotional metadata
        enriched = self.add_emotional_context(markdown)
        return enriched
```

#### Embodied Cognition

- Integrate sensor inputs (camera, microphone, location)
- Map physical states to emotional responses
- Implement "embodied memory" (context tied to location/time)

#### Metacognition & Consciousness

- Self-reflection prompts (system analyzes its own state)
- Theory of mind simulation (model user's mental state)
- Metacognitive monitoring (aware of own limitations)

#### Milestones
- [ ] Week 17-18: Core sync engine
- [ ] Week 19-20: Obsidian/FlowUs adapters
- [ ] Week 21: Embodied cognition foundation
- [ ] Week 22: Metacognition layer
- [ ] Week 23: Production API & deployment
- [ ] Week 24: Testing, documentation, launch

---

## Phase Dependencies

```
Phase 1 (Core)
    │
    ├──▶ Phase 2 (Memory)
    │        │
    │        ├──▶ Phase 3 (Pathology)
    │        │        │
    │        │        └──▶ Phase 4 (Advanced)
    │        │
    │        └──▶ Phase 4 (Advanced) ──▶ Cross-Platform
    │
    └──▶ Phase 4 (Advanced) ──▶ Production API
```

---

## Technical Requirements

### Backend
- Python 3.10+
- FastAPI for REST API
- ChromaDB for vector storage
- SQLite for state persistence
- Neo4j (optional) for graph knowledge

### External Integrations
- Obsidian: Local file system + REST API
- FlowUs: REST API v1
- LLM Provider: OpenAI / Anthropic / Local

### Infrastructure
- Docker for containerization
- Redis for caching (optional)
- PostgreSQL for production (optional)

---

## Testing Strategy

| Layer | Approach |
|-------|----------|
| Unit | pytest for core math (PAD, decay, neurotransmitters) |
| Integration | E2E for memory retrieval, pathology modes |
| User Acceptance | Human evaluation of emotional authenticity |
| Performance | Load testing for concurrent sessions |

---

## Future Considerations

### Phase 5+ (Post-Launch)
- Multi-agent emotional networks
- Real-time physiological sensors (heart rate, GSR)
- VR/AR embodiment
- Collaborative consciousness simulation

### Research Directions
- Cross-cultural emotion modeling
- Developmental psychology simulation
- Quantum-inspired memory (superposition of emotional states)

---

## Appendix: File Structure

```
limbic_flow/
├── core/
│   ├── emotion/
│   │   ├── pad_calculator.py
│   │   ├── neurotransmitter.py
│   │   ├── decay_engine.py
│   │   └── state.py
│   ├── memory/
│   │   ├── hippocampus.py
│   │   ├── retrieval.py
│   │   ├── consolidation.py
│   │   └── forgetting.py
│   └── cognition/
│       ├── reconstruction.py
│       ├── expression.py
│       └── metacognition.py
├── middleware/
│   ├── pathology/
│   │   ├── alzheimer.py
│   │   ├── ptsd.py
│   │   ├── depression.py
│   │   ├── bipolar.py
│   │   ├── anxiety.py
│   │   └── autism_adhd.py
│   └── base.py
├── adapters/
│   ├── obsidian/
│   │   ├── adapter.py
│   │   ├── sync.py
│   │   └── metadata.py
│   └── flowus/
│       ├── adapter.py
│       ├── sync.py
│       └── metadata.py
└── api/
    ├── routes.py
    ├── models.py
    └── auth.py
```

---

*End of Implementation Roadmap*
