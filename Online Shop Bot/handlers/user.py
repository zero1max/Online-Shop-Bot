from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, LabeledPrice, ShippingQuery, PreCheckoutQuery
from product.delivery_option import FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from keyboards.defoult import *
from aiogram import F
from loader import router_user,  bot, db_pro,db_admins, db_user, click_token
from keyboards.defoult.keys import *
from keyboards.inline.keys import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
import time

USERDATA = {}

#-------------------------START--------------------------------
@router_user.message(CommandStart())
async def start(msg: Message):
    db_user.create_table()
    await msg.answer("Assalomu aleykum!", reply_markup=menu_user)

#-------------------------ID ---------------------------------
@router_user.message(Command("id"))
async def id(msg: Message):
    await msg.answer(f"ID: {msg.from_user.id}")


# #------------------------MENU --------------------------------
@router_user.message(F.text == "Menu🧾")
async def menu(msg: Message):
    products = db_pro.select_products()
    product = products[0]  # Birinchi mahsulotni olish
    name = product[1]
    price = product[2]
    description = product[3]
    image = product[4]
    await bot.send_photo(chat_id=msg.from_user.id, photo=image, caption=f"Mahsulot nomi: {name}\nMahsulot tavsifi: {description}\nMahsulot narxi: {price}", reply_markup=nextorprevious)

@router_user.callback_query(lambda c: c.data == 'next')
async def show_next_product(callback_query: CallbackQuery):
    product = db_pro.select_next_product()
    if product:
        # Mahsulot ma'lumotlarini ko'rsatish
        await show_product(callback_query, product)
    else:
        await callback_query.answer("Bu so'nggi mahsulot.", show_alert=True)

@router_user.callback_query(lambda c: c.data == 'previous')
async def show_previous_product(callback_query: CallbackQuery):
    product = db_pro.select_previous_product()
    if product:
        # Mahsulot ma'lumotlarini ko'rsatish
        await show_product(callback_query, product)
    else:
        await callback_query.answer("Bu birinchi mahsulot.", show_alert=True)

@router_user.callback_query(lambda c: c.data == 'savesavat')
async def save_to_cart(callback_query: CallbackQuery):
    # Foydalanuvchining hozirgi tanlangan mahsulotini savatga qo'shish
    user_id = callback_query.from_user.id
    current_product = db_pro.select_product_by_id(db_pro.current_product_id)
    if current_product:
        product_id = current_product[0]
        db_pro.add_to_cart(db_pro.shopping_carts, user_id, product_id)
        await callback_query.answer("Mahsulot savatga qo'shildi")
    else:
        await callback_query.answer("Mahsulot topilmadi", show_alert=True)

