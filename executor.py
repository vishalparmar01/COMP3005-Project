import psycopg2
from member import Member
from staff import AdministrativeStaff
from trainer import Trainer

# Function to create tables from DDL file
def create_tables_from_file(db_connection, ddl_file_path):
    try:
        # Create a cursor object using the connection
        cursor = db_connection.cursor()

        # Read the DDL file
        with open(ddl_file_path, 'r') as ddl_file:
            ddl_commands = ddl_file.read()

        # Execute the DDL commands
        cursor.execute(ddl_commands)

        # Commit the changes and close the cursor
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

        ddl_file_path = "tables.sql"
        # Create tables from the DDL file
        create_tables_from_file(db_connection, ddl_file_path)
        # Create a cursor object using the connection
        cursor = db_connection.cursor()

        # Example usage for Member
        Member.register(db_connection,"Alice Smith", "alice.smith@example.com", "password789","Gain muscle","Weight: 150 lbs, Height: 5'7\"")
        Member.update_profile(db_connection,"Alice Smith",'password','tanay')
        Member.register(db_connection,"Arjun Pathak", "arjun.pathak@example.com", "password789","Gain muscle", "Weight: 150 lbs, Height: 5'7\"")
        Member.update_profile(db_connection,"Arjun Pathak",'fitness_goal', 'Loose Fat')

        # Example usage for Trainer
        Trainer.register(db_connection,"John Doe", "john.doe@example.com", "password123")
        Trainer.manage_schedule(db_connection,"John Doe",available_times=["09:00:00", "10:00:00", "11:00:00"])
        Trainer.register(db_connection,"Tanay Shah", "tanay.shah@example.com", "tanayshah")
        Trainer.manage_schedule(db_connection,"Tanay Shah",available_times=["10:00:00", "11:00:00", "13:00:00"])
        trainers=Trainer.get_available_trainers(db_connection, session_date="2024-04-01",session_time="15:00:00")
        for trainer in trainers:
            print(trainer.name)

        Member.schedule_training_session(db_connection,"Arjun Pathak","Tanay Shah",session_date="2024-04-01",session_time="10:00:00")
        Member.schedule_training_session(db_connection,"Alice Smith","Tanay Shah",session_date="2024-04-01",session_time="10:00:00")
        
        # Test the search_member_profile_by_name method
        member_profile = Trainer.search_member_profile_by_name(db_connection,"Alice Smith")

        if member_profile:
            print("Member profile found:")
            print("Name:", member_profile[1])
            print("Email:", member_profile[2])

        member_profile = Trainer.search_member_profile_by_name(db_connection,"Arjun Pathak")

        if member_profile:
            print("Member profile found:")
            print("Name:", member_profile[1])
            print("Email:", member_profile[2])

        # Example usage for AdministrativeStaff
        # staff = AdministrativeStaff(db_connection, "Jane Smith", "jane.smith@example.com", "password456")
        # staff.register()
        # # staff.manage_room_booking(room_number=101, booking_date="2024-04-01", booking_time="09:00:00")
        # staff.monitor_equipment_maintenance(equipment_name="Treadmill", last_maintenance_date="2024-03-01")
        # # staff.update_class_schedule(class_id=1, new_schedule="Monday, Wednesday, Friday 18:00-19:00")
        # staff.process_payment(member_id=3, amount=50.00, payment_date="2024-04-01")

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
