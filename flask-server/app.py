from flask import Flask, jsonify, send_from_directory
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder="../stock-frontend/static", template_folder="../stock-frontend")

# Use environment variables for DB connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()


@app.route("/")
def serve_index():
    return send_from_directory("../stock-frontend", "index.html")

@app.route("/api/aapl-data")
def get_aapl_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT date, close FROM aapl_prices ORDER BY date ASC")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = [{"date": row[0].strftime("%Y-%m-%d"), "close": float(row[1])} for row in rows]
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("../stock-frontend/static", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
