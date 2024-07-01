from aiogram.types import Message
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message, CallbackQuery, LabeledPrice, ShippingQuery, PreCheckoutQuery
from product.delivery_option import FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from keyboards.defoult import *
from aiogram import F
from loader import  router_asosiy, bot, db_admins
from keyboards.defoult.keys import *
from keyboards.inline.keys import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import openpyxl
from aiogram.types.input_file import FSInputFile
from aiogram.enums import ChatAction


workbook = openpyxl.Workbook()
sheet = workbook.active

class Admins(StatesGroup):
    user_id = State()
    name = State()
    surname = State()
    contact = State()
    nikname = State()

class Asosiy(Filter):
    def __init__(self, my_id: int):
        self.my_id = my_id

    async def __call__(self, msg: Message):
        return msg.from_user.id == self.my_id
    
ADMIN = 6611770508

@router_asosiy.message(CommandStart(), Asosiy(ADMIN))
async def start(msg: Message):
    await msg.answer("Assalomu aleykum Admin!", reply_markup=menu_asosiy_admin)

#-------------------New Admin----------------------------

@router_asosiy.message(F.text == 'Yangi Admin')
async def Add(msg: Message, state: FSMContext):
    db_admins.create_table()
    await state.set_state(Admins.user_id)
    await msg.answer("Yangi admin id sini yuboring!")

@router_asosiy.message(Admins.user_id)
async def user_id_set(msg: Message, state: FSMContext):
    await state.update_data(user_id = msg.text)
    await state.set_state(Admins.name)
    await msg.answer("Yangi admin ismini yuboring!")

@router_asosiy.message(Admins.name)
async def name_set(msg: Message, state: FSMContext):
    await state.update_data(name = msg.text)
    await state.set_state(Admins.surname)
    await msg.answer("Yangi admin familyasini yuboring!")

@router_asosiy.message(Admins.surname)
async def surname_set(msg: Message, state: FSMContext):
    await state.update_data(surname = msg.text)
    await state.set_state(Admins.contact)
    await msg.answer("Yangi admin telefonini yuboring!")

@router_asosiy.message(Admins.contact)
async def contact_set(msg: Message, state: FSMContext):
    await state.update_data(contact = msg.text)
    await state.set_state(Admins.nikname)
    await msg.answer("Yangi admin nikname ni yuboring!")

@router_asosiy.message(Admins.nikname)
async def nikname_set(msg: Message, state: FSMContext):
    await state.update_data(nikname = msg.text)
    data = await state.get_data()
    print(data)
    user_id = data['user_id']
    name = data['name']
    surname  = data['surname']
    contact = data['contact']
    nikname = data['nikname']
    await state.clear()
    db_admins.add_admins(user_id, name, surname, contact, nikname)
    await msg.answer("Admin qo'shildi!")

#-------------------Sotuvchilar Table----------------------
    
@router_asosiy.message(F.text == 'Sotuvchilar')
async def sotuvchilar(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
    
    user_info = db_admins.select_admins()
    if user_info:
        # Ustun sarlavhalarini qo'shish
        headers = ['ID', 'User_ID', 'Name', 'Surname', 'Contact', 'Nikname']
        sheet.append(headers)

        # Har bir sotuvchi uchun ma'lumotlarni Excel jadvalida yangi qatorga qo'shish
        for user in user_info:
            sheet.append(user)  # `user` ro'yxat bo'lishi kerak, shuning uchun to'g'ridan-to'g'ri qo'shamiz

        # Excel faylini saqlash
        workbook.save('sotuvchilar.xlsx')

    # Correctly using InputFile with the file path
    file_path = "sotuvchilar.xlsx"
    document = FSInputFile(file_path)
    
    # Sending the document
    await msg.bot.send_document(chat_id=msg.from_user.id, document=document)


