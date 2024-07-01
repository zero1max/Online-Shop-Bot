from aiogram import Dispatcher , Router, Bot
from aiogram.enums import ParseMode
from database.db_product import Database_Product
from database.db_user import Database_Users
from database.asosiy_admin import Database_Admins

TOKEN = "YOUR_TOKEN"
CLICK_TOKEN = "YOUR_CLICK_TOKEN"

db_pro = Database_Product()
db_user = Database_Users()
db_admins = Database_Admins()
dp = Dispatcher()
router_asosiy = Router()
router_admin = Router()
router_user = Router()
click_token = CLICK_TOKEN
bot = Bot(token=TOKEN)
dp.include_router(router=router_asosiy)
dp.include_router(router=router_admin)
dp.include_router(router=router_user)
