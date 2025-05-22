from alpha_vantage.timeseries import TimeSeries
import psycopg2

# Connect to RDS
conn = psycopg2.connect(
    host="10.0.3.198",
    dbname="stocks",
    user="pgadmin",
    password="Passw0rd1234!",
    port=5432
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
ts = TimeSeries(key="YOUR_API_KEY", output_format='pandas')
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
