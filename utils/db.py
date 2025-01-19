import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "shieldbot_db"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", 5432),
    )
    return conn

def save_attack_log(attack_type, base_url, details):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO attack_logs (attack_type, base_url, details)
        VALUES (%s, %s, %s)
        """,
        (attack_type, base_url, json.dumps(details)),
    )
    conn.commit()
    cursor.close()
    conn.close()
