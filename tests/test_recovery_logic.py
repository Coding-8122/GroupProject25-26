import pytest
from app.utils.recovery_calculations import calculate_recovery_hours

def test_calculate_recovery_low_intensity():
    # Baseline: Low intensity, good sleep, no soreness
    hours = calculate_recovery_hours(intensity=2, soreness=1, sleep_hours=8)
    assert hours < 24 # Should be ready within a day

def test_calculate_recovery_high_intensity():
    # Stress test: High intensity, bad sleep, high soreness
    hours = calculate_recovery_hours(intensity=9, soreness=8, sleep_hours=4)
    assert hours > 48 # Should require significant rest