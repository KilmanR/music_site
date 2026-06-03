import os
import shutil
from dotenv import load_dotenv
import psycopg2

# ============================================
# 🎵 ДАННЫЕ ДЛЯ ВСТАВКИ (МЕНЯЙ ТОЛЬКО ЗДЕСЬ!)
# ============================================
GENRE = "Dance"                   # Жанр
ARTIST = "Edo Denova, Sz_Becca"                # Исполнитель
ALBUM = "Like A Prayer"                # Альбом
YEAR = 2026                         # Год выпуска
TRACK = "Like A Prayer"   # Трек
DURATION_SEC = 148                   # Длительность в секундах
MP3_FILE_PATH = "media/audio/edo_denova_sz_becca_like_a_prayer.mp3" # Путь к файлу
# ============================================

# Загружаем настройки из .env
load_dotenv()

# Подключаемся к БД
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print(f"🎵 Добавляем: {ARTIST} - {TRACK}")

cur = conn.cursor()

# 1. Добавляем жанр (если нет)
cur.execute("SELECT id FROM genres WHERE name = %s;", (GENRE,))
genre_id = cur.fetchone()
if not genre_id:
    cur.execute("INSERT INTO genres (name) VALUES (%s) RETURNING id;", (GENRE,))
    genre_id = cur.fetchone()[0]
    print(f"✅ Жанр '{GENRE}' добавлен (ID: {genre_id})")
else:
    genre_id = genre_id[0]
    print(f"✓ Жанр '{GENRE}' уже существует (ID: {genre_id})")

# 2. Добавляем исполнителя (если нет)
cur.execute("SELECT id FROM artists WHERE name = %s AND genre_id = %s;", (ARTIST, genre_id))
artist_id = cur.fetchone()
if not artist_id:
    cur.execute("INSERT INTO artists (name, genre_id) VALUES (%s, %s) RETURNING id;", (ARTIST, genre_id))
    artist_id = cur.fetchone()[0]
    print(f"✅ Исполнитель '{ARTIST}' добавлен (ID: {artist_id})")
else:
    artist_id = artist_id[0]
    print(f"✓ Исполнитель '{ARTIST}' уже существует (ID: {artist_id})")

# 3. Добавляем альбом (если нет)
cur.execute("SELECT id FROM albums WHERE title = %s AND artist_id = %s;", (ALBUM, artist_id))
album_id = cur.fetchone()
if not album_id:
    cur.execute("INSERT INTO albums (title, year, artist_id) VALUES (%s, %s, %s) RETURNING id;", (ALBUM, YEAR, artist_id))
    album_id = cur.fetchone()[0]
    print(f"✅ Альбом '{ALBUM}' ({YEAR}) добавлен (ID: {album_id})")
else:
    album_id = album_id[0]
    print(f"✓ Альбом '{ALBUM}' уже существует (ID: {album_id})")

# 4. Добавляем трек с путём к файлу
duration_ms = DURATION_SEC * 1000
cur.execute("SELECT id FROM tracks WHERE title = %s AND album_id = %s;", (TRACK, album_id))
track_exists = cur.fetchone()

if not track_exists:
    cur.execute("""
        INSERT INTO tracks (title, duration_ms, album_id, file_path) 
        VALUES (%s, %s, %s, %s);
    """, (TRACK, duration_ms, album_id, MP3_FILE_PATH))
    print(f"✅ Трек '{TRACK}' добавлен!")
    print(f"📁 Путь к файлу: {MP3_FILE_PATH}")
else:
    # Обновляем путь к файлу, если трек уже есть
    cur.execute("""
        UPDATE tracks SET file_path = %s 
        WHERE title = %s AND album_id = %s;
    """, (MP3_FILE_PATH, TRACK, album_id))
    print(f"✓ Путь к файлу обновлён для '{TRACK}'")

# Сохраняем изменения
conn.commit()
cur.close()
conn.close()

print("✅ Готово!")