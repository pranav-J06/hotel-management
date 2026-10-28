-- ============================================================================
-- Hotel Management System - MySQL Database (BCNF Compliant)
-- Schema based on Final Relational Schema provided
-- Primary Keys are auto-increment INT where applicable
-- Foreign Keys enforce referential integrity with CASCADE / SET NULL
-- ============================================================================

DROP DATABASE IF EXISTS hotel_management;
CREATE DATABASE hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hotel_management;

SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------------------------
-- 1. ZipCode (Pin-no, City, State)
-- Original: ZipCode(Pin-no, City, State)
-- ----------------------------------------------------------------------------
CREATE TABLE ZipCode (
    Pin_no VARCHAR(10) PRIMARY KEY,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 2. Guest (G-ID, First_Name, Last_Name, DOB, Gender, Mob-No)
-- Original: Guest(G-ID, First_Name, Last_Name, DOB, Gender, Mob-No)
-- ----------------------------------------------------------------------------
CREATE TABLE Guest (
    G_ID INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    DOB DATE,
    Gender ENUM('Male','Female','Other'),
    Mob_No VARCHAR(15) NOT NULL UNIQUE,
    CONSTRAINT chk_guest_mob CHECK (Mob_No REGEXP '^[0-9]{10,15}$')
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 3. Employee (E-ID, First_Name, Last_Name, Salary, Sex, Mob-No, Pin-no)
-- Original: Employee(E-ID, First_Name, Last_Name, Salary, Sex, Mob-No, Pin-no)
-- FK: Pin-no -> ZipCode(Pin-no)
-- ----------------------------------------------------------------------------
CREATE TABLE Employee (
    E_ID INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Salary DECIMAL(10,2) NOT NULL,
    Sex ENUM('Male','Female','Other'),
    Mob_No VARCHAR(15) NOT NULL UNIQUE,
    Pin_no VARCHAR(10),
    CONSTRAINT chk_salary CHECK (Salary > 0),
    CONSTRAINT fk_employee_zipcode FOREIGN KEY (Pin_no) REFERENCES ZipCode(Pin_no)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 4. Room (R-ID, Type, Capacity, Availability)
-- Original: Room(R-ID, Type, Capacity, Availability)
-- ----------------------------------------------------------------------------
CREATE TABLE Room (
    R_ID INT AUTO_INCREMENT PRIMARY KEY,
    Type VARCHAR(30) NOT NULL COMMENT 'Single, Double, Deluxe, Suite, etc.',
    Capacity INT NOT NULL,
    Availability ENUM('Available','Occupied','Maintenance') NOT NULL DEFAULT 'Available',
    Price_Per_Night DECIMAL(10,2) NOT NULL DEFAULT 1000.00,
    CONSTRAINT chk_capacity CHECK (Capacity > 0),
    CONSTRAINT chk_price CHECK (Price_Per_Night >= 0)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 5. Manager (E-ID, Department, Qualification)
-- Original: Manager(E-ID, Department, Qualification)
-- FK: E-ID -> Employee(E-ID)
-- ----------------------------------------------------------------------------
CREATE TABLE Manager (
    E_ID INT PRIMARY KEY,
    Department VARCHAR(50) NOT NULL,
    Qualification VARCHAR(100),
    CONSTRAINT fk_manager_employee FOREIGN KEY (E_ID) REFERENCES Employee(E_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 6. Housekeeper (E-ID)
-- Original: Housekeeper(E-ID)
-- FK: E-ID -> Employee(E-ID)
-- ----------------------------------------------------------------------------
CREATE TABLE Housekeeper (
    E_ID INT PRIMARY KEY,
    CONSTRAINT fk_housekeeper_employee FOREIGN KEY (E_ID) REFERENCES Employee(E_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 7. Receptionist (E-ID)
-- Original: Receptionist(E-ID)
-- FK: E-ID -> Employee(E-ID)
-- ----------------------------------------------------------------------------
CREATE TABLE Receptionist (
    E_ID INT PRIMARY KEY,
    CONSTRAINT fk_receptionist_employee FOREIGN KEY (E_ID) REFERENCES Employee(E_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 8. Booking_Record (Booking-ID, G-ID, R-ID, Booking_Type, Status)
-- Original: Booking_Record(Booking-ID, G-ID, R-ID, Booking_Type, Status)
-- FK: G-ID -> Guest, R-ID -> Room
-- ----------------------------------------------------------------------------
CREATE TABLE Booking_Record (
    Booking_ID INT AUTO_INCREMENT PRIMARY KEY,
    G_ID INT NOT NULL,
    R_ID INT NOT NULL,
    Booking_Type ENUM('Online','Walk-in','Phone','Agent') NOT NULL DEFAULT 'Walk-in',
    Status ENUM('Confirmed','Checked-in','Checked-out','Cancelled','Pending') NOT NULL DEFAULT 'Confirmed',
    Check_In DATE NOT NULL,
    Check_Out DATE NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_booking_guest FOREIGN KEY (G_ID) REFERENCES Guest(G_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_booking_room FOREIGN KEY (R_ID) REFERENCES Room(R_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT chk_dates CHECK (Check_Out > Check_In)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 9. Bill (B-ID, G-ID, Amount)
-- Original: Bill(B-ID, G-ID, Amount)
-- FK: G-ID -> Guest
-- ----------------------------------------------------------------------------
CREATE TABLE Bill (
    B_ID INT AUTO_INCREMENT PRIMARY KEY,
    G_ID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Billing_Date DATE NOT NULL DEFAULT (CURDATE()),
    Payment_Status ENUM('Paid','Unpaid','Partial') NOT NULL DEFAULT 'Unpaid',
    Booking_ID INT NULL,
    CONSTRAINT fk_bill_guest FOREIGN KEY (G_ID) REFERENCES Guest(G_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_bill_booking FOREIGN KEY (Booking_ID) REFERENCES Booking_Record(Booking_ID)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT chk_amount CHECK (Amount >= 0)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 10. Records (Record-no, Log_Details)
-- Original: Records(Record-no, Log_Details)
-- ----------------------------------------------------------------------------
CREATE TABLE Records (
    Record_no INT AUTO_INCREMENT PRIMARY KEY,
    Log_Details TEXT NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 11. Housekeeper_Room (E-ID, R-ID)
-- Original: Housekeeper_Room(E-ID, R-ID)
-- FK: E-ID -> Housekeeper, R-ID -> Room
-- ----------------------------------------------------------------------------
CREATE TABLE Housekeeper_Room (
    E_ID INT NOT NULL,
    R_ID INT NOT NULL,
    Assigned_Date DATE NOT NULL DEFAULT (CURDATE()),
    PRIMARY KEY (E_ID, R_ID),
    CONSTRAINT fk_hkroom_housekeeper FOREIGN KEY (E_ID) REFERENCES Housekeeper(E_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_hkroom_room FOREIGN KEY (R_ID) REFERENCES Room(R_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 12. Guest_Manager (G-ID, E-ID)
-- Original: Guest_Manager(G-ID, E-ID)
-- FK: G-ID -> Guest, E-ID -> Manager
-- ----------------------------------------------------------------------------
CREATE TABLE Guest_Manager (
    G_ID INT NOT NULL,
    E_ID INT NOT NULL,
    PRIMARY KEY (G_ID, E_ID),
    CONSTRAINT fk_gm_guest FOREIGN KEY (G_ID) REFERENCES Guest(G_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_gm_manager FOREIGN KEY (E_ID) REFERENCES Manager(E_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 13. Receptionist_Records (E-ID, Record-no)
-- Original: Receptionist_Records(E-ID, Record-no)
-- FK: E-ID -> Receptionist, Record-no -> Records
-- ----------------------------------------------------------------------------
CREATE TABLE Receptionist_Records (
    E_ID INT NOT NULL,
    Record_no INT NOT NULL,
    PRIMARY KEY (E_ID, Record_no),
    CONSTRAINT fk_rr_receptionist FOREIGN KEY (E_ID) REFERENCES Receptionist(E_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_rr_records FOREIGN KEY (Record_no) REFERENCES Records(Record_no)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------------------------------------------------------
-- Indexes for performance (beyond PK/FK)
-- ----------------------------------------------------------------------------
CREATE INDEX idx_guest_name ON Guest(First_Name, Last_Name);
CREATE INDEX idx_employee_name ON Employee(First_Name, Last_Name);
CREATE INDEX idx_room_type_avail ON Room(Type, Availability);
CREATE INDEX idx_booking_gid ON Booking_Record(G_ID);
CREATE INDEX idx_booking_rid ON Booking_Record(R_ID);
CREATE INDEX idx_booking_status ON Booking_Record(Status);
CREATE INDEX idx_bill_gid ON Bill(G_ID);

-- ----------------------------------------------------------------------------
-- Views (helpful for JOINs)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_booking_details AS
SELECT 
    b.Booking_ID, b.Booking_Type, b.Status, b.Check_In, b.Check_Out,
    g.G_ID, CONCAT(g.First_Name,' ',g.Last_Name) AS Guest_Name, g.Mob_No AS Guest_Phone,
    r.R_ID, r.Type AS Room_Type, r.Capacity, r.Price_Per_Night
FROM Booking_Record b
JOIN Guest g ON b.G_ID = g.G_ID
JOIN Room r ON b.R_ID = r.R_ID;

CREATE OR REPLACE VIEW vw_employee_details AS
SELECT 
    e.E_ID, CONCAT(e.First_Name,' ',e.Last_Name) AS Full_Name, e.Salary, e.Sex, e.Mob_No,
    z.Pin_no, z.City, z.State,
    CASE 
        WHEN m.E_ID IS NOT NULL THEN 'Manager'
        WHEN h.E_ID IS NOT NULL THEN 'Housekeeper'
        WHEN r.E_ID IS NOT NULL THEN 'Receptionist'
        ELSE 'Staff'
    END AS Role
FROM Employee e
LEFT JOIN ZipCode z ON e.Pin_no = z.Pin_no
LEFT JOIN Manager m ON e.E_ID = m.E_ID
LEFT JOIN Housekeeper h ON e.E_ID = h.E_ID
LEFT JOIN Receptionist r ON e.E_ID = r.E_ID;

-- ============================================================================
-- End of Schema
-- Verify with: SHOW TABLES; DESCRIBE Guest; etc.
-- ============================================================================
