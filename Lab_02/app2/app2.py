from flask import Flask, render_template, request, url_for, make_response
import operator as op

app2 = Flask(__name__)
application = app2

operations = ['+', '-', '*', '/']
operations_function = { '+' : op.add, '-' : op.sub, '*' : op.mul, '/' : op.truediv }


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


#@app2.route('/calc')
#def calc():
#    try:
#        title = 'Калькулятор'
#        result = None
#        error_msg = None
#        op1 = float(request.args.get('operand1', 0))
#        op2 = float(request.args.get('operand2', 0))
#        operation = request.args.get('operation')
#        if operation == '+':
#            result = op1 + op2
#        elif operation == '-':
#            result = op1 - op2
#        elif operation == '*':
#            result = op1 * op2
#        elif operation == '/':
#            result = op1 / op2
#    except ValueError:
#        error_msg = "Пожалуйста, вводите только числа"
#    except ZeroDivisionError:
#        error_msg = "На ноль делить нельзя"
#
#    return render_template('calc.html', title=title,  operations=operations, result=result, error_msg=error_msg)

@app2.route('/calc')
def calc():
    title = 'Калькулятор'
    try:
        result = None
        error_msg = ''
        op1 = float(request.args.get('operand1', 0))
        op2 = float(request.args.get('operand2', 0))
        f = operations_function[request.args.get('operation')]
        result = f(op1, op2)
    except ValueError:
        error_msg = "Пожалуйста, вводите только числа"
    except ZeroDivisionError:
        error_msg = "На ноль делить нельзя"
    except KeyError:
        error_msg = "Недопустимая операция"
    if op1 == 0 and op2 == 0:
        error_msg = ''
    return render_template('calc.html', title=title,  operations=operations, result=result, error_msg=error_msg)

@app2.route('/tel', methods=['GET', 'POST'])
def tel():
    title = 'Проверка телефона'
    teleph = request.args.get('telephone', '')
    telephone = request.args.get('telephone', '')
    numbers = 0
    signs = 0
    msg_error = ''
    length = 0
    new_teleph = ''
    right_teleph = ''

    if request.method == 'POST':
        teleph = str(request.form['telephone'])
        telephone = str(request.form['telephone'])
        if teleph != '': 
            teleph = teleph.replace(' ', '')
            length = len(teleph)
            for numb in teleph:
                if numb in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    numbers = numbers + 1
                if numb in ['(', ')', '-', '.', '+']:
                    signs = signs + 1
            if numbers + signs != length:
                msg_error = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
            if ((teleph[0] == '+' and teleph[1] == '7') or teleph[0] == '8') and (numbers not in [10, 11]):
                msg_error = 'Недопустимый ввод. Неверное количество цифр.'
            if numbers not in [10, 11]:
                msg_error = 'Недопустимый ввод. Неверное количество цифр.'
            if msg_error == '':
                new_teleph = [int(num) for num in filter(lambda num: num.isnumeric(), teleph)]
                if new_teleph[0] == 7:
                    new_teleph[0] = 8
                for t in new_teleph:
                    right_teleph = right_teleph + str(t)
                right_teleph = right_teleph[0] + '-' + right_teleph[1:4] + '-' + right_teleph[4:7] + '-' + right_teleph[7:9] + '-'+ right_teleph[9:11]
    else:
        telephone=str(request.args.get('telephone', ''))

    return render_template('tel.html', title=title, teleph=teleph, msg_error=msg_error, telephone=telephone, new_teleph=new_teleph, right_teleph=right_teleph)
