import csv
import io

def generate_workout_csv(workouts):
    # Create an in-memory "file" to write to
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write the Header row
    writer.writerow(['Date', 'Exercise', 'Sets', 'Reps', 'Weight (kg)'])
    
    # Write the data rows
    for w in workouts:
        writer.writerow([w.date.strftime('%Y-%m-%d'), w.exercise_name, w.sets, w.reps, w.weight])
    
    return output.getvalue()