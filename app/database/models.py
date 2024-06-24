# import libraries(modules) for working with database
from sqlalchemy import BigInteger, ForeignKey, String
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# import engine which starts database
from config import ENGINE, ECHO

# runs database
engine = create_async_engine(url=ENGINE, echo=ECHO)
async_session = async_sessionmaker(engine)


# creates Base main Class
class Base(AsyncAttrs, DeclarativeBase):
    pass
    # tables and name of their columns
    """
        user(id,tg_id),
        category(id,name),
        item(id,name,description,image,price)
        cart(id,user_id,product_id)

    """


# creates Users table
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    # creates relqtions between tables
    cart_rel: Mapped[List['Cart']] = relationship(
        back_populates='user_rel')


# creates categories table
class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    item_rel: Mapped[List['Item']] = relationship(
        back_populates='category_rel')


# creates items table
class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    photo: Mapped[str] = mapped_column(String(200))
    price: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    # creates relations between tables
    category_rel: Mapped['Category'] = relationship(back_populates='item_rel')
    cart_rel: Mapped[List['Cart']] = relationship(
        back_populates='item_rel')


# creates Cart table
class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item: Mapped[int] = mapped_column(ForeignKey('items.id'))
    # creates relations between tables
    user_rel: Mapped['User'] = relationship(back_populates='cart_rel')
    item_rel: Mapped['Item'] = relationship(back_populates='cart_rel')


# function that runs engine(creates all tables in database)
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
