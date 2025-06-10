from flask import redirect, render_template, request
from flask_login import login_user, login_required, logout_user, current_user
from pyexpat.errors import messages
from requests import post, get, put, delete
from data.users import User
from forms.users import LoginForm, EditUserForm, RegisterForm


def add_user_routes(app, session):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = session.query(User).filter(User.login == form.login.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
            return render_template('login.html', message='Incorrect login or password', form=form)
        return render_template('login.html', title='Login', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Register',
                                       form=form,
                                       message="Passwords do not match")
            user = post('http://localhost:8080/api/v2/users',
                        json={'login': form.login.data, 'password': form.password.data}).json()
            if user['success']:
                return redirect('/index')
            else:
                return render_template('register.html', title='Register', message=user, form=form)
        return render_template('register.html', title='Register', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/users')
    @login_required
    def users():
        users_ = get('http://localhost:8080/api/v2/users').json()['users']
        if current_user.is_admin:
            return render_template('users.html', users=users_, title='Users')

    @app.route('/users/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def edit_users(user_id):
        user = get(f'http://localhost:8080/api/v2/users/{user_id}').json()['users']
        if current_user.is_admin:
            form = EditUserForm()
            if request.method == 'GET':
                form.login.data = user['login']
                form.is_admin.data = user['is_admin']
            if form.validate_on_submit():
                user_update = put(f'http://localhost:8080/api/v2/users/{user_id}',
                                  json={'login': form.login.data,
                                        'is_admin': 'true' if form.is_admin.data in ['True',
                                                                                     'yes'] else 'false'}).json()
                if 'success' in user_update:
                    return redirect('/')
                else:
                    return render_template('edit_users.html', form=form, message=user_update)
            return render_template('edit_users.html', form=form)
        return render_template('users.html', message='forbidden')

    @app.route('/delete/users/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def delete_user(user_id):
        if current_user.is_admin:
            user_delete = delete(f'http://localhost:8080/api/v2/users/{user_id}').json()
            if 'success' in user_delete:
                return redirect('/')
            return render_template('users.html', message=user_delete['error'])
        return render_template('users.html', message='forbidden')

    @app.route('/add/users', methods=['GET', 'POST'])
    @login_required
    def add_user():
        redirect('/register')
