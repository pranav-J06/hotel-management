import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_word_report():
    doc = Document()

    # Set 1-inch margins (standard Word layout)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base styles
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(11)
    normal_font.color.rgb = RGBColor(0x26, 0x26, 0x26)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    def set_cell_background(cell, fill_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_table_borders(table, color="D3D3D3"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)
        return p

    def add_figure(img_path, caption_text, width=5.6):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run()
            run.add_picture(img_path, width=Inches(width))
            
            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_after = Pt(10)
            crun = cp.add_run(caption_text)
            crun.font.name = 'Calibri'
            crun.font.size = Pt(9.5)
            crun.font.italic = True
            crun.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    # ==================== COVER PAGE ====================
    logo_p = doc.add_paragraph()
    logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    logo_p.paragraph_format.space_before = Pt(12)
    logo_p.paragraph_format.space_after = Pt(16)
    if os.path.exists("images/vit_chennai_logo.png"):
        l_run = logo_p.add_run()
        l_run.add_picture("images/vit_chennai_logo.png", width=Inches(3.3))

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(8)
    title_p.paragraph_format.space_after = Pt(6)
    t_run = title_p.add_run("DA3 CAD PROJECT REPORT")
    t_run.font.name = 'Calibri'
    t_run.font.size = Pt(16)
    t_run.font.bold = True
    t_run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(24)
    s_run = sub_p.add_run("Cloud-Native Hotel Management System Using AWS Cloud Resources and BCNF Relational Architecture")
    s_run.font.name = 'Calibri'
    s_run.font.size = Pt(12.5)
    s_run.font.bold = True
    s_run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    # Details Table
    details = [
        ("Project / Product Name", "HotelStay Management System"),
        ("Student Name", "Pranav Jahagirdar"),
        ("Registration No.", "24BCE1503"),
        ("Course Code & Subject", "BCSE355L & Cloud Architecture Design"),
        ("Slot / Section", "E2+TE2"),
        ("Submitted To", "Preetha Evangeline D"),
        ("Institution", "Vellore Institute of Technology, Chennai"),
        ("Academic Year", "2026–2027")
    ]

    table = doc.add_table(rows=len(details), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, "BFBFBF")

    for i, (label, val) in enumerate(details):
        row = table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.5)
        c1.width = Inches(4.0)
        set_cell_background(c0, "F2F2F2")
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(10.5)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        if label in ["Student Name", "Registration No.", "Submitted To"]:
            r1.font.bold = True
        r1.font.size = Pt(10.5)

    doc.add_page_break()

    # ==================== TABLE OF CONTENTS ====================
    add_h1("Table of Contents")
    toc_items = [
        ("1. Abstract", "3"),
        ("2. Introduction", "3"),
        ("3. Objectives and Scope", "4"),
        ("4. System Architecture", "4"),
        ("5. AWS Services & Infrastructure Components Used", "5"),
        ("6. Database Schema & BCNF Normalization", "6"),
        ("7. Application Features", "8"),
        ("8. Implementation Details & Demonstration Screenshots", "9"),
        ("    8.1 Application Header & Live Health Status", "9"),
        ("    8.2 Guest & Room Management (Enter Details View)", "9"),
        ("    8.3 Room & Booking Allocation Form", "10"),
        ("    8.4 Filtered Retrieval & Relational SQL View (vw_booking_details)", "10"),
        ("    8.5 Billing & Invoicing Form", "11"),
        ("    8.6 System Health Check Endpoint", "11"),
        ("9. AWS Infrastructure Screenshots", "12"),
        ("    9.1 Amazon EC2 Instance — Running Status", "12"),
        ("    9.2 EC2 Instance Configuration Details", "13"),
        ("    9.3 EC2 Security Group Inbound & Outbound Rules", "13"),
        ("    9.4 Docker Multi-Container Orchestration Status", "14"),
        ("    9.5 MySQL Database Container & BCNF Schema Verification", "14"),
        ("    9.6 Nginx Reverse Proxy & HTTP Port 80 Routing", "15"),
        ("    9.7 Java Backend REST API Execution Logs", "15"),
        ("    9.8 Amazon CloudWatch System Performance Metrics", "16"),
        ("10. Test Cases and Results", "17"),
        ("11. Conclusion", "18"),
        ("12. References", "19")
    ]
    for title, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(title)
        r_t.font.size = Pt(10.5)
        dots_count = max(5, 75 - len(title))
        r_dots = p.add_run(" " + "." * dots_count + " ")
        r_dots.font.color.rgb = RGBColor(0x8C, 0x8C, 0x8C)
        r_p = p.add_run(page)
        r_p.font.bold = True

    doc.add_page_break()

    # ==================== 1. ABSTRACT ====================
    add_h1("1. Abstract")
    doc.add_paragraph(
        "This report details the architectural design, implementation, and cloud deployment of HotelStay, a full-stack, "
        "cloud-native Hotel Management System developed as the DA3 project at Vellore Institute of Technology, Chennai. "
        "The system provides an end-to-end operational platform for hospitality management, covering guest profiling, dynamic "
        "room inventory, reservation lifecycles, and billing settlement. The application is architectured as a multi-tier solution "
        "deployed on an Amazon Elastic Compute Cloud (Amazon EC2) virtual server running Ubuntu Linux in the ap-south-1 (Mumbai) region."
    )
    doc.add_paragraph(
        "The frontend presentation tier is built with React 18 and bundled using Vite, served through a high-performance Nginx web server "
        "acting as a reverse proxy on HTTP port 80. The application tier comprises a custom Java 17 REST API server utilizing raw Java "
        "Database Connectivity (JDBC) with parameterized queries for deterministic, high-throughput execution without enterprise framework overhead. "
        "The persistence tier is powered by MySQL 8.0, adhering strictly to Boyce-Codd Normal Form (BCNF) across 13 relational entities, reinforced with "
        "foreign key referential integrity, domain constraints (CHECK), cascading actions, and relational database views (vw_booking_details)."
    )
    doc.add_paragraph(
        "All tiers are containerized and orchestrated using Docker and Docker Compose. Nginx acts as the single public gateway on port 80, eliminating "
        "Cross-Origin Resource Sharing (CORS) complexity and proxying API traffic internally to the backend. Operational resilience on AWS Free-Tier "
        "compute is ensured through an automated 512MB virtual memory swap configuration and integrated Amazon CloudWatch telemetry monitoring."
    )

    # ==================== 2. INTRODUCTION ====================
    add_h1("2. Introduction")
    doc.add_paragraph(
        "Modern hospitality operations require highly available, resilient, and responsive information systems capable of handling room allocations, "
        "guest registrations, and transactional billing without downtime or data inconsistency. Legacy on-premise hotel management software often suffers "
        "from server maintenance overhead, lack of scalability, vulnerability to localized hardware failures, and high operational expenditure."
    )
    doc.add_paragraph(
        "Cloud computing provides a compelling solution by offering on-demand compute elasticity, automated networking, managed storage, and pay-as-you-go economics. "
        "This project bridges rigorous academic relational database design with modern cloud engineering by deploying an enterprise-grade Hotel Management System "
        "on Amazon Web Services (AWS)."
    )
    doc.add_paragraph(
        "The core database design enforces Boyce-Codd Normal Form (BCNF) normalization to eliminate data insertion, update, and deletion anomalies. "
        "By combining this normalized schema with a lightweight, containerized micro-architecture on Amazon EC2, the system achieves responsive sub-second page rendering, "
        "zero CORS configuration complexity, and cost-effective operation within the AWS Free Tier."
    )

    # ==================== 3. OBJECTIVES AND SCOPE ====================
    add_h1("3. Objectives and Scope")
    objectives = [
        "Relational Schema Rigor: Design and implement a robust 13-table relational schema fully normalized to Boyce-Codd Normal Form (BCNF), complete with primary keys, composite keys, foreign keys with referential actions (CASCADE, SET NULL), CHECK constraints, and optimized SQL Views (vw_booking_details).",
        "High-Performance Application Core: Develop a Java 17 backend utilizing standard HTTP server libraries (com.sun.net.httpserver.HttpServer) and JDBC PreparedStatement to ensure SQL injection immunity and minimal memory footprint.",
        "Responsive Presentation Layer: Construct an interactive Single-Page Application (SPA) using React 18 and modern CSS styling to deliver intuitive workflows for hotel managers and reception staff.",
        "Cloud Infrastructure Deployment: Provision an Amazon EC2 (t3.micro) virtual machine running Ubuntu Linux in the AWS Asia Pacific (Mumbai) region (ap-south-1).",
        "Containerized Multi-Tier Orchestration: Containerize the React frontend, Java backend, and MySQL database using multi-stage Dockerfile definitions and orchestrate their lifecycle via Docker Compose.",
        "Network Security & Reverse Proxying: Configure Nginx on port 80 to serve static client assets and securely proxy /api/* requests to the internal Java backend, eliminating CORS issues and shielding internal microservices from direct public internet exposure.",
        "Cloud Cost & Resource Optimization: Enact a 512MB virtual swap configuration on Ubuntu to ensure smooth compilation and container execution on resource-constrained Free-Tier instances without out-of-memory (OOM) failures.",
        "Cloud Observability: Monitor CPU utilization, network traffic, and system logs through integrated Amazon CloudWatch telemetry and container health checks."
    ]
    for obj in objectives:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        parts = obj.split(":", 1)
        r_bold = p.add_run(parts[0] + ":")
        r_bold.font.bold = True
        p.add_run(parts[1])

    doc.add_page_break()

    # ==================== 4. SYSTEM ARCHITECTURE ====================
    add_h1("4. System Architecture")
    doc.add_paragraph(
        "The application implements a decoupled, three-tier cloud architecture hosted on an Amazon EC2 virtual server (t3.micro). "
        "The architecture separates public-facing presentation components from internal application and database services through container network abstraction and AWS security group firewalls."
    )

    arch_table_data = [
        ("Tier", "Component", "Technology", "Responsibilities & Network Exposure"),
        ("Presentation", "Web Server & Client SPA", "React 18, Vite, Nginx, Alpine", "Serves client SPA on HTTP Port 80; reverse-proxies /api/* requests to backend container; handles gzip compression. Publicly exposed to 0.0.0.0/0."),
        ("Application", "REST API Microservice", "Java 17 (Corretto/Temurin), JDBC, Gson", "Executes business logic and JDBC queries; bound to host port 8080 for direct container diagnostics, but shielded from external internet ingress by the AWS Security Group."),
        ("Persistence", "Relational Database", "MySQL 8.0, InnoDB, utf8mb4", "Maintains transactional ACID guarantees; enforces BCNF relations, views, and indexes. Bound exclusively to 127.0.0.1 (loopback), completely inaccessible to public internet."),
        ("Infrastructure", "Compute & Host", "AWS EC2 (t3.micro), Ubuntu 24.04 LTS", "Virtual server host; provides Linux kernel namespaces; maintains 512MB swap space; enforces AWS Security Group firewall perimeter.")
    ]
    t_arch = doc.add_table(rows=len(arch_table_data), cols=4)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_arch, "D3D3D3")
    for r_idx, row in enumerate(arch_table_data):
        for c_idx, val in enumerate(row):
            cell = t_arch.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            if r_idx == 0:
                set_cell_background(cell, "1F4E79")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
                p.runs[0].font.size = Pt(9.5)

    doc.add_paragraph()
    doc.add_paragraph(
        "Network Ingress & Defense-in-Depth Model:\n"
        "1. External traffic enters exclusively through standard HTTP Port 80 managed by Nginx.\n"
        "2. The Nginx reverse proxy routes client requests for / to the compiled static assets and proxies /api/* requests internally to the Java backend (hotel_backend:8080) over the Docker bridge network (app_default).\n"
        "3. While host port 8080 is published for developer diagnosis on the EC2 machine, the external AWS Security Group (launch-wizard-1) does not permit port 8080 inbound from the internet, ensuring defense-in-depth.\n"
        "4. MySQL is bound strictly to the host loopback interface (127.0.0.1:3306), ensuring that external network packets cannot reach the persistence layer directly."
    )

    # ==================== 5. AWS SERVICES USED ====================
    add_h1("5. AWS Services & Infrastructure Components Used")
    aws_table_data = [
        ("AWS / Cloud Service", "Resource Identifier / Type", "Purpose & Architecture Role"),
        ("Amazon EC2", "t3.micro (Ubuntu 24.04 LTS)", "Provides scalable virtual compute host for running containerized services within the AWS Free Tier (ap-south-1)."),
        ("Amazon VPC", "Default VPC (ap-south-1)", "Provides logical network isolation, public subnets (subnet-0ccec48796ac7db5d), and internet gateway routing."),
        ("Security Groups", "launch-wizard-1 (sg-05c58f0544aeeeb4d)", "Stateful virtual firewall: permits inbound HTTP (Port 80) and SSH (Port 22); includes inherited Port 1433 rule from initial launch template."),
        ("Amazon EBS", "8 GiB General Purpose SSD (gp3)", "Provides persistent block-level root storage for the OS, container images, and MySQL database named volume (db_data)."),
        ("Amazon CloudWatch", "EC2 Console Monitoring (AWS/EC2)", "Integrated telemetry tracking CPU utilization (%), network in/out throughput, packet counts, and T3 CPU burst credit consumption."),
        ("Docker Engine", "Docker Community Edition v27+", "Provides lightweight, isolated runtime environments for the frontend, backend, and database containers."),
        ("Docker Compose", "Compose Specification (V2)", "Orchestrates multi-container networking, dependencies, persistent volume mounting, and container health checks."),
        ("Linux Swap Space", "512 MiB Virtual Swap (/swapfile)", "Augments physical RAM of Free-Tier EC2 instance, preventing Out-Of-Memory (OOM) build failures.")
    ]
    t_aws = doc.add_table(rows=len(aws_table_data), cols=3)
    t_aws.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_aws, "D3D3D3")
    for r_idx, row in enumerate(aws_table_data):
        for c_idx, val in enumerate(row):
            cell = t_aws.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            if r_idx == 0:
                set_cell_background(cell, "1F4E79")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
                p.runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # ==================== 6. DATABASE SCHEMA & BCNF ====================
    add_h1("6. Database Schema & BCNF Normalization")
    doc.add_paragraph(
        "The persistence tier is built upon a rigorously structured 13-table relational schema designed to satisfy Boyce-Codd Normal Form (BCNF). "
        "A relation R is in BCNF if and only if for every non-trivial functional dependency X -> Y, X is a superkey of R. "
        "This design systematically eliminates insertion, update, and deletion anomalies."
    )
    bcnf_data = [
        ("#", "Relation Name", "Attributes", "Key Functional Dependencies & Role"),
        ("1", "ZipCode", "Pin_no, City, State", "Pin_no -> City, State (BCNF decomposition eliminating transitive dependency from Employee)"),
        ("2", "Guest", "G_ID, First_Name, Last_Name, DOB, Gender, Mob_No", "G_ID -> All attributes; Candidate Key: Mob_No -> G_ID (both superkeys)"),
        ("3", "Employee", "E_ID, First_Name, Last_Name, Salary, Sex, Mob_No, Pin_no", "E_ID -> All attributes; Foreign Key to ZipCode(Pin_no)"),
        ("4", "Room", "R_ID, Room_No, Type, Capacity, Price_Per_Night, Status", "R_ID -> All attributes; Status CHECK (Available, Occupied)"),
        ("5", "Manager", "E_ID, Dept_Managed, Allowance", "E_ID -> Dept_Managed, Allowance; 1:1 Specialization FK to Employee"),
        ("6", "Housekeeper", "E_ID, Shift, Overtime_Hours", "E_ID -> Shift, Overtime_Hours; 1:1 Specialization FK to Employee"),
        ("7", "Receptionist", "E_ID, Counter_No, Languages", "E_ID -> Counter_No, Languages; 1:1 Specialization FK to Employee"),
        ("8", "Booking_Record", "Booking_ID, Check_In, Check_Out, Total_Amount, G_ID, R_ID, Booking_Type, Status", "Booking_ID -> All; FK to Guest(G_ID) and Room(R_ID); temporal amount snapshot"),
        ("9", "Bill", "B_ID, Amount, Payment_Method, Payment_Date, Status, Booking_ID", "B_ID -> All; FK to Booking_Record(Booking_ID); Status: Unpaid/Paid"),
        ("10", "Records", "Record_no, Type, Date_Logged, Description", "Record_no -> All; Operational audit logging entity"),
        ("11", "Housekeeper_Room", "E_ID, R_ID", "(E_ID, R_ID) -> All; M:N relationship junction table"),
        ("12", "Guest_Manager", "G_ID, E_ID", "(G_ID, E_ID) -> All; VIP guest executive assignment junction table"),
        ("13", "Receptionist_Records", "E_ID, Record_no", "(E_ID, Record_no) -> All; Audit trail junction table")
    ]
    t_bcnf = doc.add_table(rows=len(bcnf_data), cols=4)
    t_bcnf.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_bcnf, "D3D3D3")
    for r_idx, row in enumerate(bcnf_data):
        for c_idx, val in enumerate(row):
            cell = t_bcnf.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            if r_idx == 0:
                set_cell_background(cell, "1F4E79")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
                p.runs[0].font.size = Pt(9.5)

    doc.add_paragraph()
    add_h2("BCNF Decomposition & Functional Dependency Analysis")
    doc.add_paragraph(
        "1. Elimination of Transitive Dependencies via ZipCode: In standard staff management tables, storing City and State alongside Employee would introduce the dependency "
        "E_ID -> Pin_no and Pin_no -> City, State, violating BCNF because Pin_no is not a superkey of Employee. By decomposing this into a dedicated ZipCode(Pin_no, City, State) "
        "relation where Pin_no is the primary key (and superkey), the schema satisfies BCNF.\n\n"
        "2. Justification of Total_Amount in Booking_Record (Temporal Immutability): Relational purity might suggest that Total_Amount is a derived attribute "
        "(Price_Per_Night * Nights). However, in enterprise hospitality management, storing Total_Amount upon booking creation is a deliberate, standardized temporal snapshot pattern. "
        "Hotel room tariffs (Price_Per_Night in Room) change frequently due to seasonality, promotions, and inflation. If Total_Amount were dynamically derived from the current Room table, "
        "any tariff update would retroactively alter past financial receipts, violating accounting integrity. Under temporal functional dependencies, Total_Amount is determined uniquely by "
        "the booking transaction at that specific point in time: Booking_ID -> Total_Amount. Since Booking_ID is the candidate key and superkey, BCNF is strictly preserved.\n\n"
        "3. Single-Inheritance Specialization: Role tables (Manager, Housekeeper, Receptionist) share primary key E_ID with Employee. The functional dependency E_ID -> attributes holds with "
        "E_ID being the unique primary key, adhering to BCNF.\n\n"
        "4. Junction Relations: Tables Housekeeper_Room, Guest_Manager, and Receptionist_Records possess composite keys with no non-key attributes or dependencies other than the full key, "
        "satisfying BCNF trivially."
    )

    doc.add_page_break()

    # ==================== 7. APPLICATION FEATURES ====================
    add_h1("7. Application Features")
    features = [
        "7.1 Real-Time System Status & Header: Operator identification (Pranav Jahagirdar • Reception) and live health badge (DB: UP) dynamically reflecting MySQL connectivity over JDBC.",
        "7.2 Guest Registration & Contact Validation: Form module supporting guest insertion with format constraints for 10–15 digit contact numbers, date of birth, and gender.",
        "7.3 Room Inventory Management: Room creation form supporting room types (Single, Double, Deluxe, Suite), capacity specification, nightly tariffs, and initial availability.",
        "7.4 Reservation & Booking Allocation: Form module linking registered guests and rooms with booking types (Walk-in, Online, Phone, Agent) and reservation statuses (Confirmed, Checked-in, Pending).",
        "7.5 Billing & Invoicing Settlement: Add Bill form linking financial settlement to guests and active bookings with amount input and status tracking (Unpaid / Paid).",
        "7.6 Multi-Table Filtered Retrieval: Interactive search tab executing multi-criteria WHERE queries against the vw_booking_details SQL view, supporting arrival date, room type, booking type, and status filtering with live SQL syntax display.",
        "7.7 Diagnostic Health Endpoint: Dedicated /api/health endpoint verifying live JDBC database pool connectivity and reporting HTTP 200 JSON payload."
    ]
    for feat in features:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        parts = feat.split(":", 1)
        r_b = p.add_run(parts[0] + ":")
        r_b.font.bold = True
        p.add_run(parts[1])

    doc.add_page_break()

    # ==================== 8. IMPLEMENTATION DETAILS ====================
    add_h1("8. Implementation Details & Demonstration Screenshots")

    add_h2("8.1 Application Header & Live Health Status")
    doc.add_paragraph(
        "The application header displays the operator identity, active role, and live MySQL database connectivity status (DB: UP). "
        "The navigation bar provides one-click switching between transactional data entry ('1. Enter Details') and multi-table filtered retrieval ('2. Retrieve / Search')."
    )
    add_figure("images/figure_8_2_guests.png", "Figure 8.1 — Application Header & Navigation: Operator details (Pranav Jahagirdar • Reception) and live health indicator (DB: UP).")

    add_h2("8.2 Guest & Room Management (Enter Details View)")
    doc.add_paragraph(
        "The Guest and Room management interface provides transactional forms to insert new entities into the normalized BCNF schema. "
        "The UI validates guest contact numbers and assigns room capacities and tariffs via raw JDBC PreparedStatements."
    )
    add_figure("images/figure_8_2_guests.png", "Figure 8.2 — Data Entry Module: Transactional forms for Guest, Room, and Booking insertion into MySQL with active DB status indicator (DB: UP).")

    add_h2("8.3 Room & Booking Allocation Form")
    doc.add_paragraph(
        "The Room and Booking forms allow front-desk receptionists to allocate available rooms to registered guests, specify booking channels "
        "(Walk-in, Online, Phone, Agent), and set initial reservation status."
    )
    add_figure("images/figure_8_5_bills_bookings.png", "Figure 8.3 — Room Inventory & Reservation Forms: Dynamic room type selection and booking creation cards.")

    add_h2("8.4 Filtered Retrieval & Relational SQL View (vw_booking_details)")
    doc.add_paragraph(
        "The Retrieve / Search view executes real-time multi-criteria filtering against the vw_booking_details SQL view. "
        "It displays the live SQL query preview (SELECT * FROM vw_booking_details;) and renders joined guest names, contact numbers, room numbers, and reservation schedules."
    )
    add_figure("images/figure_8_4_retrieve_search.png", "Figure 8.4 — Relational View Query: Live execution of vw_booking_details with multi-field WHERE filter and joined results table.")

    add_h2("8.5 Billing & Invoicing Form")
    doc.add_paragraph(
        "The Billing module enables front-desk staff to generate invoices linked via foreign key to registered guests and active bookings, "
        "specifying billing amounts and tracking payment status (Unpaid / Paid)."
    )
    add_figure("images/figure_8_5_bills_bookings.png", "Figure 8.5 — Billing Management: Add Bill form linking payments to guest and booking entities with Unpaid status.")

    add_h2("8.6 System Health Check Endpoint")
    doc.add_paragraph(
        "The diagnostic API endpoint (/api/health) verifies live end-to-end database connectivity through the Nginx reverse proxy, returning a JSON payload confirming status: UP "
        "and the target database hotel_management."
    )
    add_figure("images/figure_8_6_health_check.png", "Figure 8.6 — Health Check Verification: JSON response from the Java backend confirming active MySQL connection over Port 80 via Nginx reverse proxy.")

    doc.add_page_break()

    # ==================== 9. AWS INFRASTRUCTURE SCREENSHOTS ====================
    add_h1("9. AWS Infrastructure Screenshots")

    add_h2("9.1 Amazon EC2 Instance — Running Status")
    doc.add_paragraph(
        "The EC2 console demonstrates that the Ubuntu virtual instance (Instance ID: i-0601e61a67c089561, Name: hotel-management-server) is active "
        "in the Running state with status checks Initializing (captured during the initial instance boot sequence prior to 2/2 checks completion), "
        "assigned a public IPv4 address (15.206.165.236), and residing in the ap-south-1b Availability Zone."
    )
    add_figure("images/figure_9_1_ec2_running.png", "Figure 9.1 — Amazon EC2 Management Console: Virtual server (t3.micro, i-0601e61a67c089561) in Running state (Status check: Initializing) with public IP 15.206.165.236.")

    add_h2("9.2 EC2 Instance Configuration Details")
    doc.add_paragraph(
        "The configuration panel reveals the architectural specifications of the compute instance: Amazon Machine Image (Ubuntu 24.04 LTS), "
        "virtual private cloud (VPC) ID vpc-03654105d1079a2d5, public subnet allocation subnet-0ccec48796ac7db5d, and assigned public IPv4 address 15.206.165.236."
    )
    add_figure("images/figure_9_2_ec2_details.png", "Figure 9.2 — EC2 Configuration Summary: Subnet, VPC ID, Private IP (172.31.10.113), and Public IPv4 address.")

    add_h2("9.3 EC2 Security Group Inbound & Outbound Rules")
    doc.add_paragraph(
        "The Security Group (launch-wizard-1, sg-05c58f0544aeeeb4d) acts as an enterprise firewall controlling ingress traffic to the host. "
        "As shown in Figure 9.3, the inbound rules specify:\n"
        "• HTTP (TCP Port 80, 0.0.0.0/0): Allows public web traffic to reach the Nginx reverse proxy.\n"
        "• SSH (TCP Port 22, 0.0.0.0/0): Allows administrative console access via EC2 Instance Connect.\n"
        "• MS SQL (TCP Port 1433, 0.0.0.0/0): An inactive firewall rule carried over from the initial launch wizard template selection before the Ubuntu AMI was finalized. "
        "Because no SQL Server process listens on port 1433, this rule represents an inert firewall entry that can be pruned in production hardening.\n"
        "Crucially, host ports 8080 (backend) and 3306 (MySQL) are completely omitted from the Security Group inbound rules, ensuring that public internet clients "
        "cannot directly connect to the backend or database microservices."
    )
    add_figure("images/figure_9_3_security_group.png", "Figure 9.3 — Security Group Configuration: Inbound firewall rules showing HTTP (Port 80), SSH (Port 22), and template-inherited MS SQL (Port 1433).")

    add_h2("9.4 Docker Multi-Container Orchestration Status")
    doc.add_paragraph(
        "Executing sudo docker compose ps within the EC2 terminal verifies that all three container services are active and healthy:\n"
        "• hotel_frontend: Nginx web server bound to host port 80 (0.0.0.0:80->80/tcp).\n"
        "• hotel_backend: Java 17 REST API bound to host port 8080 (0.0.0.0:8080->8080/tcp) for local host diagnostics, shielded from the public internet by the Security Group.\n"
        "• hotel_db: MySQL 8.0 bound strictly to host loopback (127.0.0.1:3306->3306/tcp, healthy), completely preventing external remote connections."
    )
    add_figure("images/figure_9_4_docker_ps.png", "Figure 9.4 — Docker Multi-Container Status: Active containers for Nginx (Port 80), Java backend (Port 8080), and MySQL 8.0 (127.0.0.1:3306, healthy).")

    add_h2("9.5 MySQL Database Container & BCNF Schema Verification")
    doc.add_paragraph(
        "Terminal execution inside the MySQL container showing the result of SHOW TABLES; and verification of all 13 BCNF tables and 2 SQL views within the hotel_management database schema.\n\n"
        "Security Note on Development Credentials: In Figure 9.5, the parameter -prootpassword123 is supplied directly in the CLI command for immediate schema verification during testing. "
        "In an enterprise cloud production environment, best practices dictate abstracting credentials using AWS Secrets Manager or AWS Systems Manager Parameter Store, "
        "injecting credentials dynamically at runtime via IAM roles rather than passing them on the command line."
    )
    add_figure("images/figure_9_5_mysql_tables.png", "Figure 9.5 — MySQL Schema Verification: Terminal execution confirming all 13 BCNF relational tables and 2 SQL views in hotel_management.")

    add_h2("9.6 Nginx Reverse Proxy & HTTP Port 80 Routing")
    doc.add_paragraph(
        "Demonstrates external HTTP access to the application via the EC2 Public IPv4 address in a browser without any port number (standard port 80), "
        "proving that Nginx is successfully routing requests."
    )
    add_figure("images/figure_9_6_public_url.png", "Figure 9.6 — Public Cloud Access: Hotel management web application loading seamlessly over the EC2 public IPv4 address (http://15.206.165.236/) on standard HTTP Port 80.")

    add_h2("9.7 Java Backend REST API Execution Logs")
    doc.add_paragraph(
        "Terminal output of sudo docker compose logs --tail=25 backend showing the Java 17 application boot sequence, dynamic environment variable loading (DB_URL, PORT), "
        "and successful database handshake (✓ DB connection OK) followed by HTTP endpoint registration."
    )
    add_figure("images/figure_9_7_backend_logs.png", "Figure 9.7 — Backend Runtime Logs: Java 17 API startup, successful database connection (✓ DB connection OK), and route registration.")

    add_h2("9.8 Amazon CloudWatch System Performance Metrics")
    doc.add_paragraph(
        "Figure 9.8 displays the Amazon EC2 integrated Monitoring dashboard, which captures real-time Amazon CloudWatch basic telemetry metrics for the hotel-management-server instance over a 1-hour window. The graphs illustrate:\n"
        "• CPU utilization (%): Operational peaks up to 21.23% during Docker image unpacking and build phases, stabilizing near ~0% at idle.\n"
        "• Network in (bytes): Ingress throughput peaking at 162.4 MB during base container image downloads (MySQL, Corretto, Alpine) and npm package resolution.\n"
        "• Network out (bytes): Egress throughput peaking at 916.5 KB during client HTTP web asset delivery.\n"
        "• Network packets in (count): Telemetry peaking at ~110.65K packets during build and package installation.\n"
        "• Network packets out (count): Telemetry peaking at ~3.81K packets for outbound HTTP responses.\n"
        "• CPU credit usage and CPU credit balance (count): Burstable T3 credit balance maintained at ~0.72 credits with credit usage peaking at 2.15 credits."
    )
    add_figure("images/figure_9_8_cloudwatch_metrics.png", "Figure 9.8 — EC2 Integrated CloudWatch Telemetry: Real-time CPU utilization (peak 21.23%), network ingress/egress bytes, packet counts, and T3 CPU credit telemetry.")

    doc.add_page_break()

    # ==================== 10. TEST CASES ====================
    add_h1("10. Test Cases and Results")
    test_cases_data = [
        ("Test ID", "Module", "Test Scenario & Inputs", "Expected Result", "Actual Result & Photographic Evidence", "Status"),
        ("TC-01", "Guest Registration", "Submit Add Guest form with First Name, Last Name, DOB, Gender, and 10-digit mobile.", "Guest inserted into MySQL; auto G_ID assigned; UI refreshes.", "Record created; visible in database and results view. (Verified in Figure 8.2 & 8.4)", "PASS"),
        ("TC-02", "Guest Validation", "Attempt to register guest with invalid mobile (less than 10 digits).", "HTML5 regex constraint pattern prevents form submission.", "Submission blocked by browser validation; no DB write occurred. (Verified in UI form constraints)", "PASS"),
        ("TC-03", "Room Inventory", "Submit Add Room form with Type: Single, Capacity: 1, Price: 1500, Availability: Available.", "Room entity inserted into Room table; initial availability set.", "Room saved successfully; ready for reservation allocation. (Verified in Figure 8.2)", "PASS"),
        ("TC-04", "Booking Allocation", "Create booking linking registered Guest and Room with Walk-in type and Confirmed status.", "Booking_Record inserted with temporal amount snapshot; linked via FK.", "Booking created successfully; visible in Retrieve / Search table. (Verified in Figure 8.2 & 8.4)", "PASS"),
        ("TC-05", "Relational View Query", "Execute search on '2. Retrieve / Search' tab against vw_booking_details with filter criteria.", "Unified JSON records returned joining Guest, Room, Dates, and Status.", "View queried live; results table renders joined records with SQL preview. (Verified in Figure 8.4)", "PASS"),
        ("TC-06", "Billing Settlement", "Submit Add Bill form linking Guest and active Booking with Amount and Status: Unpaid.", "Invoice record inserted into Bill table with foreign key linkage.", "Bill saved successfully with Unpaid status; linked to guest. (Verified in Figure 8.5)", "PASS"),
        ("TC-07", "Diagnostic Health", "Send HTTP GET request to /api/health over public IP on Port 80.", "JSON response returned: {\"status\":\"UP\",\"db\":\"hotel_management\"}.", "HTTP 200 OK received with UP status confirming JDBC database pool. (Verified in Figure 8.6)", "PASS"),
        ("TC-08", "Nginx Reverse Proxy", "Access web application via public IPv4 (http://15.206.165.236/) without port specification.", "Nginx routes port 80 to React frontend and proxies /api/* internally.", "Web application loads seamlessly; live health status shows DB: UP. (Verified in Figure 9.6)", "PASS"),
        ("TC-09", "Container Orchestration", "Execute sudo docker compose ps on EC2 host to verify container health.", "Frontend, backend, and db containers active with db reported healthy.", "All 3 containers active; db healthy; ports mapped correctly. (Verified in Figure 9.4)", "PASS"),
        ("TC-10", "Schema Verification", "Execute SHOW TABLES; inside MySQL container via Docker CLI.", "13 BCNF relational tables and 2 SQL views listed in hotel_management schema.", "All 13 tables and 2 views verified present and correctly named. (Verified in Figure 9.5)", "PASS"),
        ("TC-11", "Backend Boot & Logs", "Inspect backend runtime output via sudo docker compose logs backend.", "Java 17 HTTP server boots on port 8080; DB connection established.", "Logs confirm startup and '✓ DB connection OK' message. (Verified in Figure 9.7)", "PASS"),
        ("TC-12", "Host Telemetry", "Monitor compute and network metrics in EC2 Console integrated CloudWatch monitoring.", "Telemetry shows CPU utilization peak at 21.23% and network ingress of 162.4MB.", "Metrics captured in CloudWatch graphs confirming stable resource utilization. (Verified in Figure 9.8)", "PASS")
    ]
    t_tc = doc.add_table(rows=len(test_cases_data), cols=6)
    t_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tc, "D3D3D3")
    for r_idx, row in enumerate(test_cases_data):
        for c_idx, val in enumerate(row):
            cell = t_tc.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            if r_idx == 0:
                set_cell_background(cell, "1F4E79")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
                p.runs[0].font.size = Pt(8.5)
                if val == "PASS":
                    p.runs[0].font.bold = True
                    p.runs[0].font.color.rgb = RGBColor(0x1E, 0x7E, 0x34)

    # ==================== 11. CONCLUSION ====================
    add_h1("11. Conclusion")
    doc.add_paragraph(
        "The HotelStay Hotel Management System successfully proves the feasibility and advantages of deploying a BCNF-compliant "
        "relational database and full-stack web application on Amazon Web Services. All foundational project objectives were satisfied:"
    )
    concl_points = [
        "Academic & Architectural Rigor: The database strictly adheres to Boyce-Codd Normal Form (BCNF) across 13 tables, guaranteeing complete referential integrity, eliminating data redundancy, and optimizing read operations via relational SQL views.",
        "Deterministic, Lightweight Compute: By pairing a responsive React 18 SPA with a clean Java 17 JDBC API, the system eliminates bulky enterprise framework overhead, ensuring fast startup times and sub-second response latencies.",
        "Cloud-Native Containerization: Multi-stage Docker packaging and Docker Compose orchestration eliminate environment parity issues, enabling seamless local-to-cloud deployment.",
        "Network & Operational Security: Nginx reverse proxying acts as the public entry point on Port 80, eliminating CORS errors and shielding backend microservices and database ports behind the AWS Security Group firewall.",
        "Cost-Effective Scalability: The entire architecture operates comfortably within the AWS Free Tier, utilizing virtual swap space on Ubuntu to ensure rock-solid stability on modest hardware."
    ]
    for cp in concl_points:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        parts = cp.split(":", 1)
        r_b = p.add_run(parts[0] + ":")
        r_b.font.bold = True
        p.add_run(parts[1])

    # ==================== 12. REFERENCES ====================
    add_h1("12. References")
    refs = [
        "[1] Amazon Web Services, 'Amazon Elastic Compute Cloud (EC2) User Guide for Linux Instances,' AWS Documentation, 2024. [Online]. Available: https://docs.aws.amazon.com/ec2/",
        "[2] Amazon Web Services, 'Amazon Virtual Private Cloud (VPC) User Guide,' AWS Documentation, 2024. [Online]. Available: https://docs.aws.amazon.com/vpc/",
        "[3] Amazon Web Services, 'Amazon CloudWatch User Guide,' AWS Documentation, 2024. [Online]. Available: https://docs.aws.amazon.com/cloudwatch/",
        "[4] Oracle Corporation, 'MySQL 8.0 Reference Manual — Optimization, Views, and InnoDB Storage Engine,' 2024. [Online]. Available: https://dev.mysql.com/doc/refman/8.0/en/",
        "[5] Oracle Corporation, 'Java SE 17 Documentation & JDBC 4.3 Specification,' 2024. [Online]. Available: https://docs.oracle.com/en/java/javase/17/",
        "[6] Nginx Inc., 'Nginx Reverse Proxy & HTTP Load Balancing Documentation,' 2024. [Online]. Available: https://nginx.org/en/docs/http/ngx_http_proxy_module.html",
        "[7] Docker Inc., 'Docker Compose Specification & Multi-Stage Builds,' Docker Docs, 2024. [Online]. Available: https://docs.docker.com/compose/",
        "[8] Meta Platforms, 'React 18 Documentation — Concurrent Rendering and Hooks,' 2024. [Online]. Available: https://react.dev/",
        "[9] A. Silberschatz, H. F. Korth, and S. Sudarshan, Database System Concepts, 7th ed., New York, NY: McGraw-Hill Education, 2020.",
        "[10] R. Elmasri and S. B. Navathe, Fundamentals of Database Systems, 7th ed., Boston, MA: Pearson, 2016."
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r_ref = p.add_run(ref)
        r_ref.font.size = Pt(9.5)

    output_path = "24BCE1503-DA3-HotelManagement_Report.docx"
    doc.save(output_path)
    print(f"Successfully generated: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    create_word_report()
