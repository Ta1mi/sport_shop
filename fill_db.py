from backend.database import Database
from hashlib import sha256

def fill_sample_data(db):
    """Заполнение базы тестовыми данными"""
    try:
        # Добавляем пользователей (пропускаем если уже существуют)
        users = [
            ("manager1", "manager123", "Иван Менеджеров", "manager"),
            ("seller1", "seller123", "Анна Продавцова", "sales")
        ]
        
        for username, password, full_name, role in users:
            # Проверяем существование пользователя перед добавлением
            existing_user = db.execute(
                "SELECT id FROM users WHERE username = %s",
                (username,),
                fetch=True
            )
            if not existing_user:
                db.create_user(username, password, full_name, role)
                print(f"✅ Пользователь {username} добавлен")
            else:
                print(f"ℹ️ Пользователь {username} уже существует, пропускаем")

        # Добавляем товары (добавляем даже если существуют, так как нет уникального ограничения на имя)
        products = [
            {"name": "Футбольный мяч", "category": "Футбол", "price": 2499.99, 
             "quantity": 50, "description": "Официальный мяч FIFA", "supplier": "Nike"},
            {"name": "Баскетбольный мяч", "category": "Баскетбол", "price": 1899.99,
             "quantity": 30, "description": "Размер 7, профессиональный", "supplier": "Spalding"},
            {"name": "Беговая дорожка", "category": "Фитнес", "price": 45999.99,
             "quantity": 5, "description": "Профессиональная модель", "supplier": "Torneo"},
            {"name": "Теннисная ракетка", "category": "Теннис", "price": 8999.99,
             "quantity": 15, "description": "Карбоновая ракетка", "supplier": "Wilson"}
        ]
        
        for product in products:
            db.add_product(product)
            print(f"✅ Товар {product['name']} добавлен")

        print("✅ Тестовые данные успешно обработаны")
        return True

    except Exception as e:
        print(f"❌ Ошибка при заполнении тестовых данных: {e}")
        return False

if __name__ == "__main__":
    with Database() as db:
        # Инициализация БД (создаст таблицы если их нет)
        db.init_db()
        
        # Заполнение тестовыми данными
        fill_sample_data(db)