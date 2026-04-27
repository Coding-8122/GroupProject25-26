import pytest
from app.utils.recovery_calculations import calculate_recovery_hours

def test_calculate_recovery_logic():
    """Test recovery calculation with various intensity/sleep scenarios."""
    assert calculate_recovery_hours(intensity=2, soreness=1, sleep_hours=8) == 32
    assert calculate_recovery_hours(intensity=9, soreness=8, sleep_hours=4) == 86
    assert calculate_recovery_hours(intensity=10, soreness=10, sleep_hours=8) == 79