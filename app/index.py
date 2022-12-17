from app import app, dao, login_mana, admin, decorators, controllers


app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/login', 'login_my_user', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/login-admin', 'login_admin', controllers.login_admin, methods=['post'])
app.add_url_rule('/register', 'register_my_user', controllers.register_my_user, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout_my_user', controllers.logout_my_user)
app.add_url_rule('/booking', 'booking', controllers.booking)
app.add_url_rule('/booking', 'load_flights', controllers.load_flights, methods=['post'])
app.add_url_rule('/flight/<flight_id>', 'detail', controllers.detail)
app.add_url_rule('/flight/<flight_id>', 'save_ticket', controllers.save_ticket, methods=['POST'])
app.add_url_rule('/admin/fetch', 'fetch_json', controllers.fetch_json, methods=['post'])


@app.context_processor
def common_data():
    return {
        "ticket_number": dao.count_user_tickets()
    }


@login_mana.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)