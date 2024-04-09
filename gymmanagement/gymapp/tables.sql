-- DDL file for creating tables
DROP TABLE IF EXISTS health_metrics, payments, equipment_maintenance, room_bookings, trainer_schedule, class_registrations, training_sessions, administrative_staff, classes, trainers, members CASCADE;

-- Create the members table
CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    fitness_goal VARCHAR(255)
);

-- Create the trainers table
CREATE TABLE IF NOT EXISTS trainers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create the training_sessions table
CREATE TABLE IF NOT EXISTS training_sessions (
    id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    trainer_id INT NOT NULL,
    session_date DATE,
    session_time TIME,
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (trainer_id) REFERENCES trainers(id)
);

-- Create the classes table
CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    class_description TEXT,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    recurrence VARCHAR(255) NOT NULL -- For example, "everyday", "weekdays", etc.
);

-- Create the class_registrations table
CREATE TABLE IF NOT EXISTS class_registrations (
    id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    class_id INT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

-- Create the administrative_staff table
CREATE TABLE IF NOT EXISTS administrative_staff (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create the room_bookings table
CREATE TABLE IF NOT EXISTS room_bookings (
    id SERIAL PRIMARY KEY,
    room_number INT NOT NULL,
    booking_date DATE,
    booking_time TIME,
    FOREIGN KEY (member_id) REFERENCES members(id)
);

CREATE TABLE IF NOT EXISTS equipment_maintenance (
    id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(255) NOT NULL,
    last_maintenance_date DATE,
    maintenance_frequency VARCHAR(255),
    FOREIGN KEY (staff_id) REFERENCES administrative_staff(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    payment_amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE,
    FOREIGN KEY (member_id) REFERENCES members(id)
);

CREATE TABLE IF NOT EXISTS trainer_schedule (
    id SERIAL PRIMARY KEY,
    trainer_id INT NOT NULL,
    available_time TIME,
    FOREIGN KEY (trainer_id) REFERENCES trainers(id)
);

CREATE TABLE IF NOT EXISTS health_metrics (
    id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    FOREIGN KEY (member_id) REFERENCES members(id)
);