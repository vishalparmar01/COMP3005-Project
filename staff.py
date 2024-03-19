class AdministrativeStaff:
    def __init__(self, db_connection, name, email, password):
        self.db_connection = db_connection
        self.name = name
        self.email = email
        self.password = password
        self.id = None

    @staticmethod
    def create_table(db_connection):
                # Create the administrative_staff table if it doesn't exist
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS administrative_staff (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        db_connection.commit()
        cursor.close()

        # Create the room_bookings table if it doesn't exist
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS room_bookings (
                id SERIAL PRIMARY KEY,
                room_number INT NOT NULL,
                booking_date DATE,
                booking_time TIME
            )
        """)
        db_connection.commit()
        cursor.close()

        # Create the equipment_maintenance table if it doesn't exist
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment_maintenance (
                id SERIAL PRIMARY KEY,
                equipment_name VARCHAR(255) NOT NULL,
                last_maintenance_date DATE
            )
        """)
        db_connection.commit()
        cursor.close()

        # Create the payments table if it doesn't exist
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                member_id INT NOT NULL,
                payment_amount DECIMAL(10, 2) NOT NULL,
                payment_date DATE,
                FOREIGN KEY (member_id) REFERENCES members(id)
            )
        """)
        db_connection.commit()
        cursor.close()

    def register(self):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO administrative_staff (name, email, password) VALUES (%s, %s, %s)", (self.name, self.email, self.password))
        self.db_connection.commit()
        self.id = cursor.lastrowid
        cursor.close()

    @staticmethod
    def get_staff_by_email(db_connection, email):
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM administrative_staff WHERE email = %s", (email,))
        staff_data = cursor.fetchone()
        cursor.close()
        if staff_data:
            return AdministrativeStaff(db_connection, staff_data[1], staff_data[2], staff_data[3])
        return None
    
    def manage_room_booking(self, room_number, booking_date, booking_time):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO room_bookings (room_number, booking_date, booking_time) VALUES (%s, %s, %s)", (room_number, booking_date, booking_time))
        self.db_connection.commit()
        cursor.close()

    def monitor_equipment_maintenance(self, equipment_name, last_maintenance_date):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO equipment_maintenance (equipment_name, last_maintenance_date) VALUES (%s, %s)", (equipment_name, last_maintenance_date))
        self.db_connection.commit()
        cursor.close()

    def update_class_schedule(self, class_id, new_schedule):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE classes SET class_schedule = %s WHERE id = %s", (new_schedule, class_id))
        self.db_connection.commit()
        cursor.close()

    def process_payment(self, member_id, amount, payment_date):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO payments (member_id, payment_amount, payment_date) VALUES (%s, %s, %s)", (member_id, amount, payment_date))
        self.db_connection.commit()
        cursor.close()
