# import database tables
from app.database.models import User, Category, Item, Cart
# import module for async requests to database
from app.database.models import async_session
# import modules for sql requests
from sqlalchemy import select, delete


# function that sets user in database by his id
async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


# function that sets product in database
async def set_item(data):
    async with async_session() as session:
        session.add(Item(**data))
        await session.commit()


# function that sets cart in database
async def set_cart(tg_id, item_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.add(Cart(user=user.id, item=item_id))
        await session.commit()


# function that gets cart from database
async def get_cart(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        basket = await session.scalars(select(Cart).where(Cart.user == user.id))
        return basket


# function that gets all users from database
async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users


# function that gets all products categories from database
async def get_categories():
    async with async_session() as session:
        categories = await session.scalars(select(Category))
        return categories


# function that gets all items by category from database
async def get_items_by_category(category_id: int):
    async with async_session() as session:
        items = await session.scalars(select(Item).where(Item.category == category_id))
        return items


# function that gets product by id from database
async def get_item_by_id(item_id: int):
    async with async_session() as session:
        item = await session.scalar(select(Item).where(Item.id == item_id))
        return item


# function that deletes cart from database
async def delete_cart(tg_id, item_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        await session.execute(delete(Cart).where(Cart.user == user.id, Cart.item == item_id))
        await session.commit()
