from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.workout import WorkoutLog
from app.models.body_metric import BodyMetric
from datetime import datetime, timedelta
import random

app = create_app()


def seed_data():
    with app.app_context():
        print("Cleaning old data...")
        db.drop_all()
        db.create_all()

        print("Creating demo user...")
        demo_user = User(
            email="demo@example.com", gender="male", height=180.0, weight=80.0
        )
        demo_user.set_password("password")
        db.session.add(demo_user)
        db.session.commit()

        print("Generating 30 days of data...")
        start_date = datetime.utcnow().date() - timedelta(days=30)
        muscles = ["Chest", "Back", "Legs", "Shoulders", "Arms"]

        for i in range(30):
            current_date = start_date + timedelta(days=i)

            # Simulated Weight Loss
            weight = 85.0 - (i * 0.15) + random.uniform(-0.5, 0.5)
            fat = 20.0 - (i * 0.1) + random.uniform(-0.2, 0.2)
            metric = BodyMetric(
                user_id=demo_user.id,
                date=current_date,
                weight=round(weight, 1),
                body_fat=round(fat, 1),
            )
            db.session.add(metric)

            # Simulated Workouts (4 times a week)
            if i % 7 != 0 and i % 7 != 4:
                workout = WorkoutLog(
                    user_id=demo_user.id,
                    date=current_date,
                    exercise_name=f"Exercise {i}",
                    muscle_group=random.choice(muscles),
                    intensity=random.randint(6, 9),
                    sets=random.randint(3, 5),
                    reps=random.randint(8, 12),
                    weight=random.randint(40, 100),
                )
                db.session.add(workout)

        db.session.commit()
        print("Done! Login with demo@example.com / password")


if __name__ == "__main__":
    seed_data()
