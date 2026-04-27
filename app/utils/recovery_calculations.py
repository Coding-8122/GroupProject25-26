def calculate_recovery_hours(intensity, soreness, sleep_hours):
    # Base rest time is 24 hours as a starting point 
    recovery_time = 24
    
    # Use the RPE scale from the PIR to add intensity hours 
    intensity_weight = intensity * 3
    recovery_time += intensity_weight
    
    # Add hours for muscle soreness reported by the user 
    soreness_penalty = soreness * 2.5
    recovery_time += soreness_penalty
    
    # Subtract or add time based on sleep quality 
    if sleep_hours < 7:
        # Penalty for less than 7 hours of sleep
        sleep_adjustment = (7 - sleep_hours) * 5
        recovery_time += sleep_adjustment
    elif sleep_hours > 8:
        # Bonus for getting extra recovery sleep
        recovery_time -= 4
        
    return round(recovery_time)