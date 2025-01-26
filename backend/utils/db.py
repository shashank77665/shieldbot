import psycopg2
import os
import json  # Needed for JSON handling

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database using environment variables.

    Returns:
        psycopg2.extensions.connection: A connection object for interacting with the database.

    Raises:
        RuntimeError: If the database connection fails.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "shieldbot_db"),
            user=os.getenv("POSTGRES_USER", "user"),
            password=os.getenv("POSTGRES_PASSWORD", "password"),
            host=os.getenv("DB_HOST", "db"),
            port=os.getenv("DB_PORT", 5432),
        )
        return conn
    except psycopg2.Error as e:
        raise RuntimeError(f"Failed to connect to the database: {e}")

def save_attack_log(attack_type, base_url, details):
    """
    Save attack log details to the database.

    Args:
        attack_type (str): The type of attack (e.g., SQL Injection, XSS).
        base_url (str): The URL that was tested.
        details (dict): Additional details or results of the attack test.

    Raises:
        RuntimeError: If the database operation fails.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO shieldbot_attack_logs (attack_type, base_url, details)
            VALUES (%s, %s, %s)
            """,
            (attack_type, base_url, json.dumps(details)),
        )
        conn.commit()
    except psycopg2.Error as e:
        raise RuntimeError(f"Failed to save attack log to the database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
