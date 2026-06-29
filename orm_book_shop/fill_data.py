from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Publisher, Book, Shop, Stock, Sale, Base
from datetime import date

# Подключение
engine = create_engine('postgresql://postgres:postgres@localhost:5432/book_shop_db')
Session = sessionmaker(bind=engine)

with Session() as session:
    # Проверяем есть ли данные
    if session.query(Publisher).count() > 0:
        print("⚠️  База уже заполнена!")
        exit()
    
    # 1. Добавляем издателей
    publishers = [
        Publisher(name='Пушкин'),
        Publisher(name='Толстой'),
        Publisher(name='Достоевский'),
    ]
    session.add_all(publishers)
    session.commit()
    
    # 2. Добавляем книги
    books = [
        Book(title='Капитанская дочка', id_publisher=1),
        Book(title='Руслан и Людмила', id_publisher=1),
        Book(title='Евгений Онегин', id_publisher=1),
        Book(title='Война и мир', id_publisher=2),
        Book(title='Анна Каренина', id_publisher=2),
        Book(title='Преступление и наказание', id_publisher=3),
    ]
    session.add_all(books)
    session.commit()
    
    # 3. Добавляем магазины
    shops = [
        Shop(name='Буквоед'),
        Shop(name='Лабиринт'),
        Shop(name='Книжный дом'),
    ]
    session.add_all(shops)
    session.commit()
    
    # 4. Добавляем наличие (stock)
    stocks = [
        Stock(id_book=1, id_shop=1, count=10),  # Капитанская дочка в Буквоеде
        Stock(id_book=1, id_shop=2, count=5),   # Капитанская дочка в Лабиринте
        Stock(id_book=2, id_shop=1, count=8),   # Руслан и Людмила в Буквоеде
        Stock(id_book=3, id_shop=3, count=3),   # Евгений Онегин в Книжном доме
        Stock(id_book=4, id_shop=1, count=7),   # Война и мир в Буквоеде
        Stock(id_book=5, id_shop=2, count=4),   # Анна Каренина в Лабиринте
        Stock(id_book=6, id_shop=3, count=6),   # Преступление и наказание
    ]
    session.add_all(stocks)
    session.commit()
    
    # 5. Добавляем продажи
    sales = [
        Sale(price=600, date_sale=date(2022, 11, 9), id_stock=1, count=1),
        Sale(price=500, date_sale=date(2022, 11, 8), id_stock=3, count=1),
        Sale(price=580, date_sale=date(2022, 11, 5), id_stock=2, count=1),
        Sale(price=490, date_sale=date(2022, 11, 2), id_stock=4, count=1),
        Sale(price=600, date_sale=date(2022, 10, 26), id_stock=1, count=1),
        Sale(price=750, date_sale=date(2022, 11, 10), id_stock=5, count=1),
    ]
    session.add_all(sales)
    session.commit()
    
    print("✅ База заполнена тестовыми данными!")
    print(f"   Издателей: {session.query(Publisher).count()}")
    print(f"   Книг: {session.query(Book).count()}")
    print(f"   Магазинов: {session.query(Shop).count()}")
    print(f"   Продаж: {session.query(Sale).count()}")