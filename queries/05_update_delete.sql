-- ============================================
-- 05_UPDATE_DELETE.SQL - Обновление и удаление
-- ============================================

-- 1. Обновить путь к файлу для трека
UPDATE tracks 
SET file_path = 'media/audio/new_path.mp3'
WHERE title = 'Smells Like Teen Spirit';

-- 2. Изменить год альбома
UPDATE albums 
SET year = 1992
WHERE title = 'Nevermind';

-- 3. Увеличить длительность трека (исправление ошибки)
UPDATE tracks 
SET duration_ms = 305000
WHERE title = 'Smells Like Teen Spirit';

-- 4. Удалить трек (осторожно!)
-- DELETE FROM tracks WHERE title = 'Test Track';

-- 5. Удалить альбом (сначала нужно удалить треки!)
-- DELETE FROM tracks WHERE album_id = 5;
-- DELETE FROM albums WHERE id = 5;

-- 6. Переименовать исполнителя
-- UPDATE artists SET name = 'New Name' WHERE id = 1;