import psycopg2

conn = psycopg2.connect(
    host="db-postgresql-blr1-03991-do-user-22261195-0.f.db.ondigitalocean.com",
    port=25060,
    dbname="defaultdb",
    user="doadmin",
    password="YOUR_PASSWORD",
    sslmode="require"
)

cursor = conn.cursor()

# ✅ Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS escalation_logs (
    id SERIAL PRIMARY KEY,
    ticket_id TEXT,
    conversation TEXT,
    escalate BOOLEAN,
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
""")

conn.commit()

print("✅ Table 'escalation_logs' created successfully (or already exists)")

conn.close()