import psycopg2
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variables for DB connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()


# Fetch stock data using Alpha Vantage
ts = TimeSeries(key="YOUR_API_KEY", output_format='pandas')
print("📥 Fetching data from Alpha Vantage...")
data, _ = ts.get_daily(symbol='AAPL', outputsize='compact')  # last ~100 days

data.index = data.index.to_pydatetime()  # ensure index is datetime

inserted = 0
failed = 0

for date, row in data.iterrows():
    try:
        cur.execute("""
            INSERT INTO aapl_prices (date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (date) DO NOTHING
        """, (
            date.date(),
            float(row['1. open']),
            float(row['2. high']),
            float(row['3. low']),
            float(row['4. close']),
            int(row['5. volume'])
        ))
        inserted += cur.rowcount
    except Exception as e:
        print(f"❌ Failed for {date.date()}: {e}")
        failed += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ Insert complete. Inserted: {inserted}, Failed: {failed}")
