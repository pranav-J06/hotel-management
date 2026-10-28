# 📋 Complete AWS Deployment & Screenshot Guide
### Step-by-Step Instructions with Exact Screenshot Checkpoints for Your Report

This guide walks you through the entire deployment process from start to finish. At each step, it tells you **exactly what commands to run**, **where to click**, and **when to take each of the 14 screenshots** required for your project report ([REPORT.html](file:///c:/Users/pranav/Documents/SEM5/DBMS_project/REPORT.html) and [REPORT.md](file:///c:/Users/pranav/Documents/SEM5/DBMS_project/REPORT.md)).

---

## 📌 Master Screenshot Checklist

Print or keep this checklist open to track your progress:

| # | Figure # | What to Capture | Where to Capture | Done? |
| :-: | :--- | :--- | :--- | :-: |
| 1 | **Figure 9.1** | EC2 Instance in **Running** state with Public IPv4 | AWS EC2 Console | [ ] |
| 2 | **Figure 9.2** | EC2 **Details** tab (VPC, Subnet, AMI, Storage) | AWS EC2 Console | [ ] |
| 3 | **Figure 9.3** | Security Group **Inbound Rules** (Port 80 HTTP, Port 22 SSH) | AWS EC2 Console | [ ] |
| 4 | **Figure 9.4** | `docker compose ps` command showing all 3 containers Up | EC2 Browser Terminal | [ ] |
| 5 | **Figure 9.5** | MySQL `SHOW TABLES;` showing 13 BCNF tables & 2 views | EC2 Browser Terminal | [ ] |
| 6 | **Figure 9.7** | Backend logs showing `✓ DB connection OK` | EC2 Browser Terminal | [ ] |
| 7 | **Figure 9.6** | Browser address bar showing `http://<EC2-IP>/` (Port 80) | Web Browser | [ ] |
| 8 | **Figure 8.1** | Application Dashboard with KPI cards & Green UP badge | Web Browser | [ ] |
| 9 | **Figure 8.2** | Guest Management page & registration form | Web Browser | [ ] |
| 10 | **Figure 8.3** | Room Inventory page with "Available Only" filter toggled | Web Browser | [ ] |
| 11 | **Figure 8.4** | Bookings page with Guest/Room dropdowns & booking list | Web Browser | [ ] |
| 12 | **Figure 8.5** | Bills page with invoices, payment modes & amounts | Web Browser | [ ] |
| 13 | **Figure 8.6** | Health check JSON `{"status":"UP","db":"hotel_management"}` | Web Browser | [ ] |
| 14 | **Figure 9.8** | CloudWatch Monitoring graphs (CPU % & Network traffic) | AWS EC2 Console | [ ] |

---

## Phase 1: Push Code to GitHub (Local Computer)

Before creating the cloud server, push your code to your GitHub account:

1. Open PowerShell or Command Prompt in this project folder:
   ```powershell
   git init
   git add .
   git commit -m "Deploy Hotel Management System to AWS"
   git branch -M main
   ```
2. Go to [github.com/new](https://github.com/new) and create a repository named `hotel-management`. Keep it **Public**.
3. Link and push your code:
   ```powershell
   git remote add origin https://github.com/<YOUR_USERNAME>/hotel-management.git
   git push -u origin main
   ```

---

## Phase 2: Launch AWS EC2 Instance & Cloud Console Screenshots

### Step 1: Launch the EC2 Instance
1. Log into your [AWS Management Console](https://console.aws.amazon.com/ec2/home).
2. Ensure your region is set to **Asia Pacific (Mumbai) `ap-south-1`** (or your preferred region) in the top-right corner.
3. Click the orange **"Launch instance"** button.
4. Fill in the following settings:
   * **Name**: `hotel-management-server`
   * **OS Image**: Select **Ubuntu** $\rightarrow$ **Ubuntu Server 22.04 LTS (HVM)** *(Free Tier eligible)*.
   * **Instance type**: Select `t2.micro` (or `t3.micro`) *(Free Tier eligible)*.
   * **Key pair (login)**: Select **"Proceed without a key pair (Not recommended)"** from the dropdown (we will connect directly via the browser!).
   * **Network settings**:
     * ✅ Check **Allow SSH traffic from anywhere (0.0.0.0/0)**
     * ✅ Check **Allow HTTP traffic from the internet (0.0.0.0/0)**
   * **Configure storage**: Leave as **8 GiB gp3** *(Free Tier eligible)*.
5. Click **"Launch instance"** at the bottom right.

---

### 📸 SCREENSHOT 1: Figure 9.1 — EC2 Running Instance
1. Click **"View all instances"** (or go to [EC2 Instances List](https://console.aws.amazon.com/ec2/v2/home#Instances:)).
2. Wait 1–2 minutes until the **Instance state** says **Running** and **Status check** says **2/2 checks passed**.
3. Select your instance by clicking the checkbox next to it.
4. **Take Screenshot now!**
   * *Make sure this shows*: Instance Name, Instance ID, State (`Running`), Instance Type (`t2.micro`), Status Check (`2/2 checks passed`), and Public IPv4 address.
   * *Save as*: `figure_9_1_ec2_running.png`

---

### 📸 SCREENSHOT 2: Figure 9.2 — EC2 Configuration Details
1. With your instance selected, look at the bottom panel and click the **"Details"** tab.
2. Scroll slightly so that **AMI ID (Ubuntu)**, **VPC ID**, **Subnet ID**, **Public IPv4 address**, and **Private IPv4 address** are visible.
3. **Take Screenshot now!**
   * *Save as*: `figure_9_2_ec2_details.png`

---

### 📸 SCREENSHOT 3: Figure 9.3 — Security Group Inbound Firewall Rules
1. In the bottom panel of your instance, click the **"Security"** tab.
2. Under **Security groups**, click on the link of your security group (e.g., `launch-wizard-1` or `hotel-management-sg`).
3. Scroll down to the **"Inbound rules"** tab.
4. **Take Screenshot now!**
   * *Make sure this shows*:
     - Port `80` | Protocol `TCP` | Source `0.0.0.0/0` (HTTP)
     - Port `22` | Protocol `TCP` | Source `0.0.0.0/0` (SSH)
   * *Save as*: `figure_9_3_security_group.png`

---

## Phase 3: Connect via Browser Terminal & Run Deployment

### Step 2: Open Browser SSH Terminal
1. Go back to your [EC2 Instances List](https://console.aws.amazon.com/ec2/v2/home#Instances:).
2. Select your instance and click the **"Connect"** button at the top.
3. Stay on the **"EC2 Instance Connect"** tab and click the orange **"Connect"** button.
4. A black terminal window will open directly in your browser as user `ubuntu`.

### Step 3: Run the 1-Click Deployment Script
In the terminal window, copy and paste this command (replace with your actual GitHub URL) and press **Enter**:

```bash
git clone https://github.com/<YOUR_USERNAME>/hotel-management.git app && cd app && chmod +x setup-ec2.sh && ./setup-ec2.sh
```

**Wait 3–4 minutes.** The script will:
* Configure 2GB swap memory so your free server never runs out of RAM.
* Install Docker and Docker Compose.
* Build the React frontend with Nginx.
* Build the Java backend with Maven.
* Start MySQL and populate all 13 BCNF tables and sample data.

---

### 📸 SCREENSHOT 4: Figure 9.4 — Docker Multi-Container Status
Once the script prints `🎉 DEPLOYMENT COMPLETE!`, type this command in the terminal:

```bash
sudo docker compose ps
```

**Take Screenshot now!**
* *Make sure this shows*:
  * `hotel_frontend` (Status: Up, Ports: `0.0.0.0:80->80/tcp`)
  * `hotel_backend` (Status: Up, Ports: `0.0.0.0:8080->8080/tcp`)
  * `hotel_db` (Status: Up (healthy), Ports: `127.0.0.1:3306->3306/tcp`)
* *Save as*: `figure_9_4_docker_ps.png`

---

### 📸 SCREENSHOT 5: Figure 9.5 — MySQL 13 BCNF Tables & Views
In the terminal, run this command to inspect the database schema:

```bash
sudo docker compose exec db mysql -u root -prootpassword123 hotel_management -e "SHOW TABLES;"
```

**Take Screenshot now!**
* *Make sure this shows*: The list of 13 tables (`Bill`, `Booking_Record`, `Employee`, `Guest`, `Housekeeper`, `Room`, `ZipCode`, etc.) and the 2 views (`vw_booking_details`, `vw_employee_details`).
* *Save as*: `figure_9_5_mysql_tables.png`

---

### 📸 SCREENSHOT 6: Figure 9.7 — Java Backend Runtime Logs
In the terminal, run this command to view the backend startup logs:

```bash
sudo docker compose logs --tail=30 backend
```

**Take Screenshot now!**
* *Make sure this shows*:
  * `✓ DB connection OK`
  * `Hotel Management API running at http://localhost:8080`
  * Registered endpoints: `/api/guests /api/rooms /api/bookings /api/health`
* *Save as*: `figure_9_7_backend_logs.png`

---

## Phase 4: Application UI Screenshots (In Your Web Browser)

Copy the **Public IPv4 address** of your EC2 instance (e.g. `13.233.150.45`). Open a new tab in your web browser.

---

### 📸 SCREENSHOT 7: Figure 9.6 — Public Access over Port 80
Type `http://<YOUR-EC2-PUBLIC-IP>` in the address bar (do NOT type `:8080`, just the plain IP).

**Take Screenshot now!**
* *Make sure this shows*: The browser address bar showing `http://<YOUR-EC2-PUBLIC-IP>/` with the Hotel Management application loading seamlessly over HTTP Port 80.
* *Save as*: `figure_9_6_public_url.png`

---

### 📸 SCREENSHOT 8: Figure 8.1 — Application Dashboard
1. Click on the **Dashboard** tab in the application.
2. **Take Screenshot now!**
   * *Make sure this shows*:
     - Summary KPI cards: **Total Guests**, **Total Rooms**, **Total Bookings**, **Total Revenue**.
     - System Status badge showing green **"UP"** (or Online).
     - Recent booking activity table.
   * *Save as*: `figure_8_1_dashboard.png`

---

### 📸 SCREENSHOT 9: Figure 8.2 — Guest Management Page
1. Click on the **Guests** tab in the navigation bar.
2. Scroll to show the guest directory table with registered guests and their phone numbers.
3. Click the **"Add Guest"** button to open the registration form (or show the form with sample inputs).
4. **Take Screenshot now!**
   * *Save as*: `figure_8_2_guests.png`

---

### 📸 SCREENSHOT 10: Figure 8.3 — Room Inventory & Availability Filter
1. Click on the **Rooms** tab.
2. Toggle the **"Available Only"** checkbox or filter button so only vacant rooms are shown.
3. **Take Screenshot now!**
   * *Make sure this shows*: Room cards or table showing Room No, Room Type (Single/Deluxe/Suite), Tariff/Night, and green "Available" badges.
   * *Save as*: `figure_8_3_rooms.png`

---

### 📸 SCREENSHOT 11: Figure 8.4 — Bookings & Reservation Engine
1. Click on the **Bookings** tab.
2. View the booking form with dynamic Guest and Room dropdown selectors, check-in/out date pickers, and the table of confirmed reservations below.
3. **Take Screenshot now!**
   * *Save as*: `figure_8_4_bookings.png`

---

### 📸 SCREENSHOT 12: Figure 8.5 — Billing & Invoices
1. Click on the **Bills** (or Invoices) tab.
2. **Take Screenshot now!**
   * *Make sure this shows*: Invoice records showing Bill ID, Booking ID, Amount, Payment Method (UPI / Credit Card / Cash), Date, and "Paid" status.
   * *Save as*: `figure_8_5_bills.png`

---

### 📸 SCREENSHOT 13: Figure 8.6 — System Health Check Endpoint
1. In your browser address bar, open:
   `http://<YOUR-EC2-PUBLIC-IP>/api/health`
2. **Take Screenshot now!**
   * *Make sure this shows*: The clean JSON output in the browser:
     ```json
     {"status":"UP","db":"hotel_management"}
     ```
   * *Save as*: `figure_8_6_health_check.png`

---

## Phase 5: CloudWatch Monitoring Screenshot (After Testing)

---

### 📸 SCREENSHOT 14: Figure 9.8 — CloudWatch Metrics & Monitoring
1. Return to the [AWS EC2 Console](https://console.aws.amazon.com/ec2/v2/home#Instances:).
2. Select your `hotel-management-server` instance.
3. In the lower panel, click the **"Monitoring"** tab.
4. You will see 6–8 live performance graphs:
   * **CPU utilization (%)**
   * **Network in (bytes)** / **Network out (bytes)**
   * **Disk read/write ops**
5. **Take Screenshot now!**
   * *Make sure this shows*: The CPU Utilization graph (demonstrating healthy low utilization < 5%) and the Network traffic spikes during your test requests.
   * *Save as*: `figure_9_8_cloudwatch_metrics.png`

---

## Phase 6: Insert Screenshots into Your Report & Generate PDF

Now that you have all 14 images:

1. Open **[REPORT.html](file:///c:/Users/pranav/Documents/SEM5/DBMS_project/REPORT.html)** in **Google Chrome** or **Microsoft Edge**.
2. To replace any placeholder with your image:
   * Open `REPORT.html` in VS Code.
   * Find the corresponding figure placeholder (e.g. `Figure 8.1`).
   * Replace:
     ```html
     <div class="screenshot-box">
       ...
     </div>
     ```
     with:
     ```html
     <div style="text-align: center; margin: 15px 0;">
       <img src="path/to/figure_8_1_dashboard.png" style="max-width: 100%; border: 1px solid #cbd5e1; border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
     </div>
     ```
3. Update your name and registration number on the cover table.
4. Click the blue **"🖨️ Print / Save as PDF"** button at the top (or press **Ctrl + P**):
   * Destination: **Save as PDF**
   * Paper size: **A4**
   * Options: Check **Background graphics**
5. Click **Save** — your official DA3 project report is ready for submission!
