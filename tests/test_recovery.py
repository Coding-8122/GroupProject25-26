from app.utils.recovery_calculations import calculate_recovery_hours

def run_spike():
    print("--- 🧪 Recovery Algorithm Technical Spike 🧪 ---")
    
    scenarios = [
        {"name": "The 'Fresh' User", "intensity": 3, "soreness": 1, "sleep": 9},
        {"name": "The 'Average' Day", "intensity": 6, "soreness": 4, "sleep": 7},
        {"name": "The 'Over-trained' Athlete", "intensity": 10, "soreness": 9, "sleep": 4},
        {"name": "No Workout (Rest Day)", "intensity": 0, "soreness": 2, "sleep": 8},
    ]

    for s in scenarios:
        result = calculate_recovery_hours(s['intensity'], s['soreness'], s['sleep'])
        print(f"\nScenario: {s['name']}")
        print(f"Inputs: Intensity {s['intensity']}, Soreness {s['soreness']}, Sleep {s['sleep']}h")
        print(f"Result: {result} hours of recovery needed.")
        
        # Validation Logic
        if s['name'] == "The 'Over-trained' Athlete" and result < 48:
            print("❌ FAILURE: Recovery estimate too low for extreme fatigue.")
        elif result < 0:
            print("❌ FAILURE: Algorithm returned a negative number.")
        else:
            print("✅ SUCCESS: Result within expected range.")

if __name__ == "__main__":
    run_spike()