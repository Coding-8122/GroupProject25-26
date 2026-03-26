import pytest
from app.utils.recovery_calculations import calculate_recovery_hours

def test_calculate_recovery_low_intensity():
    hours = calculate_recovery_hours(intensity=2, soreness=1, sleep_hours=8)
    assert hours == 32

def test_calculate_recovery_high_intensity():
    hours = calculate_recovery_hours(intensity=9, soreness=8, sleep_hours=4)
    assert hours == 86

def test_recovery_baseline():
    assert calculate_recovery_hours(intensity=5, soreness=5, sleep_hours=7.5) == 52

def test_recovery_extra_sleep():
    assert calculate_recovery_hours(intensity=5, soreness=5, sleep_hours=9) == 48

def test_recovery_sleep_deprivation():
    assert calculate_recovery_hours(intensity=5, soreness=5, sleep_hours=5) == 62

def test_recovery_max_intensity():
    assert calculate_recovery_hours(intensity=10, soreness=10, sleep_hours=8) == 79