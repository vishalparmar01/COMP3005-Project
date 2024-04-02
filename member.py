from trainer import Trainer
from staff import AdministrativeStaff

class Member:
    @classmethod
    def register(
        cls,
        db_connection,
        name,
        email,
        password,
        fitness_goal=None,
        health_metrics=None,
    ):
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO members (name, email, password, fitness_goal, health_metrics) VALUES (%s, %s, %s, %s, %s)",
            (name, email, password, fitness_goal, health_metrics),
        )
        cursor.execute("SELECT LASTVAL()")
        member_id = cursor.fetchone()[0]
        db_connection.commit()
        cursor.close()
        return member_id

    @classmethod
    def update_profile(cls, db_connection, name, field, value):
        cursor = db_connection.cursor()
        cursor.execute(
            f"""
             UPDATE members
             SET {field} = %s
             WHERE name = %s
         """,
            (value, name),
        )
        db_connection.commit()
        cursor.close()

    @classmethod
    def schedule_training_session(
        cls, db_connection, member_name, trainer_name, session_date, session_time
    ):
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM members WHERE name = %s", (member_name,))
        member_id = cursor.fetchone()[0]

        # Find the trainer ID based on the trainer name
        cursor.execute("SELECT id FROM trainers WHERE name = %s", (trainer_name,))
        trainer_id = cursor.fetchone()[0]

        avail_trainers = Trainer.get_available_trainers(
            db_connection, session_date, session_time
        )
        # Check if the requested trainer is available
        if not any(trainer.name == trainer_name for trainer in avail_trainers):
            print(f"Trainer: {trainer_name}, is not available at this time.")
        else:
            cursor.execute(
                "INSERT INTO training_sessions (member_id, trainer_id, session_date, session_time) VALUES (%s, %s, %s, %s)",
                (member_id, trainer_id, session_date, session_time),
            )
            db_connection.commit()
        cursor.close()

    @classmethod
    def register_for_class(cls, db_connection, member_name, class_id):
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM members WHERE name = %s", (member_name,))
        member_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO class_registrations (member_id, class_id) VALUES (%s, %s)",
            (member_id, class_id),
        )
        db_connection.commit()
        cursor.close()
