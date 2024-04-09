from .trainer import Trainer
from .staff import AdministrativeStaff

class Member:
    @classmethod
    def register(
        cls,
        db_connection,
        name,
        email,
        password,
        fitness_goal=None,
        weight=None,
        height=None,
    ):
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO members (name, email, password, fitness_goal) VALUES (%s, %s, %s, %s)",
            (name, email, password, fitness_goal),
        )
        cursor.execute("SELECT LASTVAL()")
        member_id = cursor.fetchone()[0]
        
        # Insert health metrics if weight and height are provided
        if weight is not None and height is not None:
            cursor.execute(
                "INSERT INTO health_metrics (member_id, weight, height) VALUES (%s, %s, %s)",
                (member_id, weight, height),
            )

        db_connection.commit()
        cursor.close()
        return member_id

    @classmethod
    def update_member(cls, db_connection, member_name, field, value):
        cursor = db_connection.cursor()
        
        if field == 'weight':
            # Get the member ID for the given member name
            cursor.execute("SELECT id FROM members WHERE name = %s", (member_name,))
            member_id = cursor.fetchone()[0]
            
            # Insert the new weight entry
            cursor.execute(
                "INSERT INTO health_metrics (member_id, weight) VALUES (%s, %s)",
                (member_id, value),
            )
        else:
            # Update the profile field
            cursor.execute(
                f"""
                UPDATE members
                SET {field} = %s
                WHERE name = %s
            """,
                (value, member_name),
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
    def register_for_class(cls, db_connection, member_name, class_name):
        cursor = db_connection.cursor()
        
        # Get the member_id for the given member_name
        cursor.execute("SELECT id FROM members WHERE name = %s", (member_name,))
        member_id = cursor.fetchone()[0]
        
        # Get the class_id for the given class_name
        cursor.execute("SELECT id FROM classes WHERE class_name = %s", (class_name,))
        class_id = cursor.fetchone()[0]
        
        # Insert the registration into class_registrations
        cursor.execute(
            "INSERT INTO class_registrations (member_id, class_id) VALUES (%s, %s)",
            (member_id, class_id),
        )
        db_connection.commit()
        cursor.close()

    @classmethod
    def book_room(cls, db_connection, member_name, booking_date, booking_time):
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM members WHERE name = %s", (member_name,))
        member_id = cursor.fetchone()
        cursor.close()
        
        if not member_id:
            raise ValueError("No member found with the given name")

        # Use the manage_room_booking method from AdministrativeStaff
        room_number = AdministrativeStaff.manage_room_booking(db_connection, member_id[0], booking_date, booking_time)
        return room_number if room_number else None

    
    @classmethod
    def display_dashboard(cls, db_connection, member_name):
        cursor = db_connection.cursor()
        
        # Initialize empty lists for health metrics and classes
        health_metrics = []
        classes = []

        # Get the member ID for the given member name
        cursor.execute("SELECT id FROM members WHERE name = %s", (member_name,))
        result = cursor.fetchone()
        if result:
            member_id = result[0]
            
            # Retrieve health metrics for the member
            cursor.execute("SELECT * FROM health_metrics WHERE member_id = %s", (member_id,))
            health_metrics = cursor.fetchall()

            # Retrieve class registrations for the member
            cursor.execute("SELECT class_id FROM class_registrations WHERE member_id = %s", (member_id,))
            class_ids = cursor.fetchall()
            for class_id in class_ids:
                cursor.execute("SELECT * FROM classes WHERE id = %s", (class_id,))
                class_info = cursor.fetchone()
                if class_info:
                    classes.append(class_info)

        cursor.close()
        return health_metrics, classes  # Always return a tuple
