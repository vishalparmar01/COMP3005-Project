-- Insert data into the members table
INSERT INTO members (name, email, password, fitness_goal) VALUES
('Rahul Cheruku', 'rahulch@example.com', 'password123', 'Lose weight'),
('Bob Johnson', 'bob@example.com', 'securepw', 'Gain muscle');

-- Insert data into the trainers table
INSERT INTO trainers (name, email, password) VALUES
('John Doe', 'john@example.com', 'trainerpass'),
('Sarah Lee', 'sarah@example.com', 'sarahpass');

-- Insert data into the training_sessions table
INSERT INTO training_sessions (member_id, trainer_id, session_date, session_time) VALUES
(1, 1, '2024-04-01', '10:00:00'),
(2, 2, '2024-04-01', '11:00:00');

-- Insert data into the trainer_schedule table
INSERT INTO trainer_schedule (trainer_id, available_time) VALUES
(1, '10:00:00'),
(1, '11:00:00'),
(2, '11:00:00'),
(2, '12:00:00');

-- Insert data into the classes table
INSERT INTO classes (class_name, class_description, start_time, end_time, recurrence) VALUES
('Yoga', 'Relaxing yoga session', '13:00:00', '15:00:00', 'everyday'),
('Zumba', 'High-energy dance workout', '16:00:00', '18:00:00', 'weekdays');

-- Insert data into the administrative_staff table
INSERT INTO administrative_staff (name, email, password) VALUES
('Admin1', 'admin1@example.com', 'adminpass1'),
('Admin2', 'admin2@example.com', 'adminpass2');

-- Insert data into the room_bookings table
INSERT INTO room_bookings (room_number, booking_date, booking_time) VALUES
(101, '2024-04-01', '10:00:00'),
(102, '2024-04-01', NULL),
(103, '2024-04-01', NULL),
(104, '2024-04-01', NULL);

-- Inserting data into equipment_maintenance table
INSERT INTO equipment_maintenance (equipment_name, last_maintenance_date, maintenance_frequency) VALUES
    ('Treadmill', '2023-01-01', '6 months'),
    ('Elliptical Machine', '2023-02-15', '8 months'),
    ('Stationary Bike', '2023-03-20', '12 months');