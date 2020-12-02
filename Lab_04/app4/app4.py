from flask import Flask, render_template, request, url_for, make_response, session, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from mysql_db import MySQL

login_manager = LoginManager()

app4 = Flask(__name__)
application = app4

app4.config.from_pyfile('config.py')

mysql = MySQL(app4)

login_manager.init_app(app4)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа необходимо пройти процедуру аутентификации.'
login_manager.login_message_category = 'warning'


class User(UserMixin):
    def __init__(self, user_id, login):
        super().__init__()
        self.id = user_id
        self.login = login


@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(named_tuple=True)
    cursor.execute('SELECT * FROM users WHERE id = %s;', (user_id,))
    db_user = cursor.fetchone()
    cursor.close()
    if db_user:
        return User(user_id=db_user.id, login=db_user.login)
    return None


@app4.route('/')
def index():
    return render_template('index.html')


@app4.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'
        if login and password:
            cursor = mysql.connection.cursor(named_tuple=True)
            cursor.execute(
                'SELECT * FROM users WHERE login = %s AND password_hash = SHA2(%s, 256);', (login, password))
            db_user = cursor.fetchone()
            cursor.close()
            if db_user:
                user = User(user_id=db_user.id, login=db_user.login)
                login_user(user, remember=remember_me)

                flash('Вы успешно аутентифицированы', 'success')

                next = request.args.get('next')

                return redirect(next or url_for('index'))
        flash('Введены неверные логин и/или пароль', 'danger')
    return render_template('login.html')


@app4.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
