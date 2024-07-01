import asyncio
import logging
import sys

from loader import dp,bot, db_pro, db_user, db_admins
import handlers

async def main():
    await dp.start_polling(bot)
    db_admins.close()
    db_pro.close()
    db_user.close()
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())