import yfinance as yf
import psycopg2

# RDS connection
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

# Fetch stock data using yfinance
symbols = ['AAPL', 'TSLA', 'NVDA', '^NDX']
for symbol in symbols:
    print(f"📈 Fetching {symbol}...")
    data = yf.download(symbol, start="2024-01-01", end="2024-12-31", interval='1d')

    for date, row in data.iterrows():
        cur.execute("""
            INSERT INTO stock_prices (symbol, price, date)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (symbol, row['Close'], date.date()))

conn.commit()
cur.close()
conn.close()
print("✅ Data inserted successfully.")
