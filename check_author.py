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
    print("Подключение к Supabase...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Проверяем таблицу author
    print("\n📊 Таблица author:")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'author'
        ORDER BY ordinal_position
    """)
    
    columns = cursor.fetchall()
    if columns:
        print("  Найдены колонки:")
        for col in columns:
            nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
            print(f"    - {col[0]}: {col[1]} {nullable}")
    else:
        print("  ❌ Таблица не найдена!")
    
    # Пробуем сделать SELECT
    print("\n📝 Проверяем SELECT...")
    cursor.execute("SELECT * FROM author LIMIT 1")
    result = cursor.fetchall()
    print(f"  ✅ SELECT работает! Записей: {len(result)}")
    
    cursor.close()
    conn.close()
    print("\n✅ Всё работает!")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")