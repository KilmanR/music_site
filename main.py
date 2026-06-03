import os
from dotenv import load_dotenv
import psycopg2

# Загружаем настройки из .env
load_dotenv()

# Подключаемся к PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print("✅ Подключение к music_site успешно!")

cur = conn.cursor()
cur.execute("SELECT * FROM genres;")
rows = cur.fetchall()

print("🎵 Жанры в базе:")
for row in rows:
    print(f"ID: {row[0]} | Название: {row[1]}")

cur.close()
conn.close()