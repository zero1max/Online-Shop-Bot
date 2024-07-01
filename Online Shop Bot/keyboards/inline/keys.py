from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

category = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Elektronika', callback_data='elektronika'), InlineKeyboardButton(text='Kiyim', callback_data='kiyim')],
        [InlineKeyboardButton(text='Avtotovar', callback_data='avtotovar'), InlineKeyboardButton(text='Poyabzal', callback_data='poyabzal')],
        [InlineKeyboardButton(text='Maishiy Texnika', callback_data='maishiy_texnika')]
    ]
)

elektronika = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Smartfon', callback_data="smartfon"), InlineKeyboardButton(text='Aqlli soat', callback_data='aqlli_soat')],
        [InlineKeyboardButton(text='Noutbuk', callback_data='noutbuk'), InlineKeyboardButton(text='Quloqchin', callback_data='quloqchin')],
        [InlineKeyboardButton(text='Televizor', callback_data='televizor'), InlineKeyboardButton(text="O'yin pristavka", callback_data="oyin_pristavka")],
        [InlineKeyboardButton(text='Ortga qaytish🔙', callback_data='ortga')]
    ]
)

kiyim = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ayollar', callback_data='ayollar_k'), InlineKeyboardButton(text='Erkaklar', callback_data='erkaklar_k')],
        [InlineKeyboardButton(text='Bolalar', callback_data='bolalar')],
        [InlineKeyboardButton(text='Ortga qaytish🔙', callback_data='ortga')]
    ]
)

avtotovar = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Akkumlyatot', callback_data='akkumlyator'), InlineKeyboardButton(text='Avtotovush', callback_data='avtotovush')],
        [InlineKeyboardButton(text='Asbob va uskunalar', callback_data='asbob_va_uskuna'), InlineKeyboardButton(text='Ehtiyot qismlar', callback_data='ehtiyot_qism')],
        [InlineKeyboardButton(text='Shina va diskalar', callback_data='shina_va_diskalar')],
        [InlineKeyboardButton(text='Ortga qaytish🔙', callback_data='ortga')]
    ]
)

poyabzal = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ayollar', callback_data='ayollar_p'), InlineKeyboardButton(text='Erkaklar', callback_data='erkaklar_p')],
        [InlineKeyboardButton(text='Qizlar', callback_data='qizlar'), InlineKeyboardButton(text="O'g'il bola", callback_data='ogil_bola')],
        [InlineKeyboardButton(text='Poyabzal aksessuarlar', callback_data='poyabzal_aksessuarlar')],
        [InlineKeyboardButton(text='Ortga qaytish🔙', callback_data='ortga')]
    ]
)

maishiy_texnika = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Go'zallik", callback_data='gozallik'), InlineKeyboardButton(text='Iqlim', callback_data='iqlim')],
        [InlineKeyboardButton(text='Oshxona buyumlari', callback_data='oshxona_buyumlari'), InlineKeyboardButton(text='Uy uchun texnika',callback_data='uy_uchun_texnika')],
        [InlineKeyboardButton(text='Katta maishiy texnika', callback_data='katta_maishiy_texnika')],
        [InlineKeyboardButton(text='Ortga qaytish🔙', callback_data='ortga')]
    ]
)

nextorprevious = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data='previous'), InlineKeyboardButton(text='➡️', callback_data='next')],
        [InlineKeyboardButton(text="Savatga qo'shish📥", callback_data='savesavat')],
        [InlineKeyboardButton(text='Savat🛒', callback_data='savat')]
    ]
)

plusminus = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='➖', callback_data='decrease'), InlineKeyboardButton(text='➕', callback_data='increase')],
        [InlineKeyboardButton(text="Tayyor✅", callback_data='tayyor')]
    ]
)