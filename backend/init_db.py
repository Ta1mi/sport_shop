from database import Database

if __name__ == "__main__":
    db = Database()
    db.init_db()
    print("База данных успешно инициализирована!")
    db.close()
    from database import Database

from database import Database

if __name__ == "__main__":
    try:
        db = Database()
        if db.conn:
            db.init_db()
    finally:
        db.close()