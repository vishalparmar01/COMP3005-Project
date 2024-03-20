import psycopg2
from member import Member
from staff import AdministrativeStaff
from trainer import Trainer

# Function to create all tables
def create_tables(db_connection):
    try:
        # Create a cursor object using the connection
        cursor = db_connection.cursor()

        cursor.execute("""
        DROP TABLE IF EXISTS trainer_schedule, class_registrations, training_sessions, administrative_staff, classes, trainers, members CASCADE
    """)

        # Create the members table if it doesn't exist
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

        # Create the trainers table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trainers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

   

        # Create the training_sessions table if it doesn't exist
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

        # Create the classes table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id SERIAL PRIMARY KEY,
                class_name VARCHAR(255) NOT NULL,
                class_description TEXT
            )
        """)

        # Create the class_registrations table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS class_registrations (
                id SERIAL PRIMARY KEY,
                member_id INT NOT NULL,
                class_id INT NOT NULL,
                FOREIGN KEY (member_id) REFERENCES members(id),
                FOREIGN KEY (class_id) REFERENCES classes(id)
            )
        """)
        # STAFF
        # Create the administrative_staff table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS administrative_staff (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Create the room_bookings table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS room_bookings (
                id SERIAL PRIMARY KEY,
                room_number INT NOT NULL,
                booking_date DATE,
                booking_time TIME
            )
        """)


        # Create the equipment_maintenance table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment_maintenance (
                id SERIAL PRIMARY KEY,
                equipment_name VARCHAR(255) NOT NULL,
                last_maintenance_date DATE
            )
        """)

        # Create the payments table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                member_id INT NOT NULL,
                payment_amount DECIMAL(10, 2) NOT NULL,
                payment_date DATE,
                FOREIGN KEY (member_id) REFERENCES members(id)
            )
        """)


        #TRAINER


        # Create the trainer_schedule table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trainer_schedule (
                id SERIAL PRIMARY KEY,
                trainer_id INT NOT NULL,
                available_time TIME,
                FOREIGN KEY (trainer_id) REFERENCES trainers(id)
            )
        """)

        # Commit the changes and close the cursor and the database connection
        db_connection.commit()
        cursor.close()

    except psycopg2.Error as e:
        print("Error creating tables:", e)


def main():
    try:
        # Connect to the PostgreSQL database
        db_connection = psycopg2.connect(
            dbname="healthproject",
            user="postgres",
            password="tanayShah",
            host="localhost",
            port="5432"
        )

        create_tables(db_connection)
        # Create a cursor object using the connection
        cursor = db_connection.cursor()

        # Example usage for Member
        member = Member(db_connection, "Alice Smith", "alice.smith@example.com", "password789")
        member.fitness_goal = "Gain muscle"
        member.health_metrics = "Weight: 150 lbs, Height: 5'7\""
        member.register()
        member.update_profile(db_connection,'password', 'tanay')

        member2 = Member(db_connection, "arjun pathak", "arjun.pathak@example.com", "password789")
        member2.fitness_goal = "Gain muscle"
        member2.health_metrics = "Weight: 150 lbs, Height: 5'7\""
        member2.register()
        member2.update_profile(db_connection,'fitness_goal', 'Loose Fat')
        # member.register_for_class(class_id=1)

        # Example usage for Trainer
        
        trainer = Trainer(db_connection, "John Doe", "john.doe@example.com", "password123")
        trainer.register()
        trainer.manage_schedule(available_times=["09:00:00", "10:00:00", "11:00:00"])
        member2.schedule_training_session(trainer_id=1, session_date="2024-04-01", session_time="10:00:00")
        member.schedule_training_session(trainer_id=1, session_date="2024-04-01", session_time="10:00:00")
        # Example usage for AdministrativeStaff
        staff = AdministrativeStaff(db_connection, "Jane Smith", "jane.smith@example.com", "password456")
        staff.register()
        # staff.manage_room_booking(room_number=101, booking_date="2024-04-01", booking_time="09:00:00")
        # staff.monitor_equipment_maintenance(equipment_name="Treadmill", last_maintenance_date="2024-03-01")
        # staff.update_class_schedule(class_id=1, new_schedule="Monday, Wednesday, Friday 18:00-19:00")
        # staff.process_payment(member_id=1, amount=50.00, payment_date="2024-04-01")

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

    finally:
        # Close the cursor and the database connection
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

if __name__ == "__main__":
    main()
