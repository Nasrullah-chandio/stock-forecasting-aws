import yfinance as yf
import psycopg2

# Connect to RDS
conn = psycopg2.connect(
    host="stock-db.cwftb99aibcq.us-east-1.rds.amazonaws.com",
    dbname="stocks",
    user="pgadmin",
    password="Passw0rd1234!",
    port=5432
)
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS stock_prices (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(10),
        price FLOAT,
        date DATE
    );
""")
conn.commit()

# Fetch historical data
symbol = '^GSPC'
print(f"📈 Fetching historical data for {symbol}...")
data = yf.download(symbol, start="2015-01-01", end="2025-05-21", interval='1d')

inserted = 0
for date, row in data.iterrows():
    cur.execute("""
        INSERT INTO stock_prices (symbol, price, date)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (symbol, row['Close'], date.date()))
    inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ Done. Inserted {inserted} rows into RDS.")
