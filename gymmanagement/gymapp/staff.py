class AdministrativeStaff:
    @classmethod
    def register(cls, db_connection, name, email, password):
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO administrative_staff (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password),
        )
        cursor.execute("SELECT LASTVAL()")
        staff_id = cursor.fetchone()[0]
        db_connection.commit()
        cursor.close()
        return staff_id

    @classmethod
    def get_staff_by_name(cls, db_connection, name):
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM administrative_staff WHERE name = %s", (name,))
        staff_data = cursor.fetchone()
        cursor.close()
        if staff_data:
            return cls(db_connection, staff_data[1], staff_data[2], staff_data[3])
        return None

    @classmethod
    def manage_room_booking(cls, db_connection, booking_date, booking_time):
        cursor = db_connection.cursor()

        # Get all distinct room numbers
        cursor.execute("SELECT DISTINCT room_number FROM room_bookings")
        all_rooms = [row[0] for row in cursor.fetchall()]

        # Check for booked rooms at the given date and time
        cursor.execute(
            "SELECT DISTINCT room_number FROM room_bookings WHERE booking_date = %s AND booking_time = %s",
            (booking_date, booking_time),
        )
        booked_rooms = [row[0] for row in cursor.fetchall()]

        # Find available rooms
        available_rooms = [room for room in all_rooms if room not in booked_rooms]

        if not available_rooms:
            print(f"No available rooms on {booking_date} at {booking_time}")
            return None

        # Book the first available room
        room_number = available_rooms[0]
        cursor.execute(
            "INSERT INTO room_bookings (room_number, booking_date, booking_time) VALUES (%s, %s, %s)",
            (room_number, booking_date, booking_time),
        )
        db_connection.commit()
        cursor.close()

        print(f"Room {room_number} booked on {booking_date} at {booking_time}")
        return room_number

    @classmethod
    def monitor_equipment_maintenance(
        cls, db_connection, equipment_name, last_maintenance_date, frequency=None
    ):
        cursor = db_connection.cursor()
        # Check if equipment exists in the table
        cursor.execute(
            "SELECT * FROM equipment_maintenance WHERE equipment_name = %s",
            (equipment_name,),
        )
        existing_equipment = cursor.fetchone()
        if existing_equipment:
            # Update the last maintenance date
            cursor.execute(
                "UPDATE equipment_maintenance SET last_maintenance_date = %s WHERE equipment_name = %s",
                (last_maintenance_date, equipment_name),
            )
        else:
            # Insert new equipment with last maintenance date
            cursor.execute(
                "INSERT INTO equipment_maintenance (equipment_name, last_maintenance_date, maintenance_frequency) VALUES (%s, %s, %s)",
                (equipment_name, last_maintenance_date, frequency),
            )
        db_connection.commit()
        cursor.close()

    @classmethod
    def update_class_schedule(
        cls, db_connection, class_name, description, start_time, end_time, recurrence
    ):
        cursor = db_connection.cursor()
        # Check if the class exists, and insert it if it doesn't
        cursor.execute("SELECT id FROM classes WHERE class_name = %s", (class_name,))
        class_data = cursor.fetchone()
        if not class_data:
            cursor.execute(
                "INSERT INTO classes (class_name, class_description, start_time, end_time, recurrence) VALUES (%s, %s, %s, %s, %s)",
                (class_name, description, start_time, end_time, recurrence),
            )
            db_connection.commit()
            cursor.close()
            return

        class_id = class_data[0]
        cursor.execute(
            "UPDATE classes SET start_time = %s, end_time = %s, recurrence = %s WHERE id = %s",
            (start_time, end_time, recurrence, class_id),
        )
        db_connection.commit()
        cursor.close()

    @classmethod
    def process_payment(cls, db_connection, member_name, amount, payment_date):
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM members WHERE name = %s", (member_name,))
        member_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO payments (member_id, payment_amount, payment_date) VALUES (%s, %s, %s)",
            (member_id, amount, payment_date),
        )
        db_connection.commit()
        cursor.close()
