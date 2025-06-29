from alpha_vantage.timeseries import TimeSeries
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to RDS using values from .env
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS aapl_prices (
        date DATE PRIMARY KEY,
        open NUMERIC,
        high NUMERIC,
        low NUMERIC,
        close NUMERIC,
        volume BIGINT
    )
""")
conn.commit()

# Fetch data from Alpha Vantage
ts = TimeSeries(key="6DPS4R2VJXY5ZOWE", output_format='pandas')
data, meta = ts.get_daily(symbol='AAPL', outputsize='full')

# Insert into DB
for date, row in data.iterrows():
    cur.execute("""
        INSERT INTO aapl_prices (date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO NOTHING
    """, (date.date(), row['1. open'], row['2. high'], row['3. low'], row['4. close'], int(row['5. volume'])))

conn.commit()
cur.close()
conn.close()

print("✅ Done. AAPL data inserted.")
