# Hotel Management System — Frontend (React) + Backend (MySQL + JDBC)

BCNF schema with 13 tables as per spec.

## Project Structure
```
DBMS_project/
├── database/
│   ├── schema.sql      # ✅ Complete DDL - run first
│   ├── seed.sql        # ✅ Sample data
│   └── README.md
├── backend/            # Java 17 + JDBC + HttpServer REST API
│   ├── pom.xml
│   ├── src/main/java/com/hotel/
│   │   ├── config/DBConnection.java
│   │   ├── model/ Guest.java, Room.java, Booking.java
│   │   ├── dao/ GuestDAO.java, RoomDAO.java, BookingDAO.java
│   │   ├── api/ GuestHandler.java, RoomHandler.java, BookingHandler.java
│   │   └── Main.java
│   └── src/main/resources/db.properties
└── frontend/           # React 18 + Vite + Axios
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx
        └── components/ Dashboard, Guests, Rooms, Bookings
```

## 1. Database Setup (DONE)

**schema.sql** covers all 13 relations:
- Guest(G-ID, ...), ZipCode(Pin-no, ...), Employee(E-ID, ..., Pin-no), Room(R-ID, ...), Manager(E-ID,...), Housekeeper(E-ID), Receptionist(E-ID), Booking_Record(Booking-ID,...), Bill(B-ID,...), Records(Record-no,...), Housekeeper_Room(E-ID,R-ID), Guest_Manager(G-ID,E-ID), Receptionist_Records(E-ID,Record-no)
- Hyphens converted to underscores for MySQL.
- FKs, CHECKs, Indexes, Views (`vw_booking_details`, `vw_employee_details`)

Run:
```bash
# MySQL CLI
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql

# Or inside MySQL:
SOURCE database/schema.sql;
SOURCE database/seed.sql;
```

Verify:
```sql
USE hotel_management;
SHOW TABLES; -- should show 13 tables + 2 views
SELECT * FROM vw_booking_details;
```

## 2. Backend Setup (JDBC)

1. Install Maven (https://maven.apache.org/download.cgi) or use IntelliJ/Eclipse bundled Maven
2. Edit `backend/src/main/resources/db.properties` → set your MySQL password
3. Build & Run:
```bash
cd backend
mvn package
java -jar target/hotel-management-backend-1.0.0-jar-with-dependencies.jar
# API at http://localhost:8080
# Test: curl http://localhost:8080/api/health
```

Endpoints (all via JDBC PreparedStatement):
- `GET /api/health`
- `GET /api/guests` , `GET /api/guests/{id}` , `POST /api/guests` , `PUT /api/guests` , `DELETE /api/guests/{id}`
- `GET /api/rooms` , `GET /api/rooms?available=true` , `POST /api/rooms`
- `GET /api/bookings` , `GET /api/bookings?detailed` (uses vw_booking_details), `POST /api/bookings`

## 3. Frontend Setup (React)

```bash
cd frontend
npm install
npm run dev
# App at http://localhost:5173
# Vite proxies /api to http://localhost:8080
```

Features: Dashboard stats, Guest CRUD, Room listing, Booking creation with Guest/Room dropdowns.

## 4. Next Steps

- Extend DAOs for remaining tables: Employee, Manager, Housekeeper, Receptionist, Bill, Records, Housekeeper_Room, Guest_Manager, Receptionist_Records (pattern in `GuestDAO.java:1`)
- Add Bill generation trigger on checkout
- Add Auth (login for Manager/Receptionist)

## Tech Stack

- Frontend: HTML/CSS/ReactJS (Vite)
- Backend: Java 17, JDBC, MySQL Connector/J 8.0.33, Gson, Java HttpServer
- DB: MySQL 8.x, InnoDB, utf8mb4

## Screenshots

Run seed.sql then open frontend to see sample guests/rooms/bookings.
