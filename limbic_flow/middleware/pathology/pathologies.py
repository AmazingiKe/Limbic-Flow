from typing import Any, Dict, List
import time
import numpy as np

from limbic_flow.middleware.pathology.base import PathologyBase


class DepressionPathology(PathologyBase):
    def __init__(self, base_severity: float = 0.3):
        self.base_severity = base_severity

    @property
    def name(self) -> str:
        return "depression"

    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        cortisol = emotional_state.get("cortisol", 0.0)
        pleasure = emotional_state.get("pleasure", 0.0)
        return cortisol > 0.4 or pleasure < -0.2

    def _calculate_dynamic_severity(self, emotional_state: Dict[str, Any]) -> float:
        cortisol = emotional_state.get("cortisol", 0.3)
        cortisol_boost = max(0.0, (cortisol - 0.4) * 1.0)
        return min(1.0, self.base_severity + cortisol_boost)

    def distort_query(self, query_vector: Any, emotional_state: Dict[str, Any]) -> Any:
        if query_vector is None:
            return query_vector
        severity = self._calculate_dynamic_severity(emotional_state)
        distortion = np.full_like(query_vector, -0.1 * severity)
        return query_vector + distortion

    def distort_memories(
        self,
        memories: List[Dict[str, Any]],
        emotional_state: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        if not memories:
            return memories

        severity = self._calculate_dynamic_severity(emotional_state)
        distorted_memories = []

        for memory in memories:
            mem_copy = memory.copy()
            if "pad" in memory:
                mem_copy["pad"] = memory["pad"].copy()

            memory_pleasure = mem_copy.get("pad", {}).get("pleasure", 0.0)

            if memory_pleasure > 0.2:
                if np.random.random() < 0.8 * severity:
                    continue

            if "pad" in mem_copy:
                mem_copy["pad"]["pleasure"] *= (1.0 - 0.8 * severity)

            distorted_memories.append(mem_copy)

        return distorted_memories


class AlzheimerPathology(PathologyBase):
    def __init__(self, severity: float = 0.5):
        self.severity = severity

    @property
    def name(self) -> str:
        return "alzheimer"

    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        return True

    def distort_query(self, query_vector: Any, emotional_state: Dict[str, Any]) -> Any:
        if query_vector is None:
            return query_vector
        noise = np.random.normal(0, 0.2 * self.severity, size=query_vector.shape)
        return query_vector + noise

    def distort_memories(
        self,
        memories: List[Dict[str, Any]],
        emotional_state: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        if not memories:
            return memories

        distorted_memories = []
        current_time = emotional_state.get("timestamp", time.time())

        for memory in memories:
            memory_time = memory.get("timestamp", 0)
            time_diff = current_time - memory_time

            if time_diff < 86400:
                if np.random.random() < 0.8 * self.severity:
                    continue
            elif time_diff < 604800:
                if np.random.random() < 0.5 * self.severity:
                    continue

            distorted_memories.append(memory)

        return distorted_memories
