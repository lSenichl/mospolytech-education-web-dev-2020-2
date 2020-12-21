from flask import Blueprint, render_template, request, url_for, make_response, session, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from app import mysql

bp = Blueprint('visits', __name__, url_prefix='/visits')

@bp.route('/logs')
def logs():
    query = '''
    SELECT visit_logs.*, users.first_name, users.last_name, users.middle_name
    FROM users RIGHT OUTER JOIN visit_logs ON users.id = visit_logs.user_id
    ORDER BY visit_logs.created_at DESC;
    '''
    cursor = mysql.connection.cursor(named_tuple=True)
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    return render_template('visits/logs.html', records=records)


@bp.route('/stat/users')
def users_stat():
    query = '''
    SELECT users.id, users.first_name, users.last_name, users.middle_name, count(*) AS count
    FROM users RIGHT OUTER JOIN visit_logs ON users.id = visit_logs.user_id
    GROUP BY users.id
    ORDER BY count DESC;
    '''
    cursor = mysql.connection.cursor(named_tuple=True)
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    return render_template('visits/users.html', records=records)


@bp.route('/stat/pages')
def pages_stat():
    query = '''
    SELECT visit_logs.*, users.first_name, users.last_name, users.middle_name
    FROM users RIGHT OUTER JOIN visit_logs ON users.id = visit_logs.user_id
    ORDER BY visit_logs.created_at DESC;
    '''
    cursor = mysql.connection.cursor(named_tuple=True)
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    return render_template('visits/pages.html', records=records)