from flask import Flask, render_template, request, url_for, make_response

app2 = Flask(__name__)
application = app2

operations = ['+', '-', '*', '/']


@app2.route('/')
def index():
    return render_template('index.html')


@app2.route('/url_page')
def url_page():
    title = 'URL'
    return render_template('url_page.html', title=title)


@app2.route('/headers')
def headers():
    title = 'Заголовки запроса'
    return render_template('headers.html', title=title)


@app2.route('/cookies')
def cookies():
    title = 'Печеньки'
    resp = make_response(render_template('cookies.html', title=title))
    if 'username' in request.cookies:
        resp.set_cookie('username', 'some name', expires=0)
    else:
        resp.set_cookie('username', 'some name')
    return resp


@app2.route('/form_params', methods=['GET', 'POST'])
def form_params():
    title = 'Параметры формы'
    return render_template('form_params.html', title=title)


@app2.route('/calc')
def calc():
    try:
        title = 'Калькулятор'
        op1 = float(request.args.get('operand1'))
        op2 = float(request.args.get('operand2'))
        operation = request.args.get('operation')
        result = None
        error_msg = None
        if operation == '+':
            result = op1 + op2
        elif operation == '-':
            result = op1 - op2
        elif operation == '*':
            result = op1 * op2
        elif operation == '/':
            result = op1 / op2
    except TypeError:
        error_msg = "Пожалуйста, вводите только числа"
    

    return render_template('calc.html', title=title,  operations=operations, result=result, error_msg=error_msg)
