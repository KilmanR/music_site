--CREATE TYPE sex_type AS ENUM (
--    'male', 
--    'female', 
--    'other',
--    'attack_helicopter'
--    );

--CREATE TABLE IF NOT EXISTS client (
--    client_id SERIAL PRIMARY KEY,
--    email VARCHAR(255) NOT NULL,
--    address VARCHAR(255) NULL,
--    phone VARCHAR(15) NULL,
--    sex sex_type NOT NULL
--);

CREATE TABLE author (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birthday DATE NOT NULL
);

--CREATE TABLE IF NOT EXISTS book (
--    book_id SERIAL PRIMARY KEY,
--    title VARCHAR(255) NOT NULL,
--    price DECIMAL(10, 2) NOT NULL,
--    rating DECIMAL(3, 2) NULL,
--    total_pages INTEGER NOT NULL
--);

--CREATE TABLE IF NOT EXISTS book_author (
--    book_author_id SERIAL PRIMARY KEY,
--    book_id INTEGER NOT NULL,
--    author_id INTEGER NOT NULL,
--    CONSTRAINT fk_book FOREIGN KEY(book_id) REFERENCES book (book_id) ON DELETE CASCADE,
--    CONSTRAINT fk_author FOREIGN KEY(author_id) REFERENCES author(author_id) ON DELETE CASCADE
--);

--CREATE TABLE IF NOT EXISTS orders (
--    orders_id SERIAL PRIMARY KEY,
--    status VARCHAR(20) NOT NULL,
--    total_price DECIMAL(11, 2) NOT NULL,
--    client_id INTEGER NOT NULL REFERENCES client(client_id),
--    CONSTRAINT c1 CHECK (status IN ('OPEN', 'IN PROGRESS', 'CLOSED'))
--);