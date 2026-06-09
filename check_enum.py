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
    
    # Проверяем все ENUM типы
    print("\n📋 ENUM типы в базе:")
    cursor.execute("""
        SELECT t.typname as enum_name,
               array_agg(e.enumlabel ORDER BY e.enumsortorder) as values
        FROM pg_type t
        JOIN pg_enum e ON t.oid = e.enumtypid
        GROUP BY t.typname
        ORDER BY t.typname;
    """)
    
    enums = cursor.fetchall()
    if enums:
        for enum in enums:
            print(f"  - {enum[0]}: {enum[1]}")
    else:
        print("  (нет ENUM типов)")
    
    # Проверяем конкретно sex_type
    print("\n🔍 Проверяем sex_type...")
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM pg_type WHERE typname = 'sex_type'
        );
    """)
    exists = cursor.fetchone()[0]
    
    if exists:
        print("  ✅ ENUM sex_type существует!")
    else:
        print("  ❌ ENUM sex_type НЕ создан!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")