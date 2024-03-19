import psycopg2

conn = psycopg2.connect(
    dbname="",
    user="",
    password="",
    host=""
)

cursor = conn.cursor()