-- ============================================================================
-- Hotel Management System - Sample Seed Data
-- Run after schema.sql :  mysql -u root -p hotel_management < seed.sql
-- or: SOURCE database/schema.sql; SOURCE database/seed.sql;
-- ============================================================================
USE hotel_management;

-- ----------------------------------------------------------------------------
-- ZipCode
-- ----------------------------------------------------------------------------
INSERT INTO ZipCode (Pin_no, City, State) VALUES
('400001', 'Mumbai', 'Maharashtra'),
('110001', 'New Delhi', 'Delhi'),
('560001', 'Bengaluru', 'Karnataka'),
('600001', 'Chennai', 'Tamil Nadu'),
('700001', 'Kolkata', 'West Bengal'),
('380001', 'Ahmedabad', 'Gujarat');

-- ----------------------------------------------------------------------------
-- Guest
-- ----------------------------------------------------------------------------
INSERT INTO Guest (First_Name, Last_Name, DOB, Gender, Mob_No) VALUES
('Aarav', 'Sharma', '1995-03-15', 'Male', '9876543210'),
('Priya', 'Patel', '1998-07-22', 'Female', '9876543211'),
('Rohan', 'Verma', '1990-11-05', 'Male', '9876543212'),
('Ananya', 'Singh', '1997-01-30', 'Female', '9876543213'),
('Vikram', 'Mehta', '1988-09-18', 'Male', '9876543214');

-- ----------------------------------------------------------------------------
-- Employee
-- ----------------------------------------------------------------------------
INSERT INTO Employee (First_Name, Last_Name, Salary, Sex, Mob_No, Pin_no) VALUES
('Rajesh', 'Kumar', 75000.00, 'Male', '9000000001', '400001'),   -- E_ID 1 -> Manager
('Sunita', 'Desai', 45000.00, 'Female', '9000000002', '110001'), -- E_ID 2 -> Manager
('Amit', 'Joshi', 25000.00, 'Male', '9000000003', '560001'),     -- E_ID 3 -> Housekeeper
('Kavita', 'Rao', 24000.00, 'Female', '9000000004', '600001'),   -- E_ID 4 -> Housekeeper
('Suresh', 'Nair', 30000.00, 'Male', '9000000005', '700001'),    -- E_ID 5 -> Receptionist
('Neha', 'Gupta', 32000.00, 'Female', '9000000006', '380001'),   -- E_ID 6 -> Receptionist
('Manoj', 'Tiwari', 28000.00, 'Male', '9000000007', '400001');   -- E_ID 7 -> Receptionist

-- ----------------------------------------------------------------------------
-- Room
-- ----------------------------------------------------------------------------
INSERT INTO Room (Type, Capacity, Availability, Price_Per_Night) VALUES
-- Single (8 rooms: 6 Available, 1 Occupied, 1 Maintenance)
('Single', 1, 'Available', 1500.00),
('Single', 1, 'Occupied', 1500.00),
('Single', 1, 'Available', 1500.00),
('Single', 1, 'Available', 1500.00),
('Single', 1, 'Available', 1600.00),
('Single', 1, 'Available', 1600.00),
('Single', 1, 'Maintenance', 1500.00),
('Single', 1, 'Available', 1500.00),
-- Double (8 rooms: 6 Available, 2 Occupied)
('Double', 2, 'Available', 2500.00),
('Double', 2, 'Available', 2500.00),
('Double', 2, 'Available', 2600.00),
('Double', 2, 'Available', 2600.00),
('Double', 2, 'Occupied', 2500.00),
('Double', 2, 'Available', 2500.00),
('Double', 2, 'Available', 2700.00),
('Double', 2, 'Occupied', 2500.00),
-- Deluxe (6 rooms: 4 Available, 1 Occupied, 1 Maintenance)
('Deluxe', 3, 'Available', 4000.00),
('Deluxe', 3, 'Available', 4200.00),
('Deluxe', 2, 'Occupied', 4000.00),
('Deluxe', 3, 'Available', 4000.00),
('Deluxe', 3, 'Maintenance', 4000.00),
('Deluxe', 2, 'Available', 3800.00),
-- Suite (6 rooms: 4 Available, 1 Occupied, 1 Maintenance)
('Suite', 4, 'Maintenance', 7000.00),
('Suite', 4, 'Available', 7000.00),
('Suite', 4, 'Available', 7500.00),
('Suite', 4, 'Available', 7000.00),
('Suite', 4, 'Occupied', 7200.00),
('Suite', 5, 'Available', 8000.00);

