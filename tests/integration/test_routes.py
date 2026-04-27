import pytest

def test_dashboard_protection(client):
    """Ensure dashboard is protected by login_required and returns 401."""
    res = client.get("/dashboard")
    # Updated to 401 per security hardening policy
    assert res.status_code == 401

def test_metrics_negative_weight_rejection(authenticated_client, app):
    """Red Team Test: Ensure negative weight is rejected by the form."""
    res = authenticated_client.post(
        "/metrics",
        data={"date": "2026-04-09", "weight": -10.0, "body_fat": 10},
        follow_redirects=True,
    )

    assert b"Weight must be between" in res.data
    with app.app_context():
        from app.models.body_metric import BodyMetric
        assert BodyMetric.query.filter_by(weight=-10.0).first() is None