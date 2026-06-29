from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Stock, Shop, Sale, Base, create_db
from datetime import datetime
import os

# Параметры подключения (вынеси в переменные окружения!)
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'book_shop_db')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def find_publisher_sales(publisher_input):
    """
    Находит все продажи книг конкретного издателя
    
    publisher_input: имя или ID издателя
    """
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        # Проверяем, число ли ввели (ID) или строку (имя)
        if publisher_input.isdigit():
            publisher_id = int(publisher_input)
            publisher = session.query(Publisher).filter(Publisher.id == publisher_id).first()
        else:
            publisher = session.query(Publisher).filter(
                Publisher.name.ilike(f'%{publisher_input}%')
            ).first()
        
        if not publisher:
            print(f"Издатель '{publisher_input}' не найден!")
            return
        
        print(f"\n📚 Продажи книг издательства '{publisher.name}':\n")
        print(f"{'Название книги':<30} | {'Магазин':<20} | {'Цена':<8} | {'Дата':<12}")
        print("-" * 80)
        
        # Запрос с JOIN'ами
        results = session.query(
            Book.title,
            Shop.name,
            Sale.price,
            Sale.date_sale
        ).join(
            Stock, Book.id == Stock.id_book
        ).join(
            Shop, Stock.id == Stock.id_shop
        ).join(
            Sale, Stock.id == Sale.id_stock
        ).filter(
            Book.id_publisher == publisher.id
        ).all()
        
        for book_title, shop_name, price, date_sale in results:
            print(f"{book_title:<30} | {shop_name:<20} | {price:<8} | {date_sale.strftime('%d-%m-%Y'):<12}")
        
        print(f"\nВсего найдено: {len(results)} продаж(и)")


def main():
    # Создаём таблицы (если ещё не созданы)
    engine = create_engine(DATABASE_URL)
    create_db(engine)
    print("✅ Таблицы созданы!")
    
    # Запрашиваем издателя
    publisher_input = input("\nВведите имя или ID издателя: ").strip()
    
    if publisher_input:
        find_publisher_sales(publisher_input)


if __name__ == "__main__":
    main()