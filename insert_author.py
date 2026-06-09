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
    
    # Вставляем авторов
    authors = [
        ('Стивен Кинг', '1947-09-21'),
        ('Джордж Оруэлл', '1903-06-25'),
        ('Фёдор Достоевский', '1821-11-11'),
    ]
    
    print("Вставляем авторов...")
    for name, birthday in authors:
        cursor.execute("""
            INSERT INTO author (name, birthday)
            VALUES (%s, %s)
            RETURNING author_id;
        """, (name, birthday))
        author_id = cursor.fetchone()[0]
        print(f"  ✅ {name} (ID: {author_id})")
    
    conn.commit()
    
    # Проверяем что вставилось
    print("\n📊 Все авторы в базе:")
    cursor.execute("SELECT * FROM author ORDER BY author_id")
    for row in cursor.fetchall():
        print(f"  {row[0]} | {row[1]} | {row[2]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Готово!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    conn.rollback()