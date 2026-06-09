import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST_sup'),
    'port': os.getenv('DB_PORT_sup', 5432),
    'database': os.getenv('DB_NAME_sup'),
    'user': os.getenv('DB_USER_sup'),
    'password': os.getenv('DB_PASSWORD_sup'),
    'connect_timeout': 10
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("📊 Авторы из облака:")
    cursor.execute("SELECT * FROM author ORDER BY author_id")
    
    for row in cursor.fetchall():
        print(f"  ID: {row[0]} | {row[1]} | {row[2]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Готово!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")