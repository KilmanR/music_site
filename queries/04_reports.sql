-- ============================================
-- 04_REPORTS.SQL - Отчёты и аналитика
-- ============================================

-- 1. Статистика по жанрам
SELECT 
    g.name as genre,
    COUNT(DISTINCT ar.id) as artists_count,
    COUNT(DISTINCT a.id) as albums_count,
    COUNT(t.id) as tracks_count
FROM genres g
LEFT JOIN artists ar ON g.id = ar.genre_id
LEFT JOIN albums a ON ar.id = a.artist_id
LEFT JOIN tracks t ON a.id = t.album_id
GROUP BY g.id
ORDER BY tracks_count DESC;

-- 2. Топ исполнителей по количеству треков
SELECT 
    ar.name as artist,
    COUNT(t.id) as total_tracks,
    COUNT(DISTINCT a.id) as total_albums
FROM artists ar
JOIN albums a ON ar.id = a.artist_id
JOIN tracks t ON a.id = t.album_id
GROUP BY ar.id
ORDER BY total_tracks DESC;

-- 3. Альбомы по десятилетиям
SELECT 
    (year / 10) * 10 as decade,
    COUNT(*) as albums_count
FROM albums
GROUP BY decade
ORDER BY decade;

-- 4. Средняя длительность трека (в секундах)
SELECT 
    AVG(duration_ms) / 1000 as avg_duration_sec
FROM tracks;