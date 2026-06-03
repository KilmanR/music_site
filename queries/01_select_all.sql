-- ============================================
-- 01_SELECT_ALL.SQL - Основные SELECT-запросы
-- ============================================

-- 1. Все жанры
SELECT * FROM genres;

-- 2. Все исполнители
SELECT * FROM artists;

-- 3. Все альбомы
SELECT * FROM albums;

-- 4. Все треки
SELECT * FROM tracks;

-- 5. Треки с информацией о файле
SELECT 
    id,
    title,
    duration_ms,
    duration_ms / 1000 as duration_sec,
    file_path
FROM tracks;

-- 6. Найти трек по названию (частичное совпадение)
SELECT * FROM tracks 
WHERE title ILIKE '%Teen Spirit%';

-- 7. Все треки конкретного альбома (по ID альбома)
SELECT * FROM tracks 
WHERE album_id = 1;

-- 8. Альбомы определённого года
SELECT * FROM albums 
WHERE year = 1991;