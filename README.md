# Stock Forecasting & Data Pipeline on AWS

This project is an end-to-end stock data ingestion and forecasting platform using AWS, Python, and Terraform.

It fetches historical and daily stock market data (S&P 500), stores it in a PostgreSQL RDS database, and provides a Flask-based API + frontend for visualization. Infrastructure is defined using Terraform (planned).

---

## 🚀 Features

- Fetch and update historical S&P 500 stock data via Alpha Vantage API
- Store structured data in AWS PostgreSQL (RDS)
- Secure environment configuration using `.env`
- Flask-based API backend
- HTML/JS/CSS frontend interface
- Modular structure for future integration of anomaly detection or ML models
- Infrastructure-as-Code (Terraform) planned for EC2, RDS, VPC, and Bastion host

---

## 📁 Project Structure

.
├── flask-server/ # Flask API backend
├── stock-app/ # Python scripts for data ingestion
│ ├── fetch_sp500_history.py
│ └── daily_sp500_update.py
├── stock-frontend/ # Static frontend (HTML, JS, CSS)
├── stock-forecast-infra/ # Terraform (infra as code - WIP)
├── .gitignore
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## 🛠️ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Nasrullah-chandio/stock-forecasting-aws.git
cd stock-forecasting-aws
2. Install Python dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Setup .env
Create a .env file in the root directory:

ini
Copy
Edit
DB_HOST=your-db-endpoint
DB_PORT=5432
DB_NAME=stocks
DB_USER=pgadmin
DB_PASSWORD=yourPassword
4. Run Flask app
bash
Copy
Edit
cd flask-server
python app.py
5. Run historical fetch script
bash
Copy
Edit
python stock-app/fetch_sp500_history.py
🔮 Coming Soon
Anomaly detection module using statistical/ML methods

Scheduled daily job (via Airflow or cron)

Full Terraform deployment (EC2, RDS, VPC)

Docker and/or AWS deployment options

📜 License
This project is under the MIT License.