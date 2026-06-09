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
    
    # Все таблицы
    print("📋 Таблицы в базе:")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    
    if tables:
        for t in tables:
            print(f"  - {t[0]}")
    else:
        print("  (пусто)")
    
    # Если есть author — покажем структуру
    if any(t[0] == 'author' for t in tables):
        print("\n📊 Структура таблицы author:")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'author'
            ORDER BY ordinal_position
        """)
        for col in cursor.fetchall():
            print(f"  {col[0]}: {col[1]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Готово!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")