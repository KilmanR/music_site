import os
import time
import pygame
from dotenv import load_dotenv
import psycopg2

# Загружаем настройки
load_dotenv()

def play_audio_file(file_path):
    """Воспроизводит аудио через pygame (универсально для Win/Linux/Mac)"""
    
    # Проверяем файл
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return False
    
    print(f"🎵 Воспроизвожу: {file_path}")
    
    try:
        # Инициализируем только микшер (звук), без графики
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        print("▶️ Играет... (нажми Ctrl+C для остановки)")
        
        # Ждём, пока музыка играет
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        print("✅ Трек завершён.")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка воспроизведения: {e}")
        return False
    finally:
        pygame.mixer.quit()

def get_track_path(track_title=None):
    """Получает путь из БД"""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()
    
    if track_title:
        cur.execute("SELECT file_path FROM tracks WHERE title ILIKE %s;", (f"%{track_title}%",))
    else:
        cur.execute("SELECT file_path FROM tracks ORDER BY id DESC LIMIT 1;")
        
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

# ============================================
# 🎮 ЗАПУСК
# ============================================
if __name__ == "__main__":
    # Ищем Nirvana
    path = get_track_path("Smells Like Teen Spirit")
    if path:
        play_audio_file(path)
    else:
        print("❌ Трек не найден в базе!")