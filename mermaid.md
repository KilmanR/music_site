# 🎵 Music Database Schema

## Entity-Relationship Diagram

```mermaid
erDiagram
    GENRES ||--o{ ARTISTS : "has many"
    ARTISTS ||--o{ ALBUMS : "creates many"
    ALBUMS ||--o{ TRACKS : "contains many"

    GENRES {
        int id PK
        string name UK
    }

    ARTISTS {
        int id PK
        string name
        int genre_id FK
    }

    ALBUMS {
        int id PK
        string title
        int year
        int artist_id FK
    }

    TRACKS {
        int id PK
        string title
        int duration_ms
        string file_path
        int album_id FK
    }