-- ----------------------------------------------------------------------------
-- Manager (subset of Employee)
-- ----------------------------------------------------------------------------
INSERT INTO Manager (E_ID, Department, Qualification) VALUES
(1, 'Operations', 'MBA Hotel Management'),
(2, 'Front Office', 'MBA Hospitality');

-- ----------------------------------------------------------------------------
-- Housekeeper
-- ----------------------------------------------------------------------------
INSERT INTO Housekeeper (E_ID) VALUES (3), (4);

-- ----------------------------------------------------------------------------
-- Receptionist
-- ----------------------------------------------------------------------------
INSERT INTO Receptionist (E_ID) VALUES (5), (6), (7);

-- ----------------------------------------------------------------------------
-- Records (system logs)
-- ----------------------------------------------------------------------------
INSERT INTO Records (Log_Details) VALUES
('Guest Aarav Sharma checked in to Room 2 on 2026-09-01'),
('Room 6 marked under maintenance on 2026-09-02'),
('Monthly audit completed by Manager Rajesh Kumar');

-- ----------------------------------------------------------------------------
-- Booking_Record
-- ----------------------------------------------------------------------------
INSERT INTO Booking_Record (G_ID, R_ID, Booking_Type, Status, Check_In, Check_Out) VALUES
(1, 2, 'Online', 'Checked-in', '2026-09-01', '2026-09-05'),
(2, 3, 'Walk-in', 'Confirmed', '2026-09-06', '2026-09-08'),
(3, 8, 'Phone', 'Checked-in', '2026-09-02', '2026-09-06'),
(4, 1, 'Online', 'Pending', '2026-09-10', '2026-09-12'),
(5, 5, 'Agent', 'Confirmed', '2026-09-15', '2026-09-18');

-- ----------------------------------------------------------------------------
-- Bill
-- ----------------------------------------------------------------------------
INSERT INTO Bill (G_ID, Amount, Billing_Date, Payment_Status, Booking_ID) VALUES
(1, 6000.00, '2026-09-05', 'Unpaid', 1),
(3, 16000.00, '2026-09-06', 'Paid', 3),
(2, 5000.00, '2026-09-08', 'Unpaid', 2),
(5, 12000.00, '2026-09-18', 'Unpaid', 5);

-- ----------------------------------------------------------------------------
-- Housekeeper_Room (assignment)
-- ----------------------------------------------------------------------------
INSERT INTO Housekeeper_Room (E_ID, R_ID, Assigned_Date) VALUES
(3, 1, '2026-09-01'),
(3, 2, '2026-09-01'),
(3, 3, '2026-09-01'),
(4, 5, '2026-09-01'),
(4, 6, '2026-09-02'),
(4, 7, '2026-09-01');

-- ----------------------------------------------------------------------------
-- Guest_Manager (VIP / assigned manager)
-- ----------------------------------------------------------------------------
INSERT INTO Guest_Manager (G_ID, E_ID) VALUES
(1, 1),
(2, 2),
(5, 1);

-- ----------------------------------------------------------------------------
-- Receptionist_Records (who logged what)
-- ----------------------------------------------------------------------------
INSERT INTO Receptionist_Records (E_ID, Record_no) VALUES
(5, 1),
(6, 2),
(7, 3);

-- ----------------------------------------------------------------------------
-- Verification queries (optional)
-- ----------------------------------------------------------------------------
-- SELECT * FROM vw_booking_details;
-- SELECT * FROM vw_employee_details;
-- SELECT Type, COUNT(*) FROM Room GROUP BY Type;
