import psycopg2
from member import Member
from staff import AdministrativeStaff
from trainer import Trainer

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
        Member.create_table(db_connection)
        Trainer.create_table(db_connection)
        AdministrativeStaff.create_table(db_connection)
        # Create a cursor object using the connection
        cursor = db_connection.cursor()

        # Example usage for Member
        member = Member(db_connection, "Alice Smith", "alice.smith@example.com", "password789")
        member.fitness_goal = "Gain muscle"
        member.health_metrics = "Weight: 150 lbs, Height: 5'7\""
        member.register()
        member.schedule_training_session(trainer_id=1, session_date="2024-04-01", session_time="09:00:00")
        member.register_for_class(class_id=1)

        # Example usage for Trainer
        
        trainer = Trainer(db_connection, "John Doe", "john.doe@example.com", "password123")
        trainer.register()
        trainer.manage_schedule(available_times=["09:00:00", "10:00:00", "11:00:00"])

        # Example usage for AdministrativeStaff
        staff = AdministrativeStaff(db_connection, "Jane Smith", "jane.smith@example.com", "password456")
        staff.register()
        staff.manage_room_booking(room_number=101, booking_date="2024-04-01", booking_time="09:00:00")
        staff.monitor_equipment_maintenance(equipment_name="Treadmill", last_maintenance_date="2024-03-01")
        staff.update_class_schedule(class_id=1, new_schedule="Monday, Wednesday, Friday 18:00-19:00")
        staff.process_payment(member_id=1, amount=50.00, payment_date="2024-04-01")

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
