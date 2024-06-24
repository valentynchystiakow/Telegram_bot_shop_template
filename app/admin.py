# import messages router
from aiogram import Router, F
# import libraries
from aiogram.types import Message, CallbackQuery
# import Router Filters
from aiogram.filters import Command, Filter
# import FSM modules
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# import keyboards
import app.keyboards as kb
# import functions
from app.database.requests import get_users, set_item


# setting router for admin messages
admin = Router()


# FSM for Newsletter
class Newsletter(StatesGroup):
    message = State()


# FSM for adding item
class AddItem(StatesGroup):
    name = State()
    category = State()
    description = State()
    photo = State()
    price = State()


# setting admin messages router filter
class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [5791374868]


# function that processes apanel command
@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: Message):
    await message.answer('Another commands: /newsletter\n/add_item')


# function that processes newsletter command
@admin.message(AdminProtect(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Send message, which you want to send to all users')


# function that processes message to Newsletter
@admin.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer('Wait... Newsletter is going.')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            pass
    await message.answer('Newsletter ended succesfully.')
    await state.clear()


# function that processes add_item to database command
@admin.message(AdminProtect(), Command('add_item'))
async def add_item(message: Message, state: FSMContext):
    await state.set_state(AddItem.name)
    await message.answer("Enter product's name")


# function that processes entering product name in FMS
@admin.message(AdminProtect(), AddItem.name)
async def add_item_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    # switches to next step
    await state.set_state(AddItem.category)
    await message.answer('Choose product category', reply_markup=await kb.categories())


# function that processes entering product category in FMS
@admin.callback_query(AdminProtect(), AddItem.category)
async def add_item_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split('_')[1])
    # switches to next step
    await state.set_state(AddItem.description)
    await callback.answer('')
    await callback.message.answer('Enter product description')


# function that processes editing product description in FMS
@admin.message(AdminProtect(), AddItem.description)
async def add_item_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    # switches to next step
    await state.set_state(AddItem.photo)
    await message.answer('Send product photo')


# function that processes sending product photo in FMS
@admin.message(AdminProtect(), AddItem.photo, F.photo)
async def add_item_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    # switches to next step
    await state.set_state(AddItem.price)
    await message.answer('Enter product price')


# function that processes adding product's price and ending FMS
@admin.message(AdminProtect(), AddItem.price)
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await set_item(data)
    await message.answer('The product was added succesfully')
    # clears fms
    await state.clear()
