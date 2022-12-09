from flask import session, redirect,  url_for
from flask import render_template, request, redirect, session, jsonify
from app import app, dao, login_mana, admin
from flask_login import login_user, logout_user, login_required
from app import utils

import cloudinary.uploader


@app.route('/')
def index():
    apts = dao.get_all_airport()
    flights = dao.get_flight()
    return render_template('/index.html', airports=apts,
                           flights=flights)


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            url_next = request.args.get('next')
            return redirect(url_next if url_next else '/')

    return render_template('login.html')


@app.route('/register', methods=['get', 'post'])
def register_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        identity_number = request.form.get('identity_number')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        avatar_path = None
        if password.__eq__(confirm):
            # upload cloudinary
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']
            # add user
            try:
                dao.register(name=name,
                             username=username,
                             password=password,
                             email=email,
                             phone_number=phone_number,
                             identity_number=identity_number,
                             avatar=avatar_path)
            except Exception as ex:
                err_msg = " He thong co loi " + str(ex)
            else:
                return redirect('/login')
        else:
            err_msg = 'password, no match!!'
    return render_template('register.html', err_msg=err_msg)


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/')

@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@login_mana.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
