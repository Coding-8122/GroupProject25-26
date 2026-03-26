import pytest
from app.utils.recovery_calculations import calculate_recovery_hours

def test_calculate_recovery_low_intensity():
    # Baseline: intensity 2, soreness 1, sleep 8
    # Calculation: 24 + (2 * 3) + (1 * 2.5) + 0 = 32.5 -> 32
    hours = calculate_recovery_hours(intensity=2, soreness=1, sleep_hours=8)
    assert hours == 32

def test_calculate_recovery_high_intensity():
    # High intensity, bad sleep, high soreness
    # Calculation: 24 + (9 * 3) + (8 * 2.5) + ((7 - 4) * 5) = 24 + 27 + 20 + 15 = 86
    hours = calculate_recovery_hours(intensity=9, soreness=8, sleep_hours=4)
    assert hours == 86

def test_recovery_baseline():
    # Average intensity, soreness, and 7.5h sleep (no sleep adjustment)
    # Calculation: 24 + (5 * 3) + (5 * 2.5) = 24 + 15 + 12.5 = 51.5 -> 52
    assert calculate_recovery_hours(intensity=5, soreness=5, sleep_hours=7.5) == 52

def test_recovery_extra_sleep():
    # Bonus for long sleep (>8h)
    # Calculation: 51.5 - 4 = 47.5 -> 48
    assert calculate_recovery_hours(intensity=5, soreness=5, sleep_hours=9) == 48

def test_recovery_sleep_deprivation():
    # Penalty for low sleep (<7h)
    # Calculation: 51.5 + ((7 - 5) * 5) = 51.5 + 10 = 61.5 -> 62
    assert calculate_recovery_hours(intensity=5, soreness=5, sleep_hours=5) == 62

def test_recovery_max_intensity():
    # High intensity and high soreness
    # Calculation: 24 + (10 * 3) + (10 * 2.5) = 24 + 30 + 25 = 79
    assert calculate_recovery_hours(intensity=10, soreness=10, sleep_hours=8) == 79