# import libraries for creating buttons
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
# import functions
from app.database.requests import get_categories, get_items_by_category


# creates main menu buttons
main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Catalog', callback_data='catalog')],
                                             [InlineKeyboardButton(text='Cart', callback_data='cart'), InlineKeyboardButton(text='Contacts', callback_data='contacts')]],
                            resize_keyboard=True,
                            input_field_placeholder='Select menu'
                            )

# Button which return back to main menu
to_main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='Return to main menu', callback_data='to_main')]])


# function that creates categories menu
async def categories():
    categories = await get_categories()
    # creates categories keyboard
    keyboard = InlineKeyboardBuilder()
    # for every category in items categories
    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                     callback_data=f'category_{category.id}'))
    return keyboard.adjust(2).as_markup()


# function that creates items menu
async def items(category_id: int):
    items = await get_items_by_category(category_id)
    # creates items keyboard
    keyboard = InlineKeyboardBuilder()
    # for every item in items
    for item in items:
        keyboard.add(InlineKeyboardButton(text=item.name,
                                          callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='Back', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


# function that creates cart menu
async def cart(order_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text='Make an order', callback_data=f'order_{order_id}'))
    keyboard.add(InlineKeyboardButton(text='Back', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


# function that creates delete from cart button
async def delete_from_cart(order_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Delete from cart',
                 callback_data=f'delete_{order_id}'))
    return keyboard.adjust(2).as_markup()
