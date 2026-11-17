import os
import time
from flask import Flask, jsonify
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "soa_db"),
    "user": os.getenv("DB_USER", "soa_user"),
    "password": os.getenv("DB_PASSWORD", "soa_password"),
}

def get_connection():
    # Retry briefly while the database becomes ready.
    last_error = None
    for attempt in range(10):
        try:
            return psycopg.connect(**DB_CONFIG, row_factory=dict_row)
        except psycopg.OperationalError as exc:
            last_error = exc
            time.sleep(2)
    raise last_error

def initialize_database():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    message TEXT NOT NULL
                )
            """)
            cur.execute("SELECT COUNT(*) AS total FROM messages")
            if cur.fetchone()["total"] == 0:
                cur.execute(
                    "INSERT INTO messages (message) VALUES (%s)",
                    ("Hello from the PostgreSQL database!",)
                )

@app.get("/")
def home():
    return jsonify({
        "project": "Docker Compose Multi-Container Microservice",
        "message": "Application service is running",
        "test_endpoint": "/api/data"
    })

@app.get("/health")
def health():
    return jsonify({"status": "UP"}), 200

@app.get("/api/data")
def get_data():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, message FROM messages ORDER BY id")
                rows = cur.fetchall()
        return jsonify({
            "status": "success",
            "database": "connected",
            "records": rows
        }), 200
    except Exception as exc:
        app.logger.exception("Database request failed")
        return jsonify({
            "status": "error",
            "database": "not connected",
            "details": str(exc)
        }), 500

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=8000)
