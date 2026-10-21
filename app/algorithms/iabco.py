"""A transparent ABC-inspired course-ranking prototype.

This module implements a small, deterministic bee-colony-style search over
course orderings. It is an educational prototype, not a verified reproduction
of the paper's Improved ABC Optimisation details. Compare it against the paper
and validate it before making research fidelity claims.
"""

from __future__ import annotations

import random
from app.models.course import Course, RecommendedCourse
from app.models.student import StudentPreferences

_DIFFICULTY = {"beginner": 0, "intermediate": 1, "advanced": 2}


def _affinity(course: Course, preferences: StudentPreferences, feedback_adjustment: float) -> float:
    interests = {value.casefold() for value in preferences.interests}
    skills = {value.casefold() for value in preferences.skills}
    topic_match = len(interests.intersection(x.casefold() for x in course.interests))
    skill_match = len(skills.intersection(x.casefold() for x in course.skills))
    topic_score = min(topic_match / max(len(interests), 1), 1.0)
    skill_score = min(skill_match / max(len(skills), 1), 1.0)
    target = _DIFFICULTY[preferences.preferred_difficulty]
    distance = abs(_DIFFICULTY.get(course.difficulty, 1) - target)
    difficulty_score = max(0.0, 1.0 - 0.35 * distance)
    score = 0.55 * topic_score + 0.20 * skill_score + 0.25 * difficulty_score
    return max(0.0, min(1.0, score + feedback_adjustment))


def recommend_courses(
    courses: list[Course], preferences: StudentPreferences, *, limit: int = 5,
    adjustments: dict[str, float] | None = None, seed: int = 7,
) -> list[RecommendedCourse]:
    """Rank courses using affinity and a bounded ABC-style ordering search.

    Employed/onlooker behavior tries order swaps; scout behavior resets a
    stagnant candidate. The objective is total affinity with stable tie breaks.
    """
    if not courses or limit <= 0:
        return []
    adjustments = adjustments or {}
    scores = {c.id: _affinity(c, preferences, adjustments.get(c.id, 0.0)) for c in courses}
    rng = random.Random(seed)
    initial = sorted(range(len(courses)), key=lambda i: (-scores[courses[i].id], courses[i].id))
    population = [initial[:]]
    while len(population) < min(8, len(courses) + 1):
        candidate = initial[:]
        if len(candidate) > 1:
            a, b = rng.sample(range(len(candidate)), 2)
            candidate[a], candidate[b] = candidate[b], candidate[a]
        population.append(candidate)

    def objective(order: list[int]) -> float:
        # Earlier positions have more influence on the ranked list objective.
        return sum(scores[courses[index].id] / (position + 1) for position, index in enumerate(order))

    best = max(population, key=objective)
    stagnation = [0] * len(population)
    for _ in range(30):
        for bee in range(len(population)):
            candidate = population[bee][:]
            if len(candidate) > 1:
                a, b = rng.sample(range(len(candidate)), 2)
                candidate[a], candidate[b] = candidate[b], candidate[a]
            if objective(candidate) > objective(population[bee]):
                population[bee], stagnation[bee] = candidate, 0
            else:
                stagnation[bee] += 1
            if stagnation[bee] >= 5:
                population[bee] = initial[:]
                stagnation[bee] = 0
        # Onlookers choose the current best candidate as the colony guide.
        colony_best = max(population, key=objective)
        if objective(colony_best) > objective(best):
            best = colony_best[:]

    result = []
    for index in best[:limit]:
        course = courses[index]
        score = scores[course.id]
        result.append(RecommendedCourse(**course.model_dump(), match_score=round(score, 4), reason="Ranked from preference overlap, difficulty fit, and recorded feedback."))
    return result
