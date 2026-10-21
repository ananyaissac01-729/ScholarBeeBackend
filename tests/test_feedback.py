from app.services.feedback import FeedbackStore


def test_reward_rules_and_adjustment_are_applied():
    store = FeedbackStore()
    assert store.record("s1", "demo-python", "completed") == 1.0
    assert store.adjustments_for("s1")["demo-python"] == 0.15
    store.record("s1", "demo-python", "disliked")
    assert store.adjustments_for("s1")["demo-python"] == 0.0
    assert store.adjustments_for("another") == {}
