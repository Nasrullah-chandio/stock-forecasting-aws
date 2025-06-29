# 📊 Stock Forecasting on AWS (Terraform + Python)

This project builds a secure and scalable stock data pipeline using AWS services and Terraform. It supports fetching and storing historical stock data using Python and PostgreSQL on AWS.

---

## 🔧 Infrastructure

- **VPC** with public and private subnets
- **RDS PostgreSQL** (private subnet)
- **EC2 Bastion Host** (public subnet) to run scheduled jobs
- Infrastructure managed using **Terraform**
- Code versioned in **GitHub**

---

## 📈 Data Pipeline

- Python script fetches daily stock data (e.g., AAPL) using **Alpha Vantage**
- Stores data in RDS PostgreSQL (`aapl_prices` table)
- Can be scheduled on EC2 via `cron` or manually executed via SSH

---

## 🔐 Accessing RDS from Mac via SSH Tunnel

1. Open terminal on MacBook
2. Run SSH tunnel (keep terminal open):

```bash
ssh -i ~/.ssh/bastion-key.pem -N -L 5433:10.0.3.198:5432 ec2-user@34.202.236.205
```

3. Open **pgAdmin** and connect using:
   - **Host:** `localhost`
   - **Port:** `5433`
   - **Database:** `stocks`
   - **Username:** `pgadmin`
   - **Password:** `Passw0rd1234!`

---

## 📁 Folder Structure

```
STOCK_AWS_TERRAFORM/
├── stock-forecast-infra/     → Terraform infrastructure code
├── stock-app/                → Python scripts (e.g., fetch_sp500_history.py)
├── README.md                 → Project documentation (this file)
```

---

## ✅ Status

- Infrastructure deployed using Terraform ✅  
- PostgreSQL RDS created and secured ✅  
- EC2 bastion created and connected ✅  
- Python script fetches and inserts stock data ✅  
- Verified using pgAdmin ✅
