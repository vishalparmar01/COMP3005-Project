class Member:
    def __init__(self, db_connection, name, email, password):
        self.db_connection = db_connection
        self.name = name
        self.email = email
        self.password = password
        self.id = None
        self.fitness_goal = None
        self.health_metrics = None


    @staticmethod
    def create_table(db_connection):
                # Create the members table if it doesn't exist
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                fitness_goal VARCHAR(255),
                health_metrics VARCHAR(255)
            )
        """)
        db_connection.commit()
        cursor.close()

        # Create the training_sessions table if it doesn't exist
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_sessions (
                id SERIAL PRIMARY KEY,
                member_id INT NOT NULL,
                trainer_id INT NOT NULL,
                session_date DATE,
                session_time TIME,
                FOREIGN KEY (member_id) REFERENCES members(id),
                FOREIGN KEY (trainer_id) REFERENCES trainers(id)
            )
        """)
        db_connection.commit()
        cursor.close()

        # Create the class_registrations table if it doesn't exist
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS class_registrations (
                id SERIAL PRIMARY KEY,
                member_id INT NOT NULL,
                class_id INT NOT NULL,
                FOREIGN KEY (member_id) REFERENCES members(id),
                FOREIGN KEY (class_id) REFERENCES classes(id)
            )
        """)
        db_connection.commit()
        cursor.close()


    def register(self):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO members (name, email, password, fitness_goal, health_metrics) VALUES (%s, %s, %s, %s, %s)", (self.name, self.email, self.password, self.fitness_goal, self.health_metrics))
        self.db_connection.commit()
        self.id = cursor.lastrowid
        cursor.close()

    @staticmethod
    def get_member_by_email(db_connection, email):
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM members WHERE email = %s", (email,))
        member_data = cursor.fetchone()
        cursor.close()
        if member_data:
            member = Member(db_connection, member_data[1], member_data[2], member_data[3])
            member.id = member_data[0]
            member.fitness_goal = member_data[4]
            member.health_metrics = member_data[5]
            return member
        return None

    def update_profile(self, field, value):
        cursor = self.db_connection.cursor()
        cursor.execute(f"UPDATE members SET {field} = %s WHERE id = %s", (value, self.id))
        self.db_connection.commit()
        cursor.close()

    def schedule_training_session(self, trainer_id, session_date, session_time):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO training_sessions (member_id, trainer_id, session_date, session_time) VALUES (%s, %s, %s, %s)", (self.id, trainer_id, session_date, session_time))
        self.db_connection.commit()
        cursor.close()

    def register_for_class(self, class_id):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO class_registrations (member_id, class_id) VALUES (%s, %s)", (self.id, class_id))
        self.db_connection.commit()
        cursor.close()