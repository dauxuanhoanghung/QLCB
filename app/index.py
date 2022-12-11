import cloudinary
from flask import render_template, request, redirect, session, jsonify
from app import app, dao, login_mana, admin, decorators
from flask_login import login_user, logout_user, login_required, current_user
from app import utils
from app.models import UserRoleEnum


@app.route('/')
def index():
    apts = dao.get_all_airport()
    flights = dao.get_all_flight()
    return render_template('/index.html', airports=apts,
                           flights=flights)


@app.route('/login', methods=['get', 'post'])
@decorators.anonymous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            url_next = request.args.get('next')
            return redirect(url_next if url_next else '/')
    return render_template('/login.html')


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']
    u = dao.auth_user(username=username, password=password, user_role=UserRoleEnum.ADMIN)
    if u:
        login_user(user=u)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        if dao.check_username(username=username):
            return render_template('/register.html', err_msg='username đã tồn tại')
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
    return render_template('/register.html', err_msg=err_msg)


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/')


@app.route('/booking')
def booking():
    airport = dao.get_all_airport()
    return render_template('/booking.html', airport=airport)


@app.route('/booking', methods=['post'])
def load_flights():
    from_airport = int(request.json['fromAirport'])
    to_airport = int(request.json['toAirport'])
    start_day = request.json['trip-start']
    flights = dao.get_flight(from_airport=from_airport, to_airport=to_airport, start_day=start_day)
    data = []
    for f in flights:
        data.append({
            "id": f.id,
            "takeoff_time": f.takeoff_time,
            "flying_time": str(f.flying_time),
            "base_price": f.base_price,
            "flight_route": {
                "departure_airport": f.flight_route.departure_airport.location,
                "arrival_airport": f.flight_route.arrival_airport.location,
                "departure_img": f.flight_route.departure_airport.picture,
                "arrival_img": f.flight_route.arrival_airport.picture
            }
        })
    return jsonify(data)


@app.route('/flight/<flight_id>')
def detail(flight_id):
    ticket_type = dao.get_all_ticket_type()
    flight = dao.get_flight_by_id(flight_id)
    return render_template('/details.html', f=flight, tk_type=ticket_type, role=UserRoleEnum)


@app.route('/flight/<flight_id>', methods=['POST'])
def save_ticket(flight_id):
    name = request.form['name']
    identity = request.form['identity_number']
    phone = request.form['phone_number']
    f = dao.get_flight_by_id(flight_id)
    tk_type = int(request.form['pricing'])
    dao.save_ticket(ticket_type_id=tk_type, ticket_price=f.base_price + (2 - tk_type) * 100000,
                    flight_id=int(flight_id))
    if current_user.user_role.__eq__(UserRoleEnum.USER):
        return redirect('/')
    else:
        return redirect('/admin')


@login_mana.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)