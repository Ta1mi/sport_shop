import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from hashlib import sha256

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Database

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
app.secret_key = '2a1b0c9d'  # Из config.json

db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.execute(
            "SELECT * FROM users WHERE username = %s AND password_hash = %s",
            (username, sha256(password.encode()).hexdigest()),
            fetch=True
        )
        
        if user:
            session['user'] = {
                'id': user[0]['id'],
                'username': user[0]['username'],
                'full_name': user[0]['full_name'],
                'role': user[0]['role']
            }
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/products')
def products():
    category = request.args.get('category')
    query = "SELECT * FROM products"
    params = ()
    
    if category:
        query += " WHERE category = %s"
        params = (category,)
    
    products = db.execute(query + " ORDER BY name", params, fetch=True) or []
    return render_template('products.html', products=products, current_category=category)

@app.route('/admin')
def admin():
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('login'))
    
    products = db.execute("SELECT * FROM products ORDER BY name", fetch=True) or []
    users = db.execute("SELECT id, username, full_name, role FROM users ORDER BY username", fetch=True) or []
    
    return render_template('admin.html', products=products, users=users)

@app.route('/api/products/featured')
def featured_products():
    products = db.execute("SELECT * FROM products ORDER BY RANDOM() LIMIT 4", fetch=True) or []
    return jsonify(products)

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Требуется авторизация"})
    
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # Здесь можно добавить логику добавления в корзину
    return jsonify({
        "success": True,
        "message": "Товар добавлен в корзину",
        "cart_count": 1  # Временное значение
    })

@app.route('/api/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email or '@' not in email:
            return jsonify({"success": False, "message": "Пожалуйста, введите корректный email"}), 400
        
        existing = db.execute(
            "SELECT id FROM newsletter_subscribers WHERE email = %s",
            (email,),
            fetch=True
        )
        
        if existing:
            return jsonify({"success": False, "message": "Этот email уже подписан"}), 400
        
        db.execute(
            "INSERT INTO newsletter_subscribers (email, subscribed_at) VALUES (%s, NOW())",
            (email,)
        )
        
        return jsonify({"success": True, "message": "Спасибо за подписку!"})
    
    except Exception as e:
        print(f"Ошибка при подписке: {e}")
        return jsonify({"success": False, "message": "Ошибка сервера"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)