from backend.database import Database

def fill_sample_data(db):
    """Заполнение базы тестовыми данными"""
    try:
        # Добавляем пользователей
        users = [
            ("manager1", "manager123", "Иван Менеджеров", "manager"),
            ("seller1", "seller123", "Анна Продавцова", "sales")
        ]
        
        for username, password, full_name, role in users:
            db.create_user(username, password, full_name, role)

        # Добавляем товары
        products = [
            {"name": "Футбольный мяч", "category": "Футбол", "price": 2499.99, 
             "quantity": 50, "description": "Официальный мяч FIFA", "supplier": "Nike"},
            {"name": "Баскетбольный мяч", "category": "Баскетбол", "price": 1899.99,
             "quantity": 30, "description": "Размер 7, профессиональный", "supplier": "Spalding"}
        ]
        
        for product in products:
            db.add_product(product)

        print("✅ Тестовые данные успешно добавлены")
        return True

    except Exception as e:
        print(f"❌ Ошибка при заполнении тестовых данных: {e}")
        return False

if __name__ == "__main__":
    with Database() as db:
        db.init_db()  # Создаст таблицы, если их нет
        fill_sample_data(db)  # Заполнит тестовыми данными