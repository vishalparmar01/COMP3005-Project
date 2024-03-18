class Trainer:
    def __init__(self, db_connection, name, email, password):
        self.db_connection = db_connection
        self.name = name
        self.email = email
        self.password = password
        self.id = None

         # Create the trainers table if it doesn't exist
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trainers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        db_connection.commit()
        cursor.close()

        # Create the trainer_schedule table if it doesn't exist
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trainer_schedule (
                id INT AUTO_INCREMENT PRIMARY KEY,
                trainer_id INT NOT NULL,
                available_time TIME,
                FOREIGN KEY (trainer_id) REFERENCES trainers(id)
            )
        """)
        db_connection.commit()
        cursor.close()

    def register(self):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO trainers (name, email, password) VALUES (%s, %s, %s)", (self.name, self.email, self.password))
        self.db_connection.commit()
        self.id = cursor.lastrowid
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
