class Trainer:
    db_connection = None

    def __init__(self, id=None, name=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    @classmethod
    def register(cls, db_connection, name, email, password):
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO trainers (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password),
        )
        cursor.execute("SELECT LASTVAL()")
        trainer_id = cursor.fetchone()[0]
        db_connection.commit()
        cursor.close()
        return trainer_id

    @classmethod
    def get_trainer_by_name(cls, db_connection, name):
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM trainers WHERE name = %s", (name,))
        trainer_data = cursor.fetchone()
        cursor.close()
        if trainer_data:
            return cls.from_db_data(db_connection, trainer_data)
        else:
            raise ValueError("No such trainer")

    @classmethod
    def manage_schedule(cls, db_connection, trainer_name, available_times):
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM trainers WHERE name = %s", (trainer_name,))
        trainer_id = cursor.fetchone()[0]
        cursor.execute(
            "DELETE FROM trainer_schedule WHERE trainer_id = %s", (trainer_id,)
        )
        for time in available_times:
            cursor.execute(
                "INSERT INTO trainer_schedule (trainer_id, available_time) VALUES (%s, %s)",
                (trainer_id, time),
            )
        db_connection.commit()
        cursor.close()

    @classmethod
    def from_db_data(cls, db_connection, trainer_data):
        trainer = cls()
        trainer.db_connection = db_connection
        trainer.id = trainer_data[0]
        trainer.name = trainer_data[1]
        trainer.email = trainer_data[2]
        trainer.password = trainer_data[3]
        return trainer

    @classmethod
    def get_available_trainers(cls, db_connection, session_date, session_time):
        cursor = db_connection.cursor()
        cursor.execute(
            """
            SELECT * FROM trainers
            WHERE id NOT IN (
                SELECT DISTINCT trainer_id
                FROM training_sessions
                WHERE session_date = %s AND session_time = %s
            )
        """,
            (session_date, session_time),
        )
        trainers = []
        for trainer_data in cursor.fetchall():
            trainer_id = trainer_data[0]
            # Check if session_time is in the trainer's schedule
            cursor.execute(
                """
                SELECT * FROM trainer_schedule
                WHERE trainer_id = %s AND available_time = %s
            """,
                (trainer_id, session_time),
            )
            if cursor.fetchone() is not None:
                trainer = cls.from_db_data(db_connection, trainer_data)
                trainer.id = trainer_id
                trainers.append(trainer)
        cursor.close()
        if not trainers:
            print("There are no trainers available at the mentioned time")
        return trainers

    @classmethod
    def search_member_profile_by_name(cls, db_connection, member_name):
        # Search for a member profile by name
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM members WHERE name = %s", (member_name,))
        member_data = cursor.fetchone()
        cursor.close()
        return member_data
