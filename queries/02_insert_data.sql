-- ============================================
-- 02_INSERT_DATA.SQL - Вставка данных
-- ============================================

-- 1. Добавить новый жанр
INSERT INTO genres (name) VALUES ('Electronic');

-- 2. Добавить исполнителя
INSERT INTO artists (name, genre_id) VALUES ('Harper Quinn, Emily Esthela, Namté', 3);

-- 3. Добавить альбом
INSERT INTO albums (title, year, artist_id) 
VALUES ('Stolen Dance', 2025 , 3);

-- 4. Добавить трек (с путём к файлу)
INSERT INTO tracks (title, duration_ms, album_id, file_path) 
VALUES (
    'Stolen Dance', 
    157000, 
    3, 
    'media/audio/harper_quinn_emily_esthela_namte_stolen_dance.mp3'
);

-- 5. Добавить несколько жанров сразу
INSERT INTO genres (name) VALUES 
    ('Jazz'),
    ('Electronic'),
    ('Pop');