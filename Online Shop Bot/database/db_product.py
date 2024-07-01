import sqlite3
from dataclasses import dataclass

@dataclass
class Database_Product:
    connect: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None
    current_product_id: str = None
    current_category: str = None
    shopping_carts: dict = None


    def __post_init__(self):
        self.connect = sqlite3.connect('product.db')
        self.cursor = self.connect.cursor()
        self.shopping_carts = {}
        self.current_product_id = 0


    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            category TEXT NOT NULL,
            soni INTEGER NOT NULL
        )''')
        self.connect.commit()

    def add_products(self, name, price, description, image, category, soni):
        self.cursor.execute("INSERT INTO products (name, price, description, image, category, soni) VALUES (?, ?, ?, ?, ?,?)", (name, price, description, image, category, soni))
        self.connect.commit()

    def select_products(self):
        self.cursor.execute("SELECT * FROM products") 
        return self.cursor.fetchall()

    def select_product(self, category):
        self.cursor.execute("SELECT * FROM products WHERE category = ?", (category,))
        return self.cursor.fetchall()
    
    def select_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return self.cursor.fetchone()
    
    def delete_one(self, id, value):
        self.cursor.execute(f"DELETE FROM products WHERE {id}=?",(value,))
        self.connect.commit()

    async def decrement_product_stock(self,bot,  product_id, quantity, admin_chat_ids):
        # Mahsulot sonini o'qish
        self.cursor.execute("SELECT soni FROM products WHERE id = ?", (product_id,))
        stock = self.cursor.fetchone()[0]

        # Yangi sonni hisoblash
        new_stock = stock - quantity

        # Mahsulot sonini yangilash
        self.cursor.execute("UPDATE products SET soni = ? WHERE id = ?", (new_stock, product_id))
        self.connect.commit()

        # Agar mahsulot soni 0 ga teng bo'lsa, adminlarga xabar berish
        if new_stock <= 0:
            product_info = self.select_product_by_id(product_id)
            product_name = product_info[1]
            message = f"Diqqat: '{product_name}' mahsuloti tugadi."
            for admin_chat_id in admin_chat_ids:
                # Bot instansini o'tkazib yubormang, `self.bot` kabi biror narsa bo'lishi kerak
                await bot.send_message(chat_id=admin_chat_id, text=message)


    def update_product(self,id,product_name,description,price,image,category,soni):
        self.cursor.execute("UPDATE products SET product_name = ?, description = ?, price = ?, image = ?, category = ?, soni = ? WHERE id = ?",
                            (product_name,description,price,image,id, category, soni)
                            ) 
        self.connect.commit()

    def select_available_products(self, category):
        self.cursor.execute("SELECT * FROM products WHERE soni > 0 AND category = ?", (category,))
        return self.cursor.fetchall()


    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()

    def set_current_category(self, category):
        self.current_category = category
        self.current_product_id = self.get_min_product_id_for_category(category)

    def get_min_product_id_for_category(self, category):
        self.cursor.execute("SELECT MIN(id) FROM products WHERE category=?", (category,))
        min_id = self.cursor.fetchone()[0]
        return min_id if min_id is not None else 0

    def get_max_product_id_for_category(self, category):
        self.cursor.execute("SELECT MAX(id) FROM products WHERE category=?", (category,))
        max_id = self.cursor.fetchone()[0]
        return max_id if max_id is not None else 0

    def select_next_product(self):
        # Increment the current product ID
        self.current_product_id += 1
        
        # Select the product by the new ID
        product = self.select_product_by_id(self.current_product_id)
        
        # If there is no next product in the category, wrap around to the first product
        if not product and self.current_category:
            self.current_product_id = self.get_min_product_id_for_category(self.current_category)
            product = self.select_product_by_id(self.current_product_id)
        
        return product

    def select_previous_product(self):
        # Decrement the current product ID
        self.current_product_id -= 1
        
        # Select the product by the new ID
        product = self.select_product_by_id(self.current_product_id)
        
        # If there is no previous product in the category, wrap around to the last product
        if not product and self.current_category:
            self.current_product_id = self.get_max_product_id_for_category(self.current_category)
            product = self.select_product_by_id(self.current_product_id)
        
        return product

    @staticmethod
    def add_to_cart(shopping_carts, user_id, product_id, quantity=1):
        if user_id not in shopping_carts:
            shopping_carts[user_id] = {}
        cart = shopping_carts[user_id]
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
    
    @staticmethod
    def remove_from_cart(shopping_carts, user_id, product_id, quantity=1):
        if user_id in shopping_carts and product_id in shopping_carts[user_id]:
            cart = shopping_carts[user_id]
            if cart[product_id] > quantity:
                cart[product_id] -= quantity
            else:
                del cart[product_id]
    
    @staticmethod
    def show_cart(shopping_carts, user_id):
        if user_id in shopping_carts:
            return shopping_carts[user_id]
        else:
            return "Sizning savatingiz bo'sh."