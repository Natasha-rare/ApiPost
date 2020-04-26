from flask import Flask, render_template, redirect, request, make_response, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_restful import Api
from requests import get
import requests
import users_api
from loginform import LoginForm, JobsForm
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.users_resource import UsersResource, UsersListResource
from jobs_resource import JobsListResource,JobsResource
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(users_api.blueprint)
    # для списка объектов
    api.add_resource(UsersListResource, '/api/v2/users')

    api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')

    api.add_resource(JobsListResource, '/api/v2/jobs')

    api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')

    app.run()


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    jobs = []
    for user in session.query(Jobs).all():
        jobs.append(user)
        print(jobs)
    session.commit()
    return render_template('index.html', jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    map_api_server = 'http://static-maps.yandex.ru/1.x/?&spn=0.05,0.05&l=sat'
    print(f'http://localhost:5000/api/v2/users/{user_id}')
    a = get(f'http://localhost:5000/api/v2/users/{user_id}').json()
    a = a['user']
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": a['city_from'],
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"].split()
        map_api_server += f'&ll={toponym_coodrinates[0]},{toponym_coodrinates[1]}'
        return render_template('maps.html', title='Карта', api=map_api_server, city=a['city_from'], name=a['name'], surname=a['surname'])
    return redirect("/")


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = JobsForm()
    if form.validate_on_submit():
        if session:

            return redirect("/")
        return redirect('/logout')
    return render_template('addjob.html', title='44', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()