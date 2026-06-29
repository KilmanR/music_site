from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Таблица издателей
class Publisher(Base):
    __tablename__ = 'publisher'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    # Связь с книгами
    books = relationship('Book', back_populates='publisher')
    
    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"

# Таблица книг
class Book(Base):
    __tablename__ = 'book'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)
    
    # Связи
    publisher = relationship('Publisher', back_populates='books')
    stocks = relationship('Stock', back_populates='book')
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"

# Таблица магазинов
class Shop(Base):
    __tablename__ = 'shop'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    # Связь с наличием
    stocks = relationship('Stock', back_populates='shop')
    
    def __repr__(self):
        return f"<Shop(id={self.id}, name='{self.name}')>"

# Таблица наличия книг в магазинах
class Stock(Base):
    __tablename__ = 'stock'
    
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False, default=0)
    
    # Связи
    book = relationship('Book', back_populates='stocks')
    shop = relationship('Shop', back_populates='stocks')
    sales = relationship('Sale', back_populates='stock')
    
    def __repr__(self):
        return f"<Stock(id={self.id}, book_id={self.id_book}, shop_id={self.id_shop}, count={self.count})>"

# Таблица продаж
class Sale(Base):
    __tablename__ = 'sale'
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False, default=1)
    
    # Связь
    stock = relationship('Stock', back_populates='sales')
    
    def __repr__(self):
        return f"<Sale(id={self.id}, price={self.price}, date={self.date_sale})>"


# Функция для создания БД
def create_db(engine):
    """Создаёт все таблицы в БД"""
    Base.metadata.create_all(engine)


# Подключение к БД
def get_db_session(db_url):
    """Создаёт сессию для работы с БД"""
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session(), engine