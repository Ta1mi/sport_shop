from flask import Flask, render_template
from backend.database import Database

app = Flask(__name__, 
            static_folder='../frontend/static',
            template_folder='../frontend/templates')

# Инициализация БД при старте
db = Database()
print("✅ Подключение к PostgreSQL успешно установлено")
print("Таблицы в БД:", db.get_all_tables())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    