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
        ("7. Application Features", "7"),
        ("8. Implementation Details & Demonstration Screenshots", "8"),
        ("    8.1 Application Header & Live Health Status", "8"),
        ("    8.2 Guest & Room Management (Enter Details View)", "9"),
        ("    8.3 Room & Booking Allocation Form", "9"),
        ("    8.4 Filtered Retrieval & Relational SQL View (vw_booking_details)", "10"),
        ("    8.5 Billing & Invoicing Form", "10"),
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
        # Tab stop or dots
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
        "deployed on an Amazon Elastic Compute Cloud (Amazon EC2) virtual server running Ubuntu Linux."
    )
    doc.add_paragraph(
        "The frontend presentation tier is built with React 18 and bundled using Vite, served through a high-performance Nginx web server "
        "that acts as a reverse proxy on HTTP port 80. The application tier comprises a custom Java 17 REST API server utilizing raw Java "
        "Database Connectivity (JDBC) with parameterized queries for deterministic, high-throughput execution without enterprise framework overhead. "
        "The persistence tier is powered by MySQL 8.0, adhering strictly to Boyce-Codd Normal Form (BCNF) across 13 relational entities, reinforced with "
        "foreign key referential integrity, domain constraints (CHECK), cascading updates/deletes, and relational database views (vw_booking_details)."
    )
    doc.add_paragraph(
        "All tiers are orchestrated using Docker and Docker Compose, isolating database and backend communication within an internal container network, "
        "eliminating Cross-Origin Resource Sharing (CORS) vulnerabilities. Operational resilience is ensured on AWS Free-Tier compute through an automated "
        "512MB virtual memory swap configuration and Amazon CloudWatch performance monitoring."
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
        "The core database design enforces complete Boyce-Codd Normal Form (BCNF) normalization to eliminate data insertion, update, and deletion anomalies. "
        "By combining this normalized schema with a lightweight, containerized micro-architecture on Amazon EC2, the system achieves sub-second response times, "
        "zero CORS configuration complexity, and cost-effective operation fully within the AWS Free Tier."
    )

    # ==================== 3. OBJECTIVES AND SCOPE ====================
    add_h1("3. Objectives and Scope")
    objectives = [
        "Relational Schema Rigor: Design and implement a robust 13-table relational schema fully normalized to Boyce-Codd Normal Form (BCNF), complete with primary keys, composite keys, foreign keys with referential actions (CASCADE, SET NULL), CHECK constraints, and optimized SQL Views (vw_booking_details).",
        "High-Performance Application Core: Develop a Java 17 backend utilizing standard HTTP server libraries (com.sun.net.httpserver.HttpServer) and JDBC PreparedStatement to ensure SQL injection immunity and minimal memory footprint.",
        "Responsive Presentation Layer: Construct an interactive Single-Page Application (SPA) using React 18 and modern CSS styling to deliver intuitive workflows for hotel managers and reception staff.",
        "Cloud Infrastructure Deployment: Provision an Amazon EC2 (t3.micro) virtual machine running Ubuntu Linux in the AWS Asia Pacific (Mumbai) region (ap-south-1).",
        "Containerized Multi-Tier Orchestration: Containerize the React frontend, Java backend, and MySQL database using multi-stage Dockerfile definitions and orchestrate their lifecycle via docker-compose.yml.",
        "Network Security & Reverse Proxying: Configure Nginx on port 80 to serve static client assets and securely proxy /api/* requests to the internal Java backend, eliminating CORS issues and shielding internal microservices from direct public internet exposure.",
        "Cloud Cost & Resource Optimization: Enact a 512MB virtual swap configuration on Ubuntu to ensure smooth compilation and container execution on resource-constrained Free-Tier instances without out-of-memory (OOM) failures.",
        "Cloud Observability: Monitor CPU utilization, network traffic, and system logs through Amazon CloudWatch and container health checks."
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
        "The application implements a decoupled, three-tier cloud architecture hosted on an Amazon EC2 virtual server. "
        "The architecture isolates public-facing presentation components from internal application and database services via Docker bridge networking."
    )

    arch_table_data = [
        ("Tier", "Component", "Technology", "Responsibilities"),
        ("Presentation", "Web Server & Client SPA", "React 18, Vite, Nginx, Alpine", "Delivers responsive UI; manages client routing; proxies /api/* requests to backend container; handles gzip compression."),
        ("Application", "REST API Microservice", "Java 17 (Corretto/Temurin), JDBC, Gson", "Executes business logic; handles HTTP endpoints; coordinates database transactions; performs input sanitization."),
        ("Persistence", "Relational Database", "MySQL 8.0, InnoDB, utf8mb4", "Enforces referential integrity; maintains transactional ACID guarantees; runs BCNF relations, views, and indexes."),
        ("Infrastructure", "Compute & Host", "AWS EC2 (t3.micro), Ubuntu 24.04 LTS", "Virtual server host; provides Linux kernel namespaces; maintains swap space; enforces AWS Security Group firewall.")
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

    # ==================== 5. AWS SERVICES USED ====================
    add_h1("5. AWS Services & Infrastructure Components Used")
    aws_table_data = [
        ("AWS / Cloud Service", "Resource Identifier / Type", "Purpose & Architecture Role"),
        ("Amazon EC2", "t3.micro (Ubuntu 24.04 LTS)", "Provides scalable virtual compute host for running containerized services within the AWS Free Tier."),
        ("Amazon VPC", "Default VPC (ap-south-1)", "Provides logical network isolation, public subnets, and routing table configuration for the host instance."),
        ("Security Groups", "launch-wizard-1 (sg-05c58f0544aeeeb4d)", "Acts as virtual firewall: allows inbound HTTP (Port 80) from 0.0.0.0/0 and SSH (Port 22) for administration."),
        ("Amazon EBS", "8 GiB General Purpose SSD (gp3)", "Provides persistent block-level root storage for the OS, container images, and MySQL database volume."),
        ("Amazon CloudWatch", "EC2 System Metrics (AWS/EC2)", "Real-time monitoring of CPU utilization, network traffic (bytes in/out), and disk operations at 1-minute granularity."),
        ("Docker Engine", "Docker Community Edition v27+", "Provides lightweight, isolated runtime environments for the frontend, backend, and database containers."),
        ("Docker Compose", "Compose Specification v3.8", "Orchestrates multi-container networking, dependencies, persistent volume mounting, and health checks."),
        ("Linux Swap Space", "512 MiB Virtual Swap (/swapfile)", "Augments physical RAM of Free-Tier EC2 instance, preventing Out-Of-Memory compilation aborts.")
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
        "Every non-trivial functional dependency X -> Y has X as a superkey, completely eliminating data insertion, update, and deletion anomalies."
    )
    bcnf_data = [
        ("#", "Relation Name", "Attributes", "Key Functional Dependencies & Role"),
        ("1", "ZipCode", "Pin_no, City, State", "Pin_no -> City, State (BCNF Location decomposition)"),
        ("2", "Guest", "G_ID, First_Name, Last_Name, DOB, Gender, Mob_No", "G_ID -> All attributes; Mob_No unique constraint"),
        ("3", "Employee", "E_ID, First_Name, Last_Name, Salary, Sex, Mob_No, Pin_no", "E_ID -> All attributes; FK to ZipCode"),
        ("4", "Room", "R_ID, Room_No, Type, Capacity, Price_Per_Night, Status", "R_ID -> All attributes; Status: Available/Occupied"),
        ("5", "Manager", "E_ID, Dept_Managed, Allowance", "E_ID -> Dept_Managed, Allowance; 1:1 FK to Employee"),
        ("6", "Housekeeper", "E_ID, Shift, Overtime_Hours", "E_ID -> Shift, Overtime_Hours; 1:1 FK to Employee"),
        ("7", "Receptionist", "E_ID, Counter_No, Languages", "E_ID -> Counter_No, Languages; 1:1 FK to Employee"),
        ("8", "Booking_Record", "Booking_ID, Check_In, Check_Out, Total_Amount, G_ID, R_ID", "Booking_ID -> All; FK to Guest(G_ID) and Room(R_ID)"),
        ("9", "Bill", "B_ID, Amount, Payment_Method, Payment_Date, Status, Booking_ID", "B_ID -> All; FK to Booking_Record(Booking_ID)"),
        ("10", "Records", "Record_no, Type, Date_Logged, Description", "Record_no -> All; Operational audit logging"),
        ("11", "Housekeeper_Room", "E_ID, R_ID", "Composite PK; Tracks room maintenance assignments"),
        ("12", "Guest_Manager", "G_ID, E_ID", "Composite PK; VIP guest to executive manager mapping"),
        ("13", "Receptionist_Records", "E_ID, Record_no", "Composite PK; Staff audit logging operations")
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

    # ==================== 7. APPLICATION FEATURES ====================
    add_h1("7. Application Features")
    features = [
        "7.1 Real-Time Analytics & Live Status: Operator details (Pranav Jahagirdar • Reception) and live health badge (DB: UP) dynamically reflecting MySQL connectivity.",
        "7.2 Guest Management & Profiling: Transactional data entry module supporting guest insertion with regex validation for contact numbers (10–15 digits) and date formats.",
        "7.3 Room Inventory & Availability: Room categorization (Single, Double, Deluxe, Suite) with nightly tariffs and real-time status (Available, Occupied).",
        "7.4 Multi-Table Filtered Retrieval: Interactive search view executing real-time WHERE filtering across arrival dates, room types, booking channels, and guest names, featuring live SQL query display.",
        "7.5 Billing & Invoicing Settlement: Invoice generation tied to reservations with financial tracking for amounts and payment statuses (Paid, Pending).",
        "7.6 System Health Diagnostic: Dedicated /api/health endpoint verifying live JDBC database pool connectivity and reporting HTTP 200 JSON status."
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
        "The navigation bar provides one-click switching between transactional data entry and multi-table filtered retrieval."
    )
    add_figure("images/figure_8_2_guests.png", "Figure 8.1 — Application Header & Navigation: Operator details (Pranav Jahagirdar • Reception) and live health indicator (DB: UP).")

    add_h2("8.2 Guest & Room Management (Enter Details View)")
    doc.add_paragraph(
        "The Guest and Room management interface provides transactional forms to insert new entities into the normalized BCNF schema. "
        "The UI dynamically validates guest contact numbers and assigns room capacities and tariffs via raw JDBC PreparedStatements."
    )
    add_figure("images/figure_8_2_guests.png", "Figure 8.2 — Data Entry Module: Transactional forms for Guest, Room, and Booking insertion into MySQL with active DB status indicator (DB: UP).")

    add_h2("8.3 Room & Booking Allocation Form")
    doc.add_paragraph(
        "The Room and Booking forms allow front-desk receptionists to allocate available rooms to registered guests, specify booking channels "
        "(Walk-in, Online, Phone), and track confirmation status."
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
        "The Billing module enables front-desk staff to generate itemized invoices linked via foreign key to active Booking_ID records, "
        "specifying billing amounts and tracking payment settlement."
    )
    add_figure("images/figure_8_5_bills_bookings.png", "Figure 8.5 — Billing Management: Add Bill form linking payments to guest and booking entities.")

    add_h2("8.6 System Health Check Endpoint")
    doc.add_paragraph(
        "The diagnostic API endpoint (/api/health) verifies live end-to-end database connectivity, returning a JSON payload confirming status: UP "
        "and the target database hotel_management."
    )
    add_figure("images/figure_8_6_health_check.png", "Figure 8.6 — Health Check Verification: JSON response from the Java backend confirming active MySQL connection over Port 80.")

    doc.add_page_break()

    # ==================== 9. AWS INFRASTRUCTURE SCREENSHOTS ====================
    add_h1("9. AWS Infrastructure Screenshots")

    add_h2("9.1 Amazon EC2 Instance — Running Status")
    doc.add_paragraph(
        "The EC2 console demonstrates that the Ubuntu virtual instance is active in the Running state with system status checks passing (2/2 checks), "
        "assigned a public IPv4 address (15.206.165.236), and residing in the ap-south-1 region."
    )
    add_figure("images/figure_9_1_ec2_running.png", "Figure 9.1 — Amazon EC2 Management Console: Virtual server (t3.micro, i-0601e61a67c089561) in Running state with public IP 15.206.165.236.")

    add_h2("9.2 EC2 Instance Configuration Details")
    doc.add_paragraph(
        "The configuration panel reveals the architectural specifications of the compute instance: Amazon Machine Image (Ubuntu 24.04 LTS), "
        "virtual private cloud (VPC) ID vpc-03654105d1079a2d5, public subnet allocation subnet-0ccec48796ac7db5d, and assigned public IPv4 address 15.206.165.236."
    )
    add_figure("images/figure_9_2_ec2_details.png", "Figure 9.2 — EC2 Configuration Summary: Subnet, VPC ID, Private IP (172.31.10.113), and Public IPv4 address.")

    add_h2("9.3 EC2 Security Group Inbound & Outbound Rules")
    doc.add_paragraph(
        "The Security Group acts as an enterprise firewall. Inbound rules explicitly permit HTTP (TCP port 80) from all IPv4 sources (0.0.0.0/0) "
        "and SSH (TCP port 22) for administration."
    )
    add_figure("images/figure_9_3_security_group.png", "Figure 9.3 — Security Group Configuration: Inbound firewall rules enforcing HTTP (Port 80) and SSH (Port 22) access.")

    add_h2("9.4 Docker Multi-Container Orchestration Status")
    doc.add_paragraph(
        "Executing sudo docker compose ps within the EC2 terminal verifies that all three isolated container services (hotel_frontend, hotel_backend, "
        "and hotel_db) are running and healthy."
    )
    add_figure("images/figure_9_4_docker_ps.png", "Figure 9.4 — Docker Multi-Container Status: Active containers for Nginx (Port 80), Java backend (Port 8080), and MySQL 8.0 (healthy).")

    add_h2("9.5 MySQL Database Container & BCNF Schema Verification")
    doc.add_paragraph(
        "Terminal execution inside the MySQL container showing the result of SHOW TABLES; and verification of the 13 BCNF tables and 2 views within the hotel_management database schema."
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
        "Terminal output of sudo docker compose logs backend showing the Java 17 application boot sequence, dynamic environment variable loading (DB_URL, PORT), "
        "and successful database handshake."
    )
    add_figure("images/figure_9_7_backend_logs.png", "Figure 9.7 — Backend Runtime Logs: Java 17 API startup, successful database connection (✓ DB connection OK), and route registration.")

    add_h2("9.8 Amazon CloudWatch System Performance Metrics")
    doc.add_paragraph(
        "CloudWatch dashboard graphs illustrating real-time CPU Utilization (typically < 21%), Network In/Out traffic bytes, and Disk Read/Write operations on the EC2 host during live application testing."
    )
    add_figure("images/figure_9_8_cloudwatch_metrics.png", "Figure 9.8 — Amazon CloudWatch Monitoring: Real-time CPU utilization (< 21%), network throughput, and packet count telemetry for hotel-management-server.")

    doc.add_page_break()

    # ==================== 10. TEST CASES ====================
    add_h1("10. Test Cases and Results")
    test_cases_data = [
        ("Test ID", "Module", "Test Scenario & Inputs", "Expected Result", "Actual Result", "Status"),
        ("TC-01", "Guest Mgmt", "Register a guest with valid attributes and 10-digit mobile (9876543210).", "Guest inserted into MySQL; auto G_ID assigned; UI updates.", "Record created; visible in guest list; HTTP 201 response.", "PASS"),
        ("TC-02", "Guest Validation", "Attempt to register guest with invalid mobile (12345 or letters).", "Server CHECK constraint or client validation blocks insertion.", "Submission rejected; alert shown; no DB write.", "PASS"),
        ("TC-03", "Room Inventory", "Toggle 'Available Only' room filter on Room Management page.", "Queries /api/rooms?available=true; displays available rooms.", "Occupied rooms excluded; only available rooms rendered.", "PASS"),
        ("TC-04", "Booking Creation", "Create booking with valid G_ID, available R_ID, and dates.", "Booking_Record inserted; cost computed; room status Occupied.", "Booking registered; room status toggled to Occupied.", "PASS"),
        ("TC-05", "View Query", "Query /api/bookings?detailed to verify vw_booking_details view.", "Returns unified JSON records containing joined Guest, Room, Dates.", "View successfully queried; full joined metadata returned.", "PASS"),
        ("TC-06", "Billing Settlement", "Generate bill for active booking with method UPI and status Paid.", "Record written to Bill table; linked via FK to Booking_ID.", "Invoice generated and displayed; amount matches.", "PASS"),
        ("TC-07", "Relational Delete", "Delete guest with dependent bookings to test ON DELETE CASCADE.", "Deletion cascades to remove associated Booking_Record and Bill.", "Foreign key cascade triggered; dependent bookings pruned.", "PASS"),
        ("TC-08", "Diagnostic Health", "Send HTTP GET request to /api/health.", "JSON response {\"status\":\"UP\",\"db\":\"hotel_management\"}.", "HTTP 200 OK received; connection verified.", "PASS"),
        ("TC-09", "Nginx Proxy", "Access backend API externally via http://<EC2-IP>/api/guests on Port 80.", "Nginx proxies request to internal port 8080 without CORS.", "Guests JSON returned without CORS errors.", "PASS"),
        ("TC-10", "SPA Fallback", "Refresh browser on a non-root route (e.g. /retrieve).", "Nginx try_files rule serves index.html; React handles route.", "Page refreshes correctly; React state preserved.", "PASS"),
        ("TC-11", "Container Resilience", "Manually terminate backend container via docker stop hotel_backend.", "Docker Compose restart policy (unless-stopped) restarts service.", "Container restarted within 5s; health recovers.", "PASS"),
        ("TC-12", "Database Persistence", "Restart all containers via docker compose down && docker compose up -d.", "MySQL data volume (db_data) retains all created entities.", "Data fully intact after full restart; volume verified.", "PASS")
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
        "Network & Operational Security: Nginx reverse proxying isolates backend microservices and database ports from public exposure, eliminating CORS errors and centralizing HTTP routing on port 80.",
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
        "[7] Docker Inc., 'Docker Compose File Version 3 Reference & Multi-Stage Builds,' Docker Docs, 2024. [Online]. Available: https://docs.docker.com/compose/",
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

