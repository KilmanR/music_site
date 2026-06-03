import os
import time
import sys
import pygame
from dotenv import load_dotenv
import psycopg2

# Загружаем настройки
load_dotenv()

def play_audio_file(file_path):
    """Воспроизводит аудио через pygame"""
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return False
    
    print(f"🎵 Воспроизвожу: {file_path}")
    
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        print("▶️ Играет... (нажми Ctrl+C для остановки)")
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        print("✅ Трек завершён.")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    finally:
        pygame.mixer.quit()

def get_track_by_id(track_id):
    """Получает трек по ID из БД"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        
        cur = conn.cursor()
        cur.execute("""
            SELECT t.id, t.title, t.file_path, a.title as album, ar.name as artist
            FROM tracks t
            JOIN albums a ON t.album_id = a.id
            JOIN artists ar ON a.artist_id = ar.id
            WHERE t.id = %s;
        """, (track_id,))
        
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        return result
        
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return None

# ============================================
# 🎮 ЗАПУСК
# ============================================
if __name__ == "__main__":
    # Проверяем, передан ли ID как аргумент
    if len(sys.argv) > 1:
        track_id = int(sys.argv[1])
    else:
        # Спрашиваем ID у пользователя
        track_id = int(input("Введите ID трека: "))
    
    print(f"🔍 Ищу трек с ID {track_id}...")
    track = get_track_by_id(track_id)
    
    if track:
        id, title, file_path, album, artist = track
        print(f"🎵 Найдено: {artist} - {title} ({album})")
        print(f"📁 Файл: {file_path}")
        play_audio_file(file_path)
    else:
        print(f"❌ Трек с ID {track_id} не найден!")