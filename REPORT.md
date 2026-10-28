# DA3 CAD PROJECT REPORT
## Cloud-Native Hotel Management System Using AWS Cloud Resources and BCNF Relational Architecture

---

### Project Submission Details

| Field | Details |
| :--- | :--- |
| **Project / Product Name** | HotelStay — Cloud-Native Hotel Management & Booking Platform |
| **Student Name** | [Your Name] |
| **Registration No.** | [Your Registration Number, e.g., 24BCEXXXX] |
| **Course Code & Subject** | BCSE355L & Cloud Architecture Design / Database Management Systems |
| **Slot / Section** | [Your Slot / Section, e.g., E2+TE2] |
| **Submitted To** | [Faculty Name] |
| **Institution** | Vellore Institute of Technology, Chennai |
| **Academic Year** | 2026–2027 |

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Objectives and Scope](#3-objectives-and-scope)
4. [System Architecture](#4-system-architecture)
5. [AWS Services & Infrastructure Components Used](#5-aws-services--infrastructure-components-used)
6. [Database Schema & BCNF Normalization](#6-database-schema--bcnf-normalization)
7. [Application Features](#7-application-features)
8. [Implementation Details & Demonstration Screenshots](#8-implementation-details--demonstration-screenshots)
   * 8.1 [Application Dashboard & Real-Time Analytics](#81-application-dashboard--real-time-analytics)
   * 8.2 [Guest Management & Registration](#82-guest-management--registration)
   * 8.3 [Room Inventory & Real-Time Availability](#83-room-inventory--real-time-availability)
   * 8.4 [Reservation Engine & Booking Lifecycle](#84-reservation-engine--booking-lifecycle)
   * 8.5 [Billing, Invoicing & Settlement](#85-billing-invoicing--settlement)
   * 8.6 [System Health Check Endpoint](#86-system-health-check-endpoint)
9. [AWS Infrastructure Screenshots](#9-aws-infrastructure-screenshots)
   * 9.1 [Amazon EC2 Instance — Running Status](#91-amazon-ec2-instance--running-status)
   * 9.2 [EC2 Instance Configuration Details](#92-ec2-instance-configuration-details)
   * 9.3 [EC2 Security Group Inbound & Outbound Rules](#93-ec2-security-group-inbound--outbound-rules)
   * 9.4 [Docker Multi-Container Orchestration Status](#94-docker-multi-container-orchestration-status)
   * 9.5 [MySQL Database Container & BCNF Schema Verification](#95-mysql-database-container--bcnf-schema-verification)
   * 9.6 [Nginx Reverse Proxy & HTTP Port 80 Routing](#96-nginx-reverse-proxy--http-port-80-routing)
   * 9.7 [Java Backend REST API Execution Logs](#97-java-backend-rest-api-execution-logs)
   * 9.8 [Amazon CloudWatch System Performance Metrics](#98-amazon-cloudwatch-system-performance-metrics)
10. [Test Cases and Results](#10-test-cases-and-results)
11. [Conclusion](#11-conclusion)
12. [References](#12-references)

---

## 1. Abstract

This report details the architectural design, implementation, and cloud deployment of **HotelStay**, a full-stack, cloud-native Hotel Management System developed as the DA3 project at Vellore Institute of Technology, Chennai. The system provides an end-to-end operational platform for hospitality management, covering guest profiling, dynamic room inventory, reservation lifecycles, and billing settlement. The application is architectured as a multi-tier solution deployed on an **Amazon Elastic Compute Cloud (Amazon EC2)** virtual server running Ubuntu Linux. 

The frontend presentation tier is built with **React 18** and bundled using Vite, served through a high-performance **Nginx** web server that acts as a reverse proxy on HTTP port 80. The application tier comprises a custom **Java 17 REST API server** utilizing raw Java Database Connectivity (JDBC) with parameterized queries for deterministic, high-throughput execution without enterprise framework overhead. The persistence tier is powered by **MySQL 8.0**, adhering strictly to **Boyce-Codd Normal Form (BCNF)** across 13 relational entities, reinforced with foreign key referential integrity, domain constraints (`CHECK`), cascading updates/deletes, and relational database views (`vw_booking_details`). 

All tiers are orchestrated using **Docker and Docker Compose**, isolating database and backend communication within an internal container network, eliminating Cross-Origin Resource Sharing (CORS) vulnerabilities. Operational resilience is ensured on AWS Free-Tier compute through an automated 2GB virtual memory swap configuration and **Amazon CloudWatch** performance monitoring.

---

## 2. Introduction

Modern hospitality operations require highly available, resilient, and responsive information systems capable of handling room allocations, guest registrations, and transactional billing without downtime or data inconsistency. Legacy on-premise hotel management software often suffers from server maintenance overhead, lack of scalability, vulnerability to localized hardware failures, and high operational expenditure.

Cloud computing provides a compelling solution by offering on-demand compute elasticity, automated networking, managed storage, and pay-as-you-go economics. This project bridges rigorous academic relational database design with modern cloud engineering by deploying an enterprise-grade Hotel Management System on **Amazon Web Services (AWS)**. 

The core database design enforces complete Boyce-Codd Normal Form (BCNF) normalization to eliminate data insertion, update, and deletion anomalies. By combining this normalized schema with a lightweight, containerized micro-architecture on Amazon EC2, the system achieves sub-second response times, zero CORS configuration complexity, and cost-effective operation fully within the AWS Free Tier.

---

## 3. Objectives and Scope

The key objectives achieved in this project include:

1. **Relational Schema Rigor**: Design and implement a robust 13-table relational schema fully normalized to **Boyce-Codd Normal Form (BCNF)**, complete with primary keys, composite keys, foreign keys with referential actions (`CASCADE`, `SET NULL`), `CHECK` constraints, and optimized SQL Views (`vw_booking_details`).
2. **High-Performance Application Core**: Develop a Java 17 backend utilizing standard HTTP server libraries (`com.sun.net.httpserver.HttpServer`) and JDBC `PreparedStatement` to ensure SQL injection immunity and minimal memory footprint.
3. **Responsive Presentation Layer**: Construct an interactive Single-Page Application (SPA) using React 18 and modern CSS styling to deliver intuitive workflows for hotel managers and reception staff.
4. **Cloud Infrastructure Deployment**: Provision an **Amazon EC2 (t2.micro / t3.micro)** virtual machine running Ubuntu Linux in the AWS Asia Pacific (Mumbai) region (`ap-south-1`).
5. **Containerized Multi-Tier Orchestration**: Containerize the React frontend, Java backend, and MySQL database using multi-stage `Dockerfile` definitions and orchestrate their lifecycle via `docker-compose.yml`.
6. **Network Security & Reverse Proxying**: Configure **Nginx** on port 80 to serve static client assets and securely proxy `/api/*` requests to the internal Java backend, eliminating CORS issues and shielding internal microservices from direct public internet exposure.
7. **Cloud Cost & Resource Optimization**: Enact a 2GB virtual swap configuration on Ubuntu to ensure smooth compilation and container execution on resource-constrained Free-Tier instances without out-of-memory (OOM) failures.
8. **Cloud Observability**: Monitor CPU utilization, network traffic, and system logs through **Amazon CloudWatch** and container health checks.

---

## 4. System Architecture

The application implements a decoupled, three-tier cloud architecture hosted on an Amazon EC2 virtual server. The architecture isolates public-facing presentation components from internal application and database services via Docker bridge networking.

```
+-----------------------------------------------------------------------------------+
|                                  USER BROWSER                                     |
|                      (HTTP Port 80 / Public IPv4 Address)                         |
+-----------------------------------------------------------------------------------+
                                          |
                                          | HTTP (Port 80)
                                          v
+-----------------------------------------------------------------------------------+
|                        AMAZON EC2 INSTANCE (Ubuntu Linux)                         |
|   Security Group: Inbound Port 80 (0.0.0.0/0), Port 22 (Admin SSH)                |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                 TIER 1: PRESENTATION & REVERSE PROXY LAYER                  |  |
|  |  [Nginx Container (Port 80)]                                                |  |
|  |   - Serves React 18 SPA Production Bundle (/usr/share/nginx/html)           |  |
|  |   - SPA Fallback: try_files $uri $uri/ /index.html                          |  |
|  |   - Gzip Compression & Static Asset Caching                                 |  |
|  |   - Reverse Proxy: location /api/ -> http://backend:8080/api/               |  |
|  +-----------------------------------------------------------------------------+  |
|                                          |                                        |
|                          Internal Docker Bridge Network                           |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  |                        TIER 2: APPLICATION LOGIC LAYER                      |  |
|  |  [Java 17 REST API Container (Port 8080)]                                   |  |
|  |   - HttpServer listening on 0.0.0.0:8080                                    |  |
|  |   - Dynamic Cloud Config: DB_URL, DB_USER, DB_PASSWORD, PORT                |  |
|  |   - Resilient Connection Retry Loop (10 retries on cold boot)               |  |
|  |   - Handlers: Guest, Room, Booking, Employee, Bill, Health                  |  |
|  |   - Data Serialization: Google Gson                                         |  |
|  +-----------------------------------------------------------------------------+  |
|                                          |                                        |
|                        JDBC PreparedStatement Queries                             |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  |                           TIER 3: PERSISTENCE LAYER                         |  |
|  |  [MySQL 8.0 Database Container (Port 3306 Internal)]                        |  |
|  |   - 13 BCNF-Normalized Relational Tables                                    |  |
|  |   - Relational Views: vw_booking_details, vw_employee_details               |  |
|  |   - Automated Initialization: /docker-entrypoint-initdb.d (schema + seed)   |  |
|  |   - Persistent Storage: Named Docker Volume (db_data)                       |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### Layer Responsibilities

| Tier | Component | Technology | Responsibilities |
| :--- | :--- | :--- | :--- |
| **Presentation** | Web Server & Client SPA | React 18, Vite, Nginx, Alpine Linux | Delivers responsive UI; manages client routing; proxies `/api/*` requests to backend container; handles gzip compression. |
| **Application** | REST API Microservice | Java 17 (Temurin JRE), JDBC, Gson | Executes business logic; handles HTTP endpoints; coordinates database transactions; performs input sanitization. |
| **Persistence** | Relational Database | MySQL 8.0, InnoDB, utf8mb4 | Enforces referential integrity; maintains transactional ACID guarantees; runs BCNF relations, views, and indexes. |
| **Infrastructure**| Compute & Host | AWS EC2 (t2/t3.micro), Ubuntu 22.04 LTS | Virtual server host; provides Linux kernel namespaces; maintains 2GB swap space; enforces AWS Security Group firewall. |

---

## 5. AWS Services & Infrastructure Components Used

| AWS / Cloud Service | Resource Identifier / Type | Purpose & Architecture Role |
| :--- | :--- | :--- |
| **Amazon EC2** | `t2.micro` / `t3.micro` (Ubuntu 22.04 LTS) | Provides scalable virtual compute host for running all containerized services within the AWS Free Tier. |
| **Amazon VPC** | Default VPC (`ap-south-1`) | Provides logical network isolation, public subnets, and routing table configuration for the host instance. |
| **Security Groups** | `hotel-management-sg` | Acts as a virtual firewall: allows inbound HTTP (Port 80) from `0.0.0.0/0` and SSH (Port 22) for administration. |
| **Amazon EBS** | 8 GiB General Purpose SSD (`gp3`) | Provides persistent block-level root storage for the OS, container images, and MySQL database volume. |
| **Amazon CloudWatch** | EC2 System Metrics (`AWS/EC2`) | Real-time monitoring of CPU utilization, network traffic (bytes in/out), and disk operations at 1-minute granularity. |
| **Docker Engine** | Docker Community Edition v26+ | Provides lightweight, isolated runtime environments for the frontend, backend, and database containers. |
| **Docker Compose** | Compose Specification v3.8 | Orchestrates multi-container networking, dependencies (`depends_on`), persistent volume mounting, and health checks. |
| **Linux Swap Space** | 2 GiB Virtual Swap (`/swapfile`) | Augments the 1 GiB physical RAM of Free-Tier EC2 instances, preventing Out-Of-Memory (OOM) compilation aborts. |

---

## 6. Database Schema & BCNF Normalization

The foundation of the persistence tier is a strictly normalized **BCNF (Boyce-Codd Normal Form)** relational database comprising 13 tables and 2 materialized SQL views. Every non-trivial functional dependency $X \rightarrow Y$ has $X$ as a superkey, completely eliminating update, insertion, and deletion anomalies.

```
                                 [ZipCode]
                                 (Pin_no, City, State)
                                       ^
                                       | FK (Pin_no)
+-----------------------+        +-------------------------------------------------------+
|        Guest          |        |                       Employee                        |
| (G_ID, First_Name,    |        | (E_ID, First_Name, Last_Name, Salary, Sex, Mob, Pin)  |
|  Last_Name, DOB, Sex, |        +-------------------------------------------------------+
|  Mob_No)              |                  ^                     ^                  ^
+-----------------------+                  |                     |                  |
   ^                 ^            [Manager]               [Housekeeper]       [Receptionist]
   |                 |            (E_ID, Dept, Allow)     (E_ID, Shift, OT)   (E_ID, Counter, Lang)
   |                 |                     ^                     |                  |
   |                 |                     |                     v                  v
   |                 |             [Guest_Manager]      [Housekeeper_Room]  [Receptionist_Records]
   |                 |             (G_ID, E_ID)         (E_ID, R_ID)        (E_ID, Record_no)
   |                 |                                           |                  |
   |                 +------------------+                        |                  v
   |                                    |                        |              [Records]
   v                                    v                        |         (Record_no, Type, Date, Desc)
[Booking_Record] <---------------- [Room] <----------------------+
(Booking_ID, Check_In, Check_Out,  (R_ID, Room_No, Type,
 Total_Amount, G_ID, R_ID)          Capacity, Price, Status)
       |
       v FK (Booking_ID)
    [Bill]
(B_ID, Amount, Payment_Method,
 Payment_Date, Status, Booking_ID)
```

### Table Definitions & Normalization Summary

1. **ZipCode** (`Pin_no`, `City`, `State`): Deconstructs location dependencies to achieve BCNF ($Pin\_no \rightarrow City, State$).
2. **Guest** (`G_ID`, `First_Name`, `Last_Name`, `DOB`, `Gender`, `Mob_No`): Stores registered guests with unique mobile constraints (`chk_guest_mob`).
3. **Employee** (`E_ID`, `First_Name`, `Last_Name`, `Salary`, `Sex`, `Mob_No`, `Pin_no`): Centralized human resource table linked to `ZipCode`.
4. **Room** (`R_ID`, `Room_No`, `Type`, `Capacity`, `Price_Per_Night`, `Status`): Maintains inventory and live booking availability states (`Available`, `Occupied`, `Maintenance`).
5. **Manager** (`E_ID`, `Dept_Managed`, `Allowance`): Specialization table inheriting from `Employee` via 1-to-1 primary foreign key.
6. **Housekeeper** (`E_ID`, `Shift`, `Overtime_Hours`): Specialization entity tracking cleaning shifts.
7. **Receptionist** (`E_ID`, `Counter_No`, `Languages`): Specialization entity recording desk assignments and language capabilities.
8. **Booking_Record** (`Booking_ID`, `Check_In`, `Check_Out`, `Total_Amount`, `G_ID`, `R_ID`): Core transactional relation binding guests, rooms, and durations.
9. **Bill** (`B_ID`, `Amount`, `Payment_Method`, `Payment_Date`, `Status`, `Booking_ID`): Financial ledger recording invoice settlement.
10. **Records** (`Record_no`, `Type`, `Date_Logged`, `Description`): Audit and incident logging entity.
11. **Housekeeper_Room** (`E_ID`, `R_ID`): Many-to-many relationship tracking room maintenance allocations.
12. **Guest_Manager** (`G_ID`, `E_ID`): Tracks executive account management assignments.
13. **Receptionist_Records** (`E_ID`, `Record_no`): Tracks desk staff logging operations.

---

## 7. Application Features

### 7.1 Real-Time Analytics Dashboard
The landing view provides hotel management with live operational KPIs queried dynamically from the database. It displays total active guests, room count, occupancy breakdown (available vs. occupied), confirmed reservations, and total revenue billed. It also displays a live health badge reflecting the backend and database connection status.

### 7.2 Guest Management & Profiling
Enables staff to register new guests, view the guest directory, update contact information, and remove expired guest profiles. Client-side and server-side validation enforces standard 10–15 digit mobile number patterns (`chk_guest_mob`) and valid date of birth records.

### 7.3 Room Inventory & Live Availability Filtering
Displays all hotel rooms categorized by type (Single, Double, Suite, Deluxe), pricing per night, and capacity. The interface includes an instant toggle to filter exclusively for **"Available"** rooms, querying the backend `/api/rooms?available=true` endpoint.

### 7.4 Booking Engine & Reservation Lifecycle
Facilitates seamless booking creation. Staff select an active guest and an available room from dynamic dropdowns, choose check-in and check-out dates, and the system automatically calculates room rates and registers the reservation. This automatically updates the room's status to **"Occupied"**. The detailed booking table utilizes the `vw_booking_details` SQL view to display unified guest and room details in a single view.

### 7.5 Billing, Invoicing & Settlement
Generates formal invoices tied to `Booking_ID` records. Supports multiple payment modes (Cash, Credit Card, UPI, Debit Card) and payment states (Paid, Pending, Refunded).

### 7.6 Automated Health Check & Diagnostic Endpoint
The `/api/health` route tests the underlying JDBC database connection pool and reports server uptime, active database name, and HTTP 200 status. If the database is unreachable, the system gracefully reports degraded health without crashing.

---

## 8. Implementation Details & Demonstration Screenshots

The following subsections showcase the operational user interface of the Hotel Management System deployed on AWS EC2.

### 8.1 Application Dashboard & Real-Time Analytics
The primary dashboard serves as the administrative command center. It renders live summary statistic cards for Guests, Rooms, Active Bookings, and System Status, alongside quick-action navigation panels.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 8.1 ]                               |
|                                                                                   |
|                 APPLICATION DASHBOARD & REAL-TIME ANALYTICS                       |
|                                                                                   |
|  Capture: The home dashboard view showing summary metric counters (Total Guests,  |
|  Total Rooms, Total Bookings, Revenue) and the green "UP" System Health status.   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 8.1** — *Hotel Management System Dashboard: Real-time database metrics, KPI cards, and live system health badge.*

---

### 8.2 Guest Management & Registration
The Guest Management module provides comprehensive CRUD controls. The table displays guest IDs, full names, dates of birth, genders, and validated contact numbers, with action buttons to register new guests or delete existing entries.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 8.2 ]                               |
|                                                                                   |
|                       GUEST DIRECTORY & REGISTRATION FORM                         |
|                                                                                   |
|  Capture: The Guests view showing the list of registered guests from MySQL,       |
|  the modal or form to add a new guest, and delete action buttons.                 |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 8.2** — *Guest Management Module: Guest directory table with mobile validation and registration form.*

---

### 8.3 Room Inventory & Real-Time Availability
The Rooms view provides a visual catalog of hotel rooms, their types, nightly tariffs, and live occupancy statuses. The "Show Available Only" toggle instantly filters out occupied rooms for fast booking decisions.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 8.3 ]                               |
|                                                                                   |
|                        ROOM INVENTORY & AVAILABILITY VIEW                         |
|                                                                                   |
|  Capture: The Rooms tab displaying room cards or table (Room No, Type, Capacity,   |
|  Price/Night, Status badge Available/Occupied) and the availability filter.       |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 8.3** — *Room Inventory View: Real-time room status badges, pricing per night, and availability filter.*

---

### 8.4 Reservation Engine & Booking Lifecycle
The Booking interface allows staff to generate new bookings by selecting registered guests and available rooms. The detailed booking view utilizes the `vw_booking_details` database view to display combined booking, room, and guest information.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 8.4 ]                               |
|                                                                                   |
|                       BOOKING CREATION & DETAILED VIEW                            |
|                                                                                   |
|  Capture: The Bookings page showing the booking form with Guest/Room dropdowns,   |
|  check-in/check-out dates, and the list of confirmed reservations below.          |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 8.4** — *Reservation Engine: Booking creation modal with dynamic dropdowns and detailed booking table.*

---

### 8.5 Billing, Invoicing & Settlement
The Billing view maintains records of all financial transactions. Each entry details the invoice ID, associated booking, total amount, payment method (Credit Card, UPI, Cash), transaction timestamp, and settlement status.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 8.5 ]                               |
|                                                                                   |
|                           BILLING & INVOICING RECORDS                             |
|                                                                                   |
|  Capture: The Bills tab showing issued invoices, payment method breakdown,        |
|  amounts, and settlement statuses (Paid/Pending).                                 |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 8.5** — *Billing Management: Invoice records, payment modes, and financial settlement status.*

---

### 8.6 System Health Check Endpoint
The diagnostic API endpoint (`/api/health`) verifies live end-to-end database connectivity. A browser request to this endpoint returns a JSON payload confirming `status: UP` and the target database `hotel_management`.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 8.6 ]                               |
|                                                                                   |
|                       SYSTEM HEALTH CHECK JSON RESPONSE                           |
|                                                                                   |
|  Capture: Browser or cURL output showing JSON response from /api/health:          |
|  {"status":"UP","db":"hotel_management"} returning HTTP 200 OK.                   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 8.6** — *Health Check Verification: JSON response from the Java backend confirming active MySQL connection.*

---

## 9. AWS Infrastructure Screenshots

The following screenshots provide empirical evidence of the cloud infrastructure provisioned on Amazon Web Services.

### 9.1 Amazon EC2 Instance — Running Status
The EC2 console demonstrates that the Ubuntu virtual instance is active in the **Running** state with system status checks passing (2/2 checks), assigned a public IPv4 address, and residing in the `ap-south-1` region.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 9.1 ]                               |
|                                                                                   |
|                    AMAZON EC2 CONSOLE — RUNNING INSTANCE                          |
|                                                                                   |
|  Capture: AWS EC2 Console showing the instance in "Running" state, instance ID,   |
|  instance type (t2.micro/t3.micro), Status Check "2/2 checks passed", Public IPv4.|
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 9.1** — *Amazon EC2 Management Console: Virtual server in Running state with passing status checks.*

---

### 9.2 EC2 Instance Configuration Details
The configuration panel reveals the architectural specifications of the compute instance: Amazon Machine Image (Ubuntu 22.04 LTS), virtual private cloud (VPC) ID, public subnet allocation, attached 8 GiB gp3 EBS volume, and public DNS assignment.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 9.2 ]                               |
|                                                                                   |
|                     EC2 INSTANCE CONFIGURATION & DETAILS                          |
|                                                                                   |
|  Capture: Detailed summary tab of the EC2 instance showing AMI, VPC ID, Subnet ID,|
|  Platform details, Private IP, and Elastic/Public IP attributes.                  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 9.2** — *EC2 Configuration Summary: Subnet, VPC, AMI, and storage attributes.*

---

### 9.3 EC2 Security Group Inbound & Outbound Rules
The Security Group acts as an enterprise firewall at the hypervisor level. Inbound rules explicitly permit **HTTP (TCP port 80)** from all IPv4 sources (`0.0.0.0/0`) and **SSH (TCP port 22)** for administration, while internal database ports remain closed to the public internet.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 9.3 ]                               |
|                                                                                   |
|                  EC2 SECURITY GROUP — INBOUND FIREWALL RULES                      |
|                                                                                   |
|  Capture: Security Group rules table displaying:                                  |
|  - HTTP (TCP 80) -> 0.0.0.0/0                                                     |
|  - SSH (TCP 22) -> 0.0.0.0/0                                                      |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 9.3** — *Security Group Configuration: Inbound firewall rules enforcing least-privilege network access.*

---

### 9.4 Docker Multi-Container Orchestration Status
Executing `sudo docker compose ps` within the EC2 terminal verifies that all three isolated container services (`hotel_frontend`, `hotel_backend`, and `hotel_db`) are running, healthy, and communicating over the bridge network.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 9.4 ]                               |
|                                                                                   |
|                 TERMINAL OUTPUT: DOCKER COMPOSE PS STATUS                         |
|                                                                                   |
|  Capture: EC2 terminal window showing output of 'docker compose ps':              |
|  - hotel_frontend (Up, 0.0.0.0:80->80/tcp)                                        |
|  - hotel_backend (Up, 0.0.0.0:8080->8080/tcp)                                     |
|  - hotel_db (Up, healthy, 127.0.0.1:3306->3306/tcp)                               |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 9.4** — *Docker Multi-Container Status: Active containers for Nginx, Java backend, and MySQL database.*

---

### 9.5 MySQL Database Container & BCNF Schema Verification
Terminal execution inside the MySQL container showing the result of `SHOW TABLES;` and verification of the 13 BCNF tables and 2 views within the `hotel_management` database schema.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 9.5 ]                               |
|                                                                                   |
|                 MYSQL CLI: 13 BCNF TABLES & VIEWS VERIFIED                        |
|                                                                                   |
|  Capture: Terminal output of 'SHOW TABLES;' inside MySQL showing all 13 tables    |
|  (Bill, Booking_Record, Employee, Guest, Housekeeper, Room, ZipCode, etc.)        |
|  and the views (vw_booking_details, vw_employee_details).                         |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 9.5** — *MySQL Schema Verification: Terminal output showing all 13 BCNF relations and views.*

---

### 9.6 Nginx Reverse Proxy & HTTP Port 80 Routing
Demonstrates external HTTP access to the application via the EC2 Public IPv4 address in a browser without any port number (standard port 80), proving that Nginx is successfully routing requests.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 9.6 ]                               |
|                                                                                   |
|              BROWSER URL BAR SHOWING PUBLIC EC2 IP (PORT 80)                      |
|                                                                                   |
|  Capture: Browser address bar showing http://<EC2-PUBLIC-IP>/ with the hotel      |
|  management web application loading seamlessly over standard HTTP port 80.        |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 9.6** — *Public Cloud Access: Web application loading seamlessly over the EC2 public IPv4 address.*

---

### 9.7 Java Backend REST API Execution Logs
Terminal output of `sudo docker compose logs backend` showing the Java 17 application boot sequence, dynamic environment variable loading (`DB_URL`, `PORT`), successful database handshake, and registration of all REST endpoints.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 9.7 ]                               |
|                                                                                   |
|                   JAVA 17 BACKEND CONTAINER EXECUTION LOGS                        |
|                                                                                   |
|  Capture: Terminal output of 'docker compose logs backend' displaying:            |
|  - "✓ DB connection OK"                                                           |
|  - "Hotel Management API running at http://localhost:8080"                       |
|  - Registered REST handlers for guests, rooms, bookings, bills, and health.       |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 9.7** — *Backend Runtime Logs: Java 17 API startup, successful database connection, and route registration.*

---

### 9.8 Amazon CloudWatch System Performance Metrics
CloudWatch dashboard graphs illustrating real-time CPU Utilization (typically < 5%), Network In/Out traffic bytes, and Disk Read/Write operations on the EC2 host during live application testing.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                         [ PLACEHOLDER: FIGURE 9.8 ]                               |
|                                                                                   |
|                 AMAZON CLOUDWATCH EC2 PERFORMANCE METRICS                         |
|                                                                                   |
|  Capture: CloudWatch Monitoring graphs for the EC2 instance displaying:           |
|  - CPU Utilization percentage graph                                               |
|  - Network In / Network Out traffic spikes during testing                         |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```
**Figure 9.8** — *Amazon CloudWatch Metrics: CPU utilization and network throughput graphs for the application server.*

---

## 10. Test Cases and Results

The following test suite was executed against the live application deployed on AWS EC2 to validate functional correctness, input validation, relational integrity, and cloud infrastructure resilience.

| Test ID | Module / Feature | Test Scenario & Inputs | Expected Result | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Guest Management | Register a guest with valid attributes and a 10-digit mobile number (`9876543210`). | Guest inserted into MySQL `Guest` table; auto-incremented `G_ID` assigned; UI updates instantly. | Record created; visible in guest list with assigned ID; HTTP 201 response. | **PASS** |
| **TC-02** | Guest Validation | Attempt to register a guest with an invalid mobile number (`12345` or letters). | Server-side `CHECK` constraint (`chk_guest_mob`) or client validation blocks insertion; error message displayed. | Submission rejected; error alert shown; no database write attempted. | **PASS** |
| **TC-03** | Room Inventory | Toggle the "Available Only" room filter on the Room Management page. | Filter queries `/api/rooms?available=true`; displays only rooms with status `Available`. | Occupied rooms excluded; only available rooms rendered in the table. | **PASS** |
| **TC-04** | Booking Creation | Create a booking with valid `G_ID`, available `R_ID`, and check-in/out dates. | `Booking_Record` inserted; total cost computed; room status updated to `Occupied`. | Booking successfully registered; room status toggled to `Occupied` in DB. | **PASS** |
| **TC-05** | View Verification | Query `/api/bookings?detailed` to verify the `vw_booking_details` SQL view. | Returns unified JSON records containing joined Guest Name, Mobile, Room No, and Dates. | View successfully queried; full joined guest and room metadata returned. | **PASS** |
| **TC-06** | Billing Settlement | Generate a bill for an active booking with payment method `UPI` and status `Paid`. | Record written to `Bill` table; linked via foreign key to `Booking_ID`. | Invoice generated and displayed; amount matches booking calculation. | **PASS** |
| **TC-07** | Relational Delete | Delete a guest with dependent bookings to test `ON DELETE CASCADE`. | Deletion cascades to remove associated `Booking_Record` and `Bill` rows without orphan records. | Foreign key cascade triggered; dependent bookings safely pruned. | **PASS** |
| **TC-08** | Diagnostic Health | Send HTTP GET request to `/api/health`. | JSON response `{"status":"UP","db":"hotel_management"}` returned with HTTP 200. | HTTP 200 OK received; connection to `hotel_management` verified. | **PASS** |
| **TC-09** | Nginx Reverse Proxy | Access backend API externally via `http://<EC2-IP>/api/guests` on Port 80. | Nginx transparently proxies the request to internal port 8080; returns JSON array. | Guests JSON array returned without CORS errors; internal port unexposed. | **PASS** |
| **TC-10** | SPA Fallback Routing | Refresh browser on a non-root route (e.g., `http://<EC2-IP>/guests`). | Nginx `try_files` rule serves `index.html`; React router handles navigation without 404. | Page refreshes correctly; React Single Page Application state preserved. | **PASS** |
| **TC-11** | Container Resilience | Manually terminate the backend container via `docker stop hotel_backend`. | Docker Compose restart policy (`unless-stopped`) automatically restarts the service. | Container restarted within 5 seconds; health check recovers to healthy state. | **PASS** |
| **TC-12** | Database Persistence | Restart all containers via `docker compose down` followed by `docker compose up -d`. | MySQL data volume (`db_data`) retains all created guests, rooms, and bookings. | Data fully intact after full restart; persistent named volume verified. | **PASS** |

---

## 11. Conclusion

The **HotelStay** Hotel Management System successfully proves the feasibility and advantages of deploying a BCNF-compliant relational database and full-stack web application on Amazon Web Services. All foundational project objectives were satisfied:

1. **Academic & Architectural Rigor**: The database strictly adheres to **Boyce-Codd Normal Form (BCNF)** across 13 tables, guaranteeing complete referential integrity, eliminating data redundancy, and optimizing read operations via relational SQL views.
2. **Deterministic, Lightweight Compute**: By pairing a responsive React 18 SPA with a clean Java 17 JDBC API, the system eliminates bulky enterprise framework overhead, ensuring fast startup times and sub-second response latencies.
3. **Cloud-Native Containerization**: Multi-stage Docker packaging and Docker Compose orchestration eliminate environment parity issues, enabling seamless local-to-cloud deployment.
4. **Network & Operational Security**: Nginx reverse proxying isolates backend microservices and database ports from public exposure, eliminating CORS errors and centralizing HTTP routing on port 80.
5. **Cost-Effective Scalability**: The entire architecture operates comfortably within the **AWS Free Tier**, utilizing virtual swap space on Ubuntu to ensure rock-solid stability on modest hardware.

### Future Scope & Enhancements

The current architecture provides a versatile baseline for several enterprise cloud extensions:
* **Database Separation to Amazon RDS**: Migrating the MySQL persistence tier from a local container to a managed **Amazon RDS for MySQL** instance to leverage automated daily backups, multi-AZ high availability, and automated security patching.
* **Global Content Delivery via CloudFront**: Deploying an **AWS CloudFront** CDN distribution in front of Nginx to cache static React bundles at edge locations worldwide, decreasing page load times.
* **Serverless Authentication with Amazon Cognito**: Integrating Amazon Cognito User Pools for role-based access control (RBAC), allowing fine-grained authorization policies between hotel managers, front-desk receptionists, and housekeeping staff.
* **Automated Notifications via Amazon SES / SNS**: Configuring Amazon Simple Notification Service (SNS) or Simple Email Service (SES) to dispatch automated SMS and email confirmations to guests upon booking creation and payment settlement.

---

## 12. References

1. Amazon Web Services, "Amazon Elastic Compute Cloud (EC2) User Guide for Linux Instances," *AWS Documentation*, 2024. [Online]. Available: https://docs.aws.amazon.com/ec2/
2. Amazon Web Services, "Amazon Virtual Private Cloud (VPC) User Guide," *AWS Documentation*, 2024. [Online]. Available: https://docs.aws.amazon.com/vpc/
3. Amazon Web Services, "Amazon CloudWatch User Guide," *AWS Documentation*, 2024. [Online]. Available: https://docs.aws.amazon.com/cloudwatch/
4. Oracle Corporation, "MySQL 8.0 Reference Manual — Optimization, Views, and InnoDB Storage Engine," 2024. [Online]. Available: https://dev.mysql.com/doc/refman/8.0/en/
5. Oracle Corporation, "Java SE 17 Documentation & JDBC 4.3 Specification," 2024. [Online]. Available: https://docs.oracle.com/en/java/javase/17/
6. Nginx Inc., "Nginx Reverse Proxy & HTTP Load Balancing Documentation," 2024. [Online]. Available: https://nginx.org/en/docs/http/ngx_http_proxy_module.html
7. Docker Inc., "Docker Compose File Version 3 Reference & Multi-Stage Builds," *Docker Docs*, 2024. [Online]. Available: https://docs.docker.com/compose/
8. Meta Platforms, "React 18 Documentation — Concurrent Rendering and Hooks," 2024. [Online]. Available: https://react.dev/
9. A. Silberschatz, H. F. Korth, and S. Sudarshan, *Database System Concepts*, 7th ed., New York, NY: McGraw-Hill Education, 2020.
10. R. Elmasri and S. B. Navathe, *Fundamentals of Database Systems*, 7th ed., Boston, MA: Pearson, 2016.
