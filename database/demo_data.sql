-- Demo data for video: 5 guests, all arriving 2026-10-02, covering every room type
-- Safe to re-run: INSERT IGNORE style via NOT EXISTS checks
USE hotel_management;

-- 5 guests (unique mobiles, skip if already loaded)
INSERT INTO Guest (First_Name, Last_Name, DOB, Gender, Mob_No)
SELECT * FROM (SELECT 'Ishaan' AS f, 'Kapoor' AS l, DATE '1994-05-12' AS d, 'Male' AS g, '9810010001' AS m) t
WHERE NOT EXISTS (SELECT 1 FROM Guest WHERE Mob_No='9810010001');
INSERT INTO Guest (First_Name, Last_Name, DOB, Gender, Mob_No)
SELECT * FROM (SELECT 'Meera' AS f, 'Iyer' AS l, DATE '1996-08-20' AS d, 'Female' AS g, '9810010002' AS m) t
WHERE NOT EXISTS (SELECT 1 FROM Guest WHERE Mob_No='9810010002');
INSERT INTO Guest (First_Name, Last_Name, DOB, Gender, Mob_No)
SELECT * FROM (SELECT 'Kabir' AS f, 'Malhotra' AS l, DATE '1992-02-10' AS d, 'Male' AS g, '9810010003' AS m) t
WHERE NOT EXISTS (SELECT 1 FROM Guest WHERE Mob_No='9810010003');
INSERT INTO Guest (First_Name, Last_Name, DOB, Gender, Mob_No)
SELECT * FROM (SELECT 'Divya' AS f, 'Nair' AS l, DATE '1999-12-01' AS d, 'Female' AS g, '9810010004' AS m) t
WHERE NOT EXISTS (SELECT 1 FROM Guest WHERE Mob_No='9810010004');
INSERT INTO Guest (First_Name, Last_Name, DOB, Gender, Mob_No)
SELECT * FROM (SELECT 'Arjun' AS f, 'Reddy' AS l, DATE '1990-06-25' AS d, 'Male' AS g, '9810010005' AS m) t
WHERE NOT EXISTS (SELECT 1 FROM Guest WHERE Mob_No='9810010005');

-- 5 bookings, all arriving 2026-10-02 (skip if already loaded)
INSERT INTO Booking_Record (G_ID, R_ID, Booking_Type, Status, Check_In, Check_Out)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010001'), 4, 'Online', 'Confirmed', '2026-10-02', '2026-10-05'
WHERE NOT EXISTS (SELECT 1 FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010001') AND Check_In='2026-10-02');
INSERT INTO Booking_Record (G_ID, R_ID, Booking_Type, Status, Check_In, Check_Out)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010002'), 9, 'Walk-in', 'Confirmed', '2026-10-02', '2026-10-05'
WHERE NOT EXISTS (SELECT 1 FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010002') AND Check_In='2026-10-02');
INSERT INTO Booking_Record (G_ID, R_ID, Booking_Type, Status, Check_In, Check_Out)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010003'), 17, 'Online', 'Confirmed', '2026-10-02', '2026-10-06'
WHERE NOT EXISTS (SELECT 1 FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010003') AND Check_In='2026-10-02');
INSERT INTO Booking_Record (G_ID, R_ID, Booking_Type, Status, Check_In, Check_Out)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010004'), 20, 'Phone', 'Confirmed', '2026-10-02', '2026-10-04'
WHERE NOT EXISTS (SELECT 1 FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010004') AND Check_In='2026-10-02');
INSERT INTO Booking_Record (G_ID, R_ID, Booking_Type, Status, Check_In, Check_Out)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010005'), 24, 'Agent', 'Confirmed', '2026-10-02', '2026-10-05'
WHERE NOT EXISTS (SELECT 1 FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010005') AND Check_In='2026-10-02');

-- 5 bills, one per demo booking (3 nights x price)
INSERT INTO Bill (G_ID, Amount, Billing_Date, Payment_Status, Booking_ID)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010001'), 4500.00, '2026-10-02', 'Unpaid',
       (SELECT Booking_ID FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010001') AND Check_In='2026-10-02' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM Bill WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010001') AND Billing_Date='2026-10-02');
INSERT INTO Bill (G_ID, Amount, Billing_Date, Payment_Status, Booking_ID)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010002'), 7500.00, '2026-10-02', 'Unpaid',
       (SELECT Booking_ID FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010002') AND Check_In='2026-10-02' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM Bill WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010002') AND Billing_Date='2026-10-02');
INSERT INTO Bill (G_ID, Amount, Billing_Date, Payment_Status, Booking_ID)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010003'), 16000.00, '2026-10-02', 'Unpaid',
       (SELECT Booking_ID FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010003') AND Check_In='2026-10-02' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM Bill WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010003') AND Billing_Date='2026-10-02');
INSERT INTO Bill (G_ID, Amount, Billing_Date, Payment_Status, Booking_ID)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010004'), 8000.00, '2026-10-02', 'Paid',
       (SELECT Booking_ID FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010004') AND Check_In='2026-10-02' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM Bill WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010004') AND Billing_Date='2026-10-02');
INSERT INTO Bill (G_ID, Amount, Billing_Date, Payment_Status, Booking_ID)
SELECT (SELECT G_ID FROM Guest WHERE Mob_No='9810010005'), 21000.00, '2026-10-02', 'Unpaid',
       (SELECT Booking_ID FROM Booking_Record WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010005') AND Check_In='2026-10-02' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM Bill WHERE G_ID=(SELECT G_ID FROM Guest WHERE Mob_No='9810010005') AND Billing_Date='2026-10-02');

-- 2 log records (brings Records to 5)
INSERT INTO Records (Log_Details)
SELECT 'Demo group of 5 checked in on 2026-10-02 (Ishaan, Meera, Kabir, Divya, Arjun)'
WHERE NOT EXISTS (SELECT 1 FROM Records WHERE Log_Details LIKE 'Demo group of 5%');
INSERT INTO Records (Log_Details)
SELECT 'Bills generated for demo arrivals 2026-10-02 by Receptionist Pranav'
WHERE NOT EXISTS (SELECT 1 FROM Records WHERE Log_Details LIKE 'Bills generated for demo%');
