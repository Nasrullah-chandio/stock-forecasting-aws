import psycopg2

# 🔐 RDS connection details based on your setup
DB_HOST = "stock-db.cwftb99aibcq.us-east-1.rds.amazonaws.com"  # 🔁 Replace if your actual endpoint is different
DB_PORT = 5432
DB_NAME = "stocks"
DB_USER = "pgadmin"
DB_PASSWORD = "Passw0rd1234!"  # 🚨 This is what you used after correcting invalid special chars

try:
    print("🔌 Connecting to RDS PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cur = conn.cursor()
    
    # ✅ Create a basic table for stock prices
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            price FLOAT NOT NULL,
            date DATE NOT NULL
        );
    """)
    
    conn.commit()
    print("✅ Table 'stock_prices' created successfully.")

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error connecting to RDS or creating table:", e)
