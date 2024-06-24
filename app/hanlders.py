# import libraries
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
# import main menu keyboard
import app.keyboards as kb
# import functions
from app.database.requests import get_item_by_id, set_cart, get_cart, delete_cart

# setting router for messages filter
router = Router()


# function that processes command start
@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: Message | CallbackQuery):
    # checking if message is Message types
    if isinstance(message, Message):
        await message.answer('Welcome to internet shop!', reply_markup=kb.main)
    else:
        await message.message.edit_text("Welcome to internet shop!", reply_markup=kb.main)


# function that processes bot message text - "catalog"
@router.callback_query(F.data == 'catalog')
async def cmd_catalog(callback: CallbackQuery):
    await callback.answer('_')
    # creates menu with categories to choose
    await callback.message.edit_text('Choose category', reply_markup=await kb.categories())


# function that processes bot message that starts with 'category'
@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Choose product', reply_markup=await kb.items(callback.data.split('_')[1]))


# function that processes bot message that starts with 'item'
@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item = await get_item_by_id(callback.data.split('_')[1])
    await callback.answer('')
    await callback.message.edit_text(f'{item.name}\n\n{item.description}\n\nPrice: {item.price} USD.', reply_markup=kb.to_main)


# function that processes bot message that starts with order_ (orders product)
@router.callback_query(F.data.startswith('order_'))
async def basket(callback: CallbackQuery):
    await set_cart(callback.from_user.id, callback.data.split('_')[1])
    await callback.answer('Product was added to cart')


# function that processes mybasket
@router.callback_query(F.data == 'mybasket')
async def mybasket(callback: CallbackQuery):
    await callback.answer('')
    basket = await get_cart(callback.from_user.id)
    counter = 0
    for item_info in basket:
        item = await get_item_by_id(item_info.item)
        await callback.message.answer_photo(photo=item.photo, caption=f'{item.name}\n\n{item.description}\n\n Price: {item.price} USD',
                                            reply_markup=await kb.delete_from_basket(item.id))
        counter += 1
    await callback.message.answer('Your cart is empty') if counter == 0 else await callback.answer('')


# function that processes bot message that starts with delete_(deletes product from cart)
@router.callback_query(F.data.startswith('delete_'))
async def delete_from_basket(callback: CallbackQuery):
    await delete_cart(callback.from_user.id, callback.data.split('_')[1])
    await callback.message.delete()
    await callback.answer('You deleted product from cart')
