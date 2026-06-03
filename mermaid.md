graph TD
    subgraph genres [🟣 Таблица: genres]
        direction TB
        G1[🔑 id (PK)]
        G2[📝 name]
    end

    subgraph artists [ Таблица: artists]
        direction TB
        A1[🔑 id (PK)]
        A2[🔗 genre_id (FK -> genres)]
        A3[ name]
    end

    subgraph albums [🟢 Таблица: albums]
        direction TB
        AL1[🔑 id (PK)]
        AL2[🔗 artist_id (FK -> artists)]
        AL3[📝 title]
        AL4[ year]
    end

    subgraph tracks [🟡 Таблица: tracks]
        direction TB
        T1[🔑 id (PK)]
        T2[🔗 album_id (FK -> albums)]
        T3[📝 title]
        T4[⏱ duration_ms]
        T5[📁 file_path]
    end

    genres -- "1 Жанр" --> "N Исполнителей" : artists
    artists -- "1 Исполнитель" --> "N Альбомов" : albums
    albums -- "1 Альбом" --> "N Треков" : tracks