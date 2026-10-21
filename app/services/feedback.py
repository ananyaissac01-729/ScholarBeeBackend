"""In-memory feedback and simple reward-based preference adjustments."""

from collections import defaultdict
from dataclasses import dataclass

REWARDS = {"completed": 1.0, "started": 0.3, "skipped": -0.5, "disliked": -1.0}


@dataclass
class FeedbackEvent:
    student_id: str
    course_id: str
    outcome: str
    reward: float


class FeedbackStore:
    """Demo-only in-memory event store; data resets when the process restarts."""

    def __init__(self) -> None:
        self.events: list[FeedbackEvent] = []
        self._totals: dict[tuple[str, str], list[float]] = defaultdict(lambda: [0.0, 0.0])

    def record(self, student_id: str, course_id: str, outcome: str) -> float:
        reward = REWARDS[outcome]
        self.events.append(FeedbackEvent(student_id, course_id, outcome, reward))
        total = self._totals[(student_id, course_id)]
        total[0] += reward
        total[1] += 1
        return reward

    def adjustments_for(self, student_id: str) -> dict[str, float]:
        # Average reward contributes at most +/- 0.15 to a later ranking.
        return {course_id: max(-0.15, min(0.15, (values[0] / values[1]) * 0.15))
                for (owner, course_id), values in self._totals.items() if owner == student_id and values[1]}


feedback_store = FeedbackStore()
