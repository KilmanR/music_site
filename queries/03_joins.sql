-- ============================================
-- 03_JOINS.SQL - Связанные запросы
-- ============================================

-- 1. Все треки с информацией об альбоме и исполнителе
SELECT 
    t.id,
    t.title as track_title,
    ar.name as artist_name,
    a.year,
    a.title as album_title,
    g.name as genre_name,
    t.duration_ms,
    t.file_path                
FROM tracks t
JOIN albums a ON t.album_id = a.id
JOIN artists ar ON a.artist_id = ar.id
JOIN genres g ON ar.genre_id = g.id;

-- 2. Все альбомы с исполнителями
SELECT 
    a.title as album,
    a.year,
    ar.name as artist,
    g.name as genre
FROM albums a
JOIN artists ar ON a.artist_id = ar.id
JOIN genres g ON ar.genre_id = g.id
ORDER BY a.year DESC;

-- 3. Сколько треков в каждом альбоме
SELECT 
    a.title as album,
    ar.name as artist,
    COUNT(t.id) as tracks_count
FROM albums a
JOIN artists ar ON a.artist_id = ar.id
LEFT JOIN tracks t ON t.album_id = a.id
GROUP BY a.id, ar.name
ORDER BY tracks_count DESC;

-- 4. Общая длительность альбома (в минутах)
SELECT 
    a.title as album,
    ar.name as artist,
    SUM(t.duration_ms) / 1000 / 60 as duration_minutes
FROM albums a
JOIN artists ar ON a.artist_id = ar.id
JOIN tracks t ON t.album_id = a.id
GROUP BY a.id, ar.name;