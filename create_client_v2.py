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
    
 
    
    # 2. Проверяем, существует ли таблица
    print("\n2️⃣ Проверяем таблицу client...")
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'client'
        );
    """)
    exists = cursor.fetchone()[0]
    
    if exists:
        print("   ⚠️  Таблица уже существует!")
    else:
        print("   Создаём таблицу...")
        cursor.execute("""
            CREATE TABLE client (
                client_id SERIAL PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                address VARCHAR(255) NULL,
                phone VARCHAR(15) NULL,
                sex sex_type NOT NULL
            );
        """)
        conn.commit()
        print("   ✅ Таблица client создана!")
    
    # 3. Проверяем результат
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
    
except psycopg2.errors.QueryCanceled:
    print("\n⏱️  Таймаут! Запрос выполнялся слишком долго.")
    print("   Попробуй ещё раз или проверь подключение.")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    conn.rollback()