@router_user.callback_query(lambda c: c.data == 'savat')
async def show_cart(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    cart = db_pro.show_cart(db_pro.shopping_carts, user_id)
    if cart != "Sizning savatingiz bo'sh.":
        message_text = "Savatingizdagi mahsulotlar:\n"
        total = 0
        for product_id, quantity in cart.items():
            product = db_pro.select_product_by_id(product_id)
            if product:  # Mahsulot mavjudligini tekshirish
                name = product[1]
                price = product[2]
                total_price = price * quantity
                total += total_price
                message_text += f"{name}: {quantity} x {price} = {total_price}\n"
        message_text += f"Jami: {total}"

        # Agar original xabar rasm bilan yuborilgan bo'lsa, uni edit_caption orqali yangilang
        if callback_query.message.photo:
            await callback_query.message.edit_caption(caption=message_text, reply_markup=plusminus)
        else:
            # Agar original xabar matn bo'lsa, uni edit_text orqali yangilang
            await callback_query.message.edit_text(text=message_text, reply_markup=plusminus)
    else:
        await callback_query.answer("Sizning savatingiz bo'sh.", show_alert=True)

    
@router_user.callback_query(lambda c: c.data == 'increase')
async def increase_quantity(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    product_id = db_pro.current_product_id
    db_pro.add_to_cart(db_pro.shopping_carts, user_id, product_id, quantity=1)
    await callback_query.answer("Miqdor oshirildi")
    # Savat ko'rinishini yangilash
    await show_cart(callback_query)

@router_user.callback_query(lambda c: c.data == 'decrease')
async def decrease_quantity(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    product_id = db_pro.current_product_id
    db_pro.remove_from_cart(db_pro.shopping_carts, user_id, product_id, quantity=1)
    await callback_query.answer("Miqdor kamaytirildi")
    # Savat ko'rinishini yangilash
    await show_cart(callback_query)

@router_user.callback_query(lambda c: c.data == 'tayyor')
async def finish_order(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    cart = db_pro.show_cart(db_pro.shopping_carts, user_id)
    if cart != "Sizning savatingiz bo'sh.":
        # Buyurtmani ma'lumotlar bazasiga yoki boshqa saqlash tizimiga yuborish
        # Misol uchun: order_process(user_id, cart)
        
        # Buyurtma yakunlanganligini foydalanuvchiga yangi xabar yuborish
        await bot.send_message(chat_id=user_id, text="Buyurtmangiz muvaffaqiyatli qabul qilindi. ", reply_markup=buyurtmani_tugatish)
        # Eski xabarni o'chirish
        await callback_query.message.delete()
        await callback_query.answer("Buyurtma qabul qilindi")
    else:
        await callback_query.answer("Savatingiz bo'sh.", show_alert=True)

async def show_products(callback_query_or_message, category: str):
    user_id = getattr(callback_query_or_message, 'from_user', None).id
    chat_id = callback_query_or_message.message.chat.id if user_id is None else user_id
    products = db_pro.select_available_products(category)
    
    if not products:
        await bot.send_message(chat_id=chat_id, text="Ushbu kategoriyada mahsulotlar hozircha mavjud emas.")
        return
    
    for product in products:
        await bot.send_photo(
            chat_id=chat_id,
            photo=product[4],  # Mahsulot rasmi
            caption=f"Mahsulot nomi: {product[1]}\nNarxi: {product[2]} so'm\nSoni: {product[6]}"
            # reply_markup ni qo'shishingiz kerak, agar kerak bo'lsa.
        )

#----------------------Buyurtmani tugatish----------------------------------
    
@router_user.message(F.text == "Buyurtmani tugatish")
async def process_finish_order(msg: Message):
    chat_id = msg.from_user.id
    cart = db_pro.show_cart(db_pro.shopping_carts, chat_id)
    try:
        if cart:  # Agar savat bo'sh emas bo'lsa
            # Narxlarni tiyinga aylantiring (1 sum = 100 tiyin)
            prices = []
            for product_id, quantity in cart.items():
                product = db_pro.select_product_by_id(product_id)
                if product:
                    name, price = product[1], product[2]  # Mahsulot nomi va narxi
                    prices.append(LabeledPrice(label=name, amount=int(price) * quantity * 100))        
            # Umumiy narxni hisoblash
            total_amount = sum(price.amount for price in prices)
            product = db_pro.select_product_by_id(product_id)
            # Fakturani yaratish
            title = product[1]
            description = product[3]
            photo = product[4]
            payload = "Custom-Payload"  # Bu yerni buyurtma identifikatoriga moslashtiring
            provider_token = click_token  # Bu yerni to'lov provayderingiz tokeni bilan almashtiring
            currency = "UZS"

            # To'lov fakturasini yuborish
            await bot.send_invoice(
                chat_id=chat_id,
                title=title,
                description=description,
                payload=payload,
                provider_token=provider_token,
                currency=currency,
                prices=prices,
                photo_url=photo,
                photo_height=600,
                photo_width=600,
                need_name=True,
                need_phone_number=True,
                need_shipping_address=True,
                is_flexible=True
            )
        else:
            await msg.answer("Sizning savatingiz bo'sh.")
    except Exception as e:
        await msg.answer(f"120.000.000 kop xarid qilib bolmaydi!")
        db_pro.shopping_carts[chat_id] = {}

@router_user.shipping_query()
async def shipping_query_handler(query: ShippingQuery):
    city = query.shipping_address.city.lower()
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Biz faqat O'zbekiston uchun yetkazib bera olamiz!")
    elif city in ['tashkent', 'toshkent', 'toshken']:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)

@router_user.pre_checkout_query()
async def pre_ch_q_handler(pre_checkout_query: PreCheckoutQuery):
    chat_id = pre_checkout_query.from_user.id
    cart = db_pro.show_cart(db_pro.shopping_carts, chat_id)
    if cart:
        # Adminlarni bir marta tanlab olamiz, chunki ular har bir mahsulot uchun bir xil bo'ladi.
        admins = db_admins.select_admins()  # Bu yerda asinxron funksiya bo'lishi kerak, agar ma'lumotlar bazasi bilan ishlash asinxron bo'lsa.
        admin_ids = [admin[1] for admin in admins]  # Admin chat_idlarini ro'yxatga olish.

        for product_id, quantity in cart.items():
            # decrement_product_stock asinxron funksiya bo'lgani uchun, uni 'await' yordamida kutamiz.
            await db_pro.decrement_product_stock(bot,product_id, quantity, admin_ids)
        
        # Savatni tozalash
        db_pro.shopping_carts[chat_id] = {}

    # PreCheckoutQueryga javob berish.
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)
    # Foydalanuvchiga xabar yuborish.
    await bot.send_message(chat_id=chat_id, text="Xaridingiz uchun raxmat!")
    
#----------------------CATEGORY----------------------------------
        
@router_user.message(F.text == 'Category🗒')
async def categorys(msg: Message):
    await msg.answer(f"Tanlang:👇", reply_markup=category)


@router_user.callback_query(lambda c: c.data == 'smartfon' or c.data == 'televizor' or c.data == 'noutbuk' or c.data == 'aqlli_soat' or c.data == 'quloqchin' or c.data == 'oyin_pristavka')
async def show_products_by_category(callback: CallbackQuery):
    # Set the current category to 'smartfon'
    if callback.data == 'smartfon':
        db_pro.set_current_category('smartfon')
    elif callback.data == 'televizor':
        db_pro.set_current_category('televizor')
    elif callback.data == 'noutbuk':
        db_pro.set_current_category('noutbuk')
    elif callback.data == 'aqlli_soat':
        db_pro.set_current_category('aqlli_soat')
    elif callback.data == 'quloqchin':
        db_pro.set_current_category('quloqchin')
    elif callback.data == 'oyin_pristavka':
        db_pro.set_current_category('oyin_pristavka')
    
    # Fetch the first product for 'smartfon' category
    product = db_pro.select_product_by_id(db_pro.current_product_id)
    
    # If a product is found, display it
    if product:
        await show_product(callback, product)
    else:
        await callback.answer("Bu kategoriyada mahsulotlar yo'q.", show_alert=True)


@router_user.callback_query(lambda c: c.data == 'next')
async def show_next_product(callback_query: CallbackQuery):
    product = db_pro.select_next_product()
    if product:
        # Mahsulot ma'lumotlarini ko'rsatish
        await show_product(callback_query, product)
    else:
        await callback_query.answer("Bu so'nggi mahsulot.", show_alert=True)

@router_user.callback_query(lambda c: c.data == 'previous')
async def show_previous_product(callback_query: CallbackQuery):
    product = db_pro.select_previous_product()
    if product:
        # Mahsulot ma'lumotlarini ko'rsatish
        await show_product(callback_query, product)
    else:
        await callback_query.answer("Bu birinchi mahsulot.", show_alert=True)

# Ushbu funksiya endi har bir mahsulot uchun alohida xabar jo'natadi
async def show_product(callback_query: CallbackQuery, product):
    # Mahsulot haqidagi ma'lumotlarni olish
    name, price, description, image = product[1], product[2], product[3], product[4]
    await callback_query.message.delete()
    await callback_query.bot.send_photo(
        chat_id=callback_query.from_user.id,
        photo=image,
        caption=f"Mahsulot nomi: <b>{name}</b>\n"
                f"Mahsulot tavsifi: <b>{description}</b>\n"
                f"Mahsulot narxi: <b>{price}</b>",
        reply_markup=nextorprevious
    )

#--------------------------------------Kiyimi-------------------------------
@router_user.callback_query(F.data == 'kiyim')
async def kyim(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Tanlang:👇", reply_markup=kiyim)

@router_user.callback_query(lambda c: c.data == 'ayollar_k' or c.data == 'erkaklar_k' or c.data == 'bolalar')
async def show_products_by_category(callback: CallbackQuery):
    # Set the current category to 'smartfon'
    if callback.data == 'ayollar_k':
        db_pro.set_current_category('ayollar_k')
    elif callback.data == 'erkaklar_k':
        db_pro.set_current_category('erkaklar_k')
    elif callback.data == 'bolalar':
        db_pro.set_current_category('bolalar')
    
    # Fetch the first product for 'smartfon' category
    product = db_pro.select_product_by_id(db_pro.current_product_id)
    
    # If a product is found, display it
    if product:
        await show_product(callback, product)
    else:
        await callback.answer("Bu kategoriyada mahsulotlar yo'q.", show_alert=True)


#--------------------------------------Avto tovar-------------------------------
@router_user.callback_query(F.data == 'avtotovar')
async def avtotovr(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Tanlang:👇", reply_markup=avtotovar)

@router_user.callback_query(lambda c: c.data == 'akkumlyator' or c.data == 'asbob_va_uskuna' or c.data == 'shina_va_diskalar' or c.data == 'avtotovush' or c.data == 'ehtiyot_qism')
async def show_products_by_category(callback: CallbackQuery):
    # Set the current category to 'smartfon'
    if callback.data == 'akkumlyator':
        db_pro.set_current_category('akkumlyator')
    elif callback.data == 'asbob_va_uskuna':
        db_pro.set_current_category('asbob_va_uskuna')
    elif callback.data == 'shina_va_diskalar':
        db_pro.set_current_category('shina_va_diskalar')
    elif callback.data == 'avtotovush':
        db_pro.set_current_category('avtotovush')
    elif callback.data == 'ehtiyot_qism':
        db_pro.set_current_category('ehtiyot_qism')
    
    # Fetch the first product for 'smartfon' category
    product = db_pro.select_product_by_id(db_pro.current_product_id)
    
    # If a product is found, display it
    if product:
        await show_product(callback, product)
    else:
        await callback.answer("Bu kategoriyada mahsulotlar yo'q.", show_alert=True)


#--------------------------------------Poyabzal-------------------------------
@router_user.callback_query(F.data == 'poyabzal')
async def tovar(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Tanlang:👇", reply_markup=poyabzal)

@router_user.callback_query(lambda c: c.data == 'ayollar_p' or c.data == 'qizlar' or c.data == 'erkaklar_p' or c.data == 'ogil_bola' or c.data == 'poyabzal_aksessuarlar')
async def show_products_by_category(callback: CallbackQuery):
    # Set the current category to 'smartfon'
    if callback.data == 'ayollar_p':
        db_pro.set_current_category('ayollar_p')
    elif callback.data == 'qizlar':
        db_pro.set_current_category('qizlar')
    elif callback.data == 'erkaklar_p':
        db_pro.set_current_category('erkaklar_p')
    elif callback.data == 'ogil_bola':
        db_pro.set_current_category('ogil_bola')
    elif callback.data == 'poyabzal_aksessuarlar':
        db_pro.set_current_category('poyabzal_aksessuarlar')
    
    # Fetch the first product for 'smartfon' category
    product = db_pro.select_product_by_id(db_pro.current_product_id)
    
    # If a product is found, display it
    if product:
        await show_product(callback, product)
    else:
        await callback.answer("Bu kategoriyada mahsulotlar yo'q.", show_alert=True)


#--------------------------------------Maishiy Texnika-------------------------------
@router_user.callback_query(F.data == 'maishiy_texnika')
async def tovar(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Tanlang:👇", reply_markup=maishiy_texnika)

@router_user.callback_query(lambda c: c.data == 'gozallik' or c.data == 'oshxona_buyumlari' or c.data == 'katta_maishiy_texnika' or c.data == 'iqlim' or c.data == 'uy_uchun_texnika')
async def show_products_by_category(callback: CallbackQuery):
    # Set the current category to 'smartfon'
    if callback.data == 'gozallik':
        db_pro.set_current_category('gozallik')
    elif callback.data == 'oshxona_buyumlari':
        db_pro.set_current_category('oshxona_buyumlari')
    elif callback.data == 'katta_maishiy_texnika':
        db_pro.set_current_category('katta_maishiy_texnika')
    elif callback.data == 'iqlim':
        db_pro.set_current_category('iqlim')
    elif callback.data == 'uy_uchun_texnika':
        db_pro.set_current_category('uy_uchun_texnika')
    
    # Fetch the first product for 'smartfon' category
    product = db_pro.select_product_by_id(db_pro.current_product_id)
    
    # If a product is found, display it
    if product:
        await show_product(callback, product)
    else:
        await callback.answer("Bu kategoriyada mahsulotlar yo'q.", show_alert=True)

#--------------------------------------Ortga-------------------------------
@router_user.callback_query(F.data == 'ortga')
async def ortga(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Tanlang:👇", reply_markup=category)