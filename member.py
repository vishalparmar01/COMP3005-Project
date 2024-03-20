class Member:
    def __init__(self, db_connection, name, email, password):
        self.db_connection = db_connection
        self.name = name
        self.email = email
        self.password = password
        self.id = None
        self.fitness_goal = None
        self.health_metrics = None


    def register(self):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO members (name, email, password, fitness_goal, health_metrics) VALUES (%s, %s, %s, %s, %s)", (self.name, self.email, self.password, self.fitness_goal, self.health_metrics))
        cursor.execute("SELECT LASTVAL()")
        self.id = cursor.fetchone()[0]
        self.db_connection.commit()
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

    def update_profile(self, db_connection, field, value):
        cursor = db_connection.cursor()
        print("Updated the password ",self.id)
        cursor.execute(f'''
            UPDATE members
            SET {field} = %s
            WHERE id = %s
        ''',(value, self.id))
        # cursor.execute(f"UPDATE members SET {field} = %s WHERE id = %s", (value, self.id))
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