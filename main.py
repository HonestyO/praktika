from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'my_secret_key'  

# Настройки базы данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:(PASSWORD)@localhost:5432/samrat'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Настройки Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(80))


# Определение функции user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Страница "О Нас"
@app.route('/about')
def about():
    return render_template('about.html')


# Страница "Часто задаваемые вопросы"
@app.route('/faq')
def faq():
    return render_template('faq.html')


# Страница "Контакты"
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash('Please enter all the fields!', 'error')
            return redirect(url_for('register'))

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not user.password == password:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('login'))

        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')


# Выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
