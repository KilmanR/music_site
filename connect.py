import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import sys
sys.stdout.reconfigure(line_buffering=True)

# Загружаем переменные из .env
load_dotenv()

# DB_CONFIG
DB_CONFIG = {
    'host': os.getenv('DB_HOST_sup'),
    'port': os.getenv('DB_PORT_sup', 5432),
    'database': os.getenv('DB_NAME_sup'),
    'user': os.getenv('DB_USER_sup'),
    'password': os.getenv('DB_PASSWORD_sup'),
    'connect_timeout': 10
}

start_time = time.time()

try:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Начало работы...")
    
    # Шаг 1: Подключение
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Подключение к Supabase...")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  User: {DB_CONFIG['user']}")
    
    conn = psycopg2.connect(**DB_CONFIG)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Подключено! ({time.time() - start_time:.2f} сек)")
    
    cursor = conn.cursor()
    
    # Шаг 2: Проверка версии
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Проверка версии PostgreSQL...")
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] PostgreSQL версия: {version[0][:50]}...")
    
    # Шаг 3: Создание таблиц
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Чтение SQL скрипта...")
    sql_file = 'queries/00_create_tables.sql'
    
    if not os.path.exists(sql_file):
        raise FileNotFoundError(f"Файл {sql_file} не найден!")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Выполнение SQL скрипта...")
    print(f"  Размер скрипта: {len(sql_script)} символов")
    
    # Разбиваем на отдельные запросы по ;
    statements = sql_script.split(';')
    success_count = 0
    error_count = 0
    
    for i, stmt in enumerate(statements, 1):
        stmt = stmt.strip()
        # Пропускаем пустые строки и комментарии
        if not stmt or stmt.startswith('--'):
            continue
        
        try:
            print(f"  [{i}] Выполнение...")
            cursor.execute(stmt)
            conn.commit()
            print(f"    ✅ Успешно")
            success_count += 1
        except Exception as stmt_error:
            print(f"    ⚠️  Пропущено: {str(stmt_error)[:100]}")
            conn.rollback()
            error_count += 1
    
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Итого: ✅ {success_count} выполнено, ️ {error_count} пропущено")
    
    # Шаг 4: Показать созданные таблицы
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Проверка созданных таблиц...")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    print(f"  Найдено таблиц: {len(tables)}")
    for table in tables:
        print(f"    - {table[0]}")
    
    # Завершение
    cursor.close()
    conn.close()
    
    total_time = time.time() - start_time
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ✅ Готово! Общее время: {total_time:.2f} сек")
    
except psycopg2.OperationalError as e:
    print(f"\n❌ Ошибка подключения: {e}")
    print("\nПроверь:")
    print("  1. Интернет-соединение")
    print("  2. Правильность данных в .env")
    print("  3. Доступность Supabase")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    print("\nПроверь:")
    print("  1. Наличие файла queries/00_create_tables.sql")
    print("  2. Синтаксис SQL скрипта")
    print("  3. pip install python-dotenv psycopg2-binary")