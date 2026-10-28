# 🚀 Beginner's Guide: Deploying Hotel Management System to AWS

This guide is designed for complete beginners. You do not need to install complex tools on your Windows computer.

---

## Architecture Overview

Everything runs inside containers using Docker:
* **Frontend**: React + Nginx (Port 80)
* **Backend**: Java 17 + JDBC REST API (Port 8080, internal)
* **Database**: MySQL 8.0 (Internal network, preloaded with all 13 tables & sample data)

---

## Step 1: Push Your Code to GitHub

*(If your project is already on GitHub, skip to Step 2).*

1. Open PowerShell or Command Prompt in this project folder:
   ```powershell
   git init
   git add .
   git commit -m "Prepare project for AWS cloud deployment"
   ```
2. Create a new repository on [GitHub](https://github.com/new) (name it `hotel-management-system`). Keep it **Public** (or Private if you prefer).
3. Link and push your code (replace `<YOUR_GITHUB_URL>` with your repository URL):
   ```powershell
   git branch -M main
   git remote add origin <YOUR_GITHUB_URL>
   git push -u origin main
   ```

---

## Step 2: Create a Free Server on AWS (Lightsail)

We recommend **AWS Lightsail** because it includes a **free 3-month trial**, has an in-browser terminal (no SSH key setup needed), and a simple firewall.

1. Go to the [AWS Lightsail Console](https://lightsail.aws.amazon.com/).
2. Click **Create instance**.
3. Choose the instance location:
   * **Platform**: Select **Linux/Unix**.
   * **Blueprint**: Select **OS Only** ➡️ **Ubuntu 22.04 LTS** (or 24.04 LTS).
4. Choose an instance plan:
   * Select the **$3.50/month (or $5/month)** plan (both include a free trial for the first 90 days).
5. Name your instance (e.g., `hotel-management-server`).
6. Click **Create instance** at the bottom.
7. Wait 1–2 minutes until the instance card status changes to **Running**.

---

## Step 3: Open Port 80 (HTTP) on AWS Firewall

1. Click on the name of your new instance (`hotel-management-server`).
2. Click on the **Networking** tab.
3. Under **IPv4 Firewall**, you will see **SSH (Port 22)** and **HTTP (Port 80)**.
   * If **HTTP (Port 80)** is not listed, click **Add rule**, select **HTTP**, and click **Create**.

---

## Step 4: 1-Click Deployment via Browser Terminal

1. In Lightsail, click the orange terminal icon or **"Connect using SSH"**.
   * A black terminal window will open directly in your web browser.
2. In that terminal window, copy and paste this command (replace `<YOUR_GITHUB_URL>` with your GitHub repo URL):

   ```bash
   git clone <YOUR_GITHUB_URL> app && cd app && chmod +x setup-ec2.sh && ./setup-ec2.sh
   ```

3. Press **Enter**.

### What happens now:
* The script configures 2GB swap space (prevents running out of memory on small instances).
* Automatically installs Docker and Docker Compose.
* Builds the React frontend with Nginx.
* Builds the Java 17 backend with Maven.
* Starts MySQL, loads `schema.sql` (13 tables, views, constraints), and seeds `seed.sql`.
* Takes roughly **3–5 minutes**.

---

## Step 5: View Your Live App!

When the script finishes, it will print:
```
==============================================================================
🎉 DEPLOYMENT COMPLETE!
Your Hotel Management System is live at:
👉 http://<YOUR-SERVER-PUBLIC-IP>
==============================================================================
```

Open `http://<YOUR-SERVER-PUBLIC-IP>` in your browser.
You will see your Hotel Management System dashboard, fully connected to MySQL and ready for demo or grading!

---

## Handy Commands (Cheat Sheet)

If you ever need to inspect or manage your app via the terminal:

* **View running containers:**
  ```bash
  sudo docker compose ps
  ```
* **View backend logs:**
  ```bash
  sudo docker compose logs -f backend
  ```
* **Restart the entire application:**
  ```bash
  sudo docker compose restart
  ```
* **Stop everything:**
  ```bash
  sudo docker compose down
  ```
