from flask import session
from flask import render_template, request, redirect, session, jsonify
from app import app, dao, login_mana
from flask_login import login_user, logout_user, login_required
from app import utils


@app.route('/')
def index():
    apts = dao.get_all_airport()
    flights = dao.get_flight()
    return render_template('/index.html', airports=apts,
                           flights=flights)


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    return render_template('/login.html')


@app.route('/register', methods=['get', 'post'])
def register_my_user():
    return render_template('/register.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/')


@login_mana.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)