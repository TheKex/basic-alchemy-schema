import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=180), nullable=False, unique=True)
    books = relationship("Book", back_populates="publisher")

    def __str__(self):
        return f"Publisher {self.id}: {self.name}"


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(200))
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"))
    publisher = relationship("Publisher", back_populates="books")
    shops = relationship("Shop", secondary="stock", back_populates="books")
    stocks = relationship("Stock", back_populates="book", viewonly=True)

    def __str__(self):
        return f"Book {self.id}: {self.title}"


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(200))
    books = relationship("Book", secondary="stock", back_populates="shops")
    stocks = relationship("Stock", back_populates="shop", viewonly=True)

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"))
    count = sq.Column(sq.Integer)

    __table_args__ = (sq.UniqueConstraint('id_book', 'id_shop', name='stock_unique'),
                      sq.CheckConstraint('count >= 0', name='stock_positive_count')
                      )
    book = relationship("Book", back_populates="stocks", viewonly=True)
    shop = relationship("Shop", back_populates="stocks", viewonly=True)
    sales = relationship("Sale", back_populates="stock")

    def __str__(self):
        return f"Book {self.id}: book - {self.book.title}, shop - {self.shop.name}"

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"))
    count = sq.Column(sq.Integer)

    stock = relationship("Stock", back_populates="sales")

    def __str__(self):
        return f"Sale {self.id}: {self.price}, {self.date_sale}"



def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)