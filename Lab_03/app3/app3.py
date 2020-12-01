from flask import Flask, render_template, request, url_for, make_response, session, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

login_manager = LoginManager()

app3 = Flask(__name__)
application = app3

login_manager.init_app(app3)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа необходимо пройти процедуру аутентификации.'
login_manager.login_message_category = 'warning'

app3.config.from_pyfile('config.py')

def get_users():
    return [{'user_id': '1', 'login': 'user', 'password': 'qwerty'}]

class User(UserMixin):
    def __init__(self, user_id, login, password):
        super().__init__()
        self.id = user_id
        self.login = login
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    for user in get_users():
        if user['user_id'] == user_id:
            return User(**user)
    return None

@app3.route('/')
def index():
    return render_template('index.html')

@app3.route('/visits')
def visits():
    if session.get('visits'):
        session['visits'] += 1
    else:
        session['visits'] = 1
    return render_template('visits.html')


@app3.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'
        if login and password:
            for user in get_users():
                if user['login'] == login and user['password'] == password:
                    user_object = User(**user)
                    login_user(user_object, remember=remember_me)

                    flash('Вы успешно аутентифицированы', 'success')

                    next = request.args.get('next')

                    return redirect(next or url_for('index'))
        flash('Введены неверные логин и/или пароль', 'danger')
    return render_template('login.html')

@app3.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app3.route('/secret_page')
@login_required
def secret_page():
    return render_template('secret_page.html')