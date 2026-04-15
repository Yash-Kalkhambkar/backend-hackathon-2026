import psycopg2

conn = psycopg2.connect(
    host="db-postgresql-blr1-03991-do-user-22261195-0.f.db.ondigitalocean.com",
    port=25060,
    dbname="defaultdb",
    user="doadmin",
    password="YOUR_PASSWORD_HERE",
    sslmode="require"
)
cursor = conn.cursor()

# Safely add email column — IF NOT EXISTS means this won't fail if already added
cursor.execute("""
    ALTER TABLE escalation_logs
    ADD COLUMN IF NOT EXISTS email TEXT;
""")

conn.commit()
print("✅ Migration complete — email column added to escalation_logs")
conn.close()