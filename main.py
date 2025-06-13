import sys
import json
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from backend.app import app as flask_app
import threading

def run_flask():
    with open('backend/config.json') as f:
        config = json.load(f)
    flask_app.run(port=config['app']['port'], use_reloader=False)

if __name__ == "__main__":
    # Запуск Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Создание Qt-приложения с веб-интерфейсом
    qt_app = QApplication(sys.argv)
    
    browser = QWebEngineView()
    browser.setWindowTitle("Спортивный магазин")
    browser.resize(1024, 768)
    
    with open('backend/config.json') as f:
        config = json.load(f)
    
    browser.setUrl(QUrl(f"http://localhost:{config['app']['port']}"))
    browser.show()
    
    sys.exit(qt_app.exec())