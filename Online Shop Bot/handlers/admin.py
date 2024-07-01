from aiogram.types import Message
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message, CallbackQuery, LabeledPrice, ShippingQuery, PreCheckoutQuery
from product.delivery_option import FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from keyboards.defoult import *
from aiogram import F
from loader import router_user, router_admin, bot,db_admins, db_pro, db_user, click_token
from keyboards.defoult.keys import *
from keyboards.inline.keys import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
import time

class Product(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    soni = State()
    category = State()

class Admin(Filter):
    def __init__(self, my_id: int):
        self.my_id = my_id

    async def __call__(self, msg: Message):
        return msg.from_user.id == self.my_id
    
ADMINS = db_admins.select_admins()

for admin in ADMINS:
    user_id = admin[1]

@router_admin.message(CommandStart(), Admin(user_id))
async def start(msg: Message):
    db_pro.create_table()
    await msg.answer("Assalomu aleykum Sotuvchi!", reply_markup=menu_admin)

#----------------------------Product Add----------------------
@router_admin.message(F.text == 'Add')
async def Add(msg: Message, state: FSMContext):
    await state.set_state(Product.name)
    await msg.answer("Mahsulot nomini yuboring!")

@router_admin.message(Product.name)
async def productname_set(msg: Message, state: FSMContext):
    await state.update_data(name = msg.text)
    await state.set_state(Product.description)
    await msg.answer("Mahsulot tavsifini yuboring!")

@router_admin.message(Product.description)
async def productdescription_set(msg: Message, state: FSMContext):
    await state.update_data(description = msg.text)
    await state.set_state(Product.price)
    await msg.answer("Mahsulot qiymatini yuboring!")

@router_admin.message(Product.price)
async def productprice_set(msg: Message, state: FSMContext):
    await state.update_data(price = msg.text)
    await state.set_state(Product.image)
    await msg.answer("Mahsulot rasmini yuboring!")

@router_admin.message(Product.image, F.photo)
async def productimage_set(msg: Message, state: FSMContext):
    photo_id = msg.photo[-1].file_id
    await state.update_data(image = photo_id)
    await state.set_state(Product.soni)
    await msg.answer("Mahsulot sonini kiriting!")  

@router_admin.message(Product.soni)
async def productsoni_set(msg: Message, state: FSMContext):
    await state.update_data(soni = msg.text)
    await state.set_state(Product.category)
    await msg.answer("Mahsulot categoriyasini tanlang!", reply_markup=category)  

#--------------------------------------Elektronika-------------------------------
@router_admin.callback_query(F.data == 'elektronika')
async def elektronikas(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("""Ushbu category ga siz elektronika mahsulotlarini qo'shishingiz mumkin!\n
                                  Smartfon - Telefonlar\n
                                  Televizor - Televizorlar\n
                                  Noutbuk - Noutbuklar\n
                                  Aqlli soat - Aqlli soatlar, Smart Watchlar va b.\n
                                  Quloqchin - Quloqchinlar, AirPods\n
                                  O'yin pristavka - O'yin pristavkalari""")
    await callback.message.answer("Tanlang:👇", reply_markup=elektronika)

@router_admin.callback_query(F.data == "smartfon", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "televizor", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "noutbuk", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "aqlli_soat", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "quloqchin", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "oyin_pristavka", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

#--------------------------------------Kiyimi-------------------------------
@router_admin.callback_query(F.data == 'kiyim')
async def kyim(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("""Ushbu category ga siz kiyim mahsulotlarini qo'shishingiz mumkin!\n
                                  Ayollar - Ayollarlar kiyimlari\n
                                  Bolalar - Bolalar kiyimlari\n
                                  Erkaklar - Erkaklar kiyimlari\n""")
    await callback.message.answer("Tanlang:👇", reply_markup=kiyim)

@router_admin.callback_query(F.data == "ayollar_", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "bolalar", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "erkaklar_k", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

#--------------------------------------Avto tovar-------------------------------
@router_admin.callback_query(F.data == 'avtotovar')
async def avtotovr(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("""Ushbu category ga siz avto tovarlarni qo'shishingiz mumkin!\n
                                  Akkumlyator - Akkumlyatorlar\n
                                  Asbob va uskuna - Asbob va uskunalar\n
                                  Shina va diskalar - Shina va diskalar\n
                                  Avto tovush - Avto tovush aksessuarlari\n
                                  Ehtiyot qismlar - Mashina uchun ehtiyot qismlar\n""")
    await callback.message.answer("Tanlang:👇", reply_markup=avtotovar)

@router_admin.callback_query(F.data == "akkumlyator", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "asbob_va_uskuna", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "shina_va_diskalar", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "avtotovush", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "ehtiyot_qism", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

#--------------------------------------Poyabzal-------------------------------
@router_admin.callback_query(F.data == 'poyabzal')
async def tovar(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("""Ushbu category ga siz poyabzalarni qo'shishingiz mumkin!\n
                                  Ayollar - Ayollarlar oyoq kiyimlari\n
                                  Erkaklar - Erkaklar oyoq kiyimlari\n
                                  O'g'il bola - O'g'il bolalar oyoq kiyimlari \n
                                  Qizlar - Qizlar oyoq kiyimlari\n""") 
    await callback.message.answer("Tanlang:👇", reply_markup=poyabzal)

@router_admin.callback_query(F.data == "ayollar_p", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "erkaklar_p", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "ogil_bola", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "qizlar", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 


#--------------------------------------Maishiy Texnika-------------------------------
@router_admin.callback_query(F.data == 'maishiy_texnika')
async def tovar(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("""Ushbu category ga siz maishiy texnikalarni qo'shishingiz mumkin!\n
                                  Go'zallik - Go'zallik uchun texnikalar\n
                                  Iqlim - Iqlim texnikalari. Konditsioner va ventilyatorlar\n
                                  Oshxona buyumlari - Oshxona buyumlari\n
                                  Uy uchun texnika - Uy uchun texnikalar. Dazmollar, changyutgichlar va b.\n
                                  Katta maishiy texnika - Katta maishiy texnikalar. Muzlatgichlar, kir yuvish mashinalari va b.""")
    await callback.message.answer("Tanlang:👇", reply_markup=maishiy_texnika)

@router_admin.callback_query(F.data == "gozallik", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "oshxona_buyumlari", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "katta_maishiy_texnika", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "iqlim", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

@router_admin.callback_query(F.data == "uy_uchun_texnika", Product.category)
async def smartfon(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(category= callback.data)
    data = await state.get_data()
    print(data)
    name = data['name']
    description = data['description']
    price = data['price']
    image = data['image']
    category = data['category']
    soni = data['soni']
    await state.clear() 
    db_pro.add_products(name, price, description, image, category, soni)
    await callback.message.answer("Mahsulot qo'shildi!") 

#---------------------See All Products--------------------

@router_admin.message(F.text == 'Mahsulotlar')
async def products(msg: Message):
    products = db_pro.select_products()
    await msg.answer("Mahsulotlar ro'yxati:")
    for product in products:
        name = product[1]
        price = product[2]
        description = product[3]
        image = product[4]
        category = product[5]
        soni = product[6]
        time.sleep(0.2)
        await bot.send_photo(chat_id=msg.from_user.id, photo=image,caption=f"Mahsulot: <b>{name}</b>\nTavsif: <b>{description}</b>\nNarxi: <b>{price}</b>\nMahsulot categoriyasi: <b>{category}</b>\nMahsulot soni: <b>{soni}</b>")