# Hotel Management System - Database

BCNF compliant schema with 13 tables as per spec.

## Files
- `schema.sql` - Complete DDL (CREATE DATABASE + 13 TABLES + FK + Views + Indexes)
- `seed.sql` - Sample data for testing

## Schema Summary
| # | Table | PK | FK |
|---|-------|----|----|
|1| ZipCode | Pin_no | - |
|2| Guest | G_ID | - |
|3| Employee | E_ID | Pin_no -> ZipCode |
|4| Room | R_ID | - |
|5| Manager | E_ID | E_ID -> Employee |
|6| Housekeeper | E_ID | E_ID -> Employee |
|7| Receptionist | E_ID | E_ID -> Employee |
|8| Booking_Record | Booking_ID | G_ID->Guest, R_ID->Room |
|9| Bill | B_ID | G_ID->Guest, Booking_ID->Booking_Record |
|10| Records | Record_no | - |
|11| Housekeeper_Room | (E_ID,R_ID) | E_ID->Housekeeper, R_ID->Room |
|12| Guest_Manager | (G_ID,E_ID) | G_ID->Guest, E_ID->Manager |
|13| Receptionist_Records | (E_ID,Record_no) | E_ID->Receptionist, Record_no->Records |

ER Note: Hyphens in original (G-ID, Pin-no etc.) converted to underscores (G_ID, Pin_no) for MySQL compatibility.

## How to Run

### Option 1: MySQL CLI
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql

# or inside mysql:
SOURCE database/schema.sql;
SOURCE database/seed.sql;
```

### Option 2: MySQL Workbench / phpMyAdmin
1. Open `schema.sql` and Execute
2. Open `seed.sql` and Execute
3. Refresh schemas -> `hotel_management`

### Verify
```sql
USE hotel_management;
SHOW TABLES;
SELECT * FROM Guest;
SELECT * FROM vw_booking_details;
SELECT * FROM vw_employee_details;
```

## Reset
```sql
DROP DATABASE hotel_management;
SOURCE database/schema.sql;
```

## For JDBC
Update `backend/src/main/resources/db.properties` with:
```
db.url=jdbc:mysql://localhost:3306/hotel_management
db.user=root
db.password=your_password
```
