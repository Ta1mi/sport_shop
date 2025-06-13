import os
import sys
from flask import Flask, render_template

# Добавляем путь к папке backend в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database  # Теперь импорт должен работать

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')

# Инициализация БД
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)