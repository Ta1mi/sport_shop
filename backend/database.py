import psycopg2
import json
from hashlib import sha256
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime

class Database:
    def __init__(self, config_path: str = 'backend/config.json'):
        """Инициализация подключения к PostgreSQL"""
        self.config_path = config_path
        self.conn = None
        self._connect()

    def _connect(self):
        """Установка соединения с базой данных"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.conn = psycopg2.connect(
                host=config['db']['host'],
                dbname=config['db']['database'],
                user=config['db']['user'],
                password=config['db']['password'],
                port=config['db']['port'],
                connect_timeout=5
            )
            print("✅ Подключение к PostgreSQL успешно установлено")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            raise

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            print("🔌 Подключение к базе данных закрыто")

    def execute(self, query: str, params: Tuple = None, fetch: bool = False) -> Optional[List[Dict]]:
        """Универсальный метод выполнения запросов"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
                self.conn.commit()
                return None
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"❌ Ошибка выполнения запроса: {e}")
            raise

    def init_db(self):
        """Инициализация структуры базы данных"""
        try:
            # Создание таблицы пользователей
            self.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(64) NOT NULL,
                    full_name VARCHAR(100),
                    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'manager', 'sales')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Создание таблицы товаров
            self.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    quantity INTEGER NOT NULL,
                    description TEXT,
                    supplier VARCHAR(100),
                    image_url VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Создание администратора по умолчанию
            admin_password = sha256("admin123".encode()).hexdigest()
            self.execute(
                "INSERT INTO users (username, password_hash, full_name, role) "
                "VALUES (%s, %s, %s, %s) ON CONFLICT (username) DO NOTHING",
                ("admin", admin_password, "Administrator", "admin")
            )
            
            print("✅ База данных успешно инициализирована")
            return True
        except Exception as e:
            print(f"❌ Ошибка при инициализации БД: {e}")
            return False

    def get_all_tables(self) -> List[str]:
        """Получение списка всех таблиц в БД"""
        try:
            result = self.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public'",
                fetch=True
            )
            return [table['table_name'] for table in result] if result else []
        except Exception as e:
            print(f"❌ Ошибка при получении списка таблиц: {e}")
            return []

    def create_user(self, username: str, password: str, full_name: str, role: str) -> bool:
        """Создание нового пользователя"""
        password_hash = sha256(password.encode()).hexdigest()
        return self.execute(
            "INSERT INTO users (username, password_hash, full_name, role) "
            "VALUES (%s, %s, %s, %s)",
            (username, password_hash, full_name, role)
        ) is not None

    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получение пользователя по ID"""
        return self.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,),
            fetch=True
        )[0] if self.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,),
            fetch=True
        ) else None

    def add_product(self, product_data: Dict) -> Optional[int]:
        """Добавление нового товара"""
        result = self.execute(
            "INSERT INTO products (name, category, price, quantity, description, supplier, image_url) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (
                product_data['name'],
                product_data['category'],
                product_data['price'],
                product_data['quantity'],
                product_data.get('description'),
                product_data.get('supplier'),
                product_data.get('image_url')
            ),
            fetch=True
        )
        return result[0]['id'] if result else None

    def get_all_products(self) -> List[Dict]:
        """Получение всех товаров"""
        return self.execute(
            "SELECT * FROM products ORDER BY name",
            fetch=True
        ) or []

    def __enter__(self):
        """Поддержка контекстного менеджера"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие соединения"""
        self.close()


if __name__ == "__main__":
    # Тестирование работы класса
    with Database() as db:
        # Инициализация БД
        db.init_db()
        
        # Вывод списка таблиц
        print("Таблицы в БД:", db.get_all_tables())
        
        # Пример добавления товара
        product_id = db.add_product({
            'name': 'Баскетбольный мяч',
            'category': 'Баскетбол',
            'price': 1899.99,
            'quantity': 15,
            'description': 'Профессиональный мяч',
            'supplier': 'Spalding'
        })
        print(f"Добавлен товар с ID: {product_id}")
        
        # Получение списка товаров
        products = db.get_all_products()
        print("Список товаров:", products)