
class Trainer:
    def __init__(self, db_connection, name, email, password):
        self.db_connection = db_connection
        self.name = name
        self.email = email
        self.password = password
        self.id = None

    def register(self):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO trainers (name, email, password) VALUES (%s, %s, %s)", (self.name, self.email, self.password))
        cursor.execute("SELECT LASTVAL()")
        self.id = cursor.fetchone()[0]
        self.db_connection.commit()
        cursor.close()

    @staticmethod
    def get_trainer_by_email(db_connection, email):
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM trainers WHERE email = %s", (email,))
        trainer_data = cursor.fetchone()
        cursor.close()
        if trainer_data:
            return Trainer(db_connection, trainer_data[1], trainer_data[2], trainer_data[3])
        return None
    
    def manage_schedule(self, available_times):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM trainer_schedule WHERE trainer_id = %s", (self.id,))
        for time in available_times:
            cursor.execute("INSERT INTO trainer_schedule (trainer_id, available_time) VALUES (%s, %s)", (self.id, time))
        self.db_connection.commit()
        cursor.close()

    @staticmethod
    def get_available_trainers(db_connection, session_date, session_time):
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM trainers WHERE id NOT IN (SELECT DISTINCT trainer_id FROM training_sessions WHERE session_date = %s AND session_time = %s)", (session_date, session_time))
        trainers = []
        for trainer_data in cursor.fetchall():
            trainer = Trainer(db_connection, trainer_data[1], trainer_data[2], trainer_data[3])
            trainer.id = trainer_data[0]
            trainers.append(trainer)
        cursor.close()
        return trainers
    
    def search_member_profile_by_name(self, member_name, member):
        # Search for a member profile by name
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM members WHERE name = %s", (member_name,))
        member_data = cursor.fetchone()
        cursor.close()
        if member_data:
            # Update the provided member object with retrieved data
            member.id = member_data[0]
            member.name = member_data[1]
            member.email = member_data[2]
            member.password = member_data[3]
            member.fitness_goal = member_data[4]
            member.health_metrics = member_data[5]
            return member
        return None
    
