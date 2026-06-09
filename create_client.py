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
    

    
    # 2. Создаём таблицу client
    print("\n2️⃣ Создаём таблицу client...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS client (
            client_id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            address VARCHAR(255) NULL,
            phone VARCHAR(15) NULL,
            sex sex_type NOT NULL
        );
    """)
    conn.commit()
    print("   ✅ Таблица client создана!")
    
    # 3. Проверяем
    print("\n📊 Проверяем таблицу client...")
    cursor.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'client'
        ORDER BY ordinal_position
    """)
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[0]}: {col[1]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Готово!")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    conn.rollback()