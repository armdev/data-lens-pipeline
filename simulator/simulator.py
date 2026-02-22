import psycopg2
import time
import random
import logging

logging.basicConfig(level=logging.INFO)

def run_simulation():
    # Connection logic with retries
    while True:
        try:
            conn = psycopg2.connect(
                host="postgres",
                dbname="main_db",
                user="admin",
                password="production_password",
                connect_timeout=5
            )
            break
        except:
            logging.info("Waiting for Postgres...")
            time.sleep(2)

    cur = conn.cursor()

    # Create the source table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS public.events (
            id SERIAL PRIMARY KEY,
            event_type TEXT,
            value FLOAT8,
            created_at BIGINT
        );
    """)
    conn.commit()

    logging.info("Simulation started. Inserting data...")

    # Data generation loop
    while True:
        event_type = random.choice(['purchase', 'view', 'click', 'login'])
        value = round(random.uniform(1.0, 1000.0), 2)
        # Debezium handles BigInt/Long as epoch milliseconds
        timestamp = int(time.time() * 1000) 
        
        cur.execute(
            "INSERT INTO events (event_type, value, created_at) VALUES (%s, %s, %s)",
            (event_type, value, timestamp)
        )
        conn.commit()
        time.sleep(0.5) # 2 events per second

if __name__ == "__main__":
    run_simulation()
