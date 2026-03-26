import pytest
from app.utils.recovery_calculations import calculate_recovery_hours

def test_recovery_baseline():
    """Test with average intensity, soreness and 7-8h sleep (no sleep adjustment)."""
    # 24 + (5*3) + (5*2.5) = 24 + 15 + 12.5 = 51.5 -> round to 52
    assert calculate_recovery_hours(intensity=5, soreness=5, sleep_hours=7.5) == 52

def test_recovery_extra_sleep():
    """Test bonus for long sleep (>8h)."""
    # Base 51.5 - 4 = 47.5 -> round to 48
    assert calculate_recovery_hours(intensity=5, soreness=5, sleep_hours=9) == 48

def test_recovery_sleep_deprivation():
    """Test penalty for low sleep (<7h)."""
    # Base 51.5 + (7-5)*5 = 51.5 + 10 = 61.5 -> round to 62
    assert calculate_recovery_hours(intensity=5, soreness=5, sleep_hours=5) == 62

def test_recovery_max_intensity():
    """Test high intensity and high soreness."""
    # 24 + (10*3) + (10*2.5) = 24 + 30 + 25 = 79
    assert calculate_recovery_hours(intensity=10, soreness=10, sleep_hours=8) == 79