import os.path
from flask import Flask, render_template
from requests import get
from flask_login import LoginManager
from data.users import User
from data import db_session
from flask_restful import Api
from api.v1 import cars_api, places_api, users_api
from api.v2 import cars_resource, places_resource, users_resource
from users import add_user_routes
from cars import add_car_routes
from places import add_places_routes

app = Flask(__name__, template_folder=os.path.abspath('../templates'), static_folder=os.path.abspath('../static'))
app.config['SECRET_KEY'] = 'secret_key'
db_session.global_init('../db/rent_auto.db')
session = db_session.create_session()
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
add_car_routes(app)
add_user_routes(app, session)
add_places_routes(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    routes = [{'path': '/users', 'name': 'Users'},
              {'path': '/places', 'name': 'Places'}]
    cars = get('http://localhost:8080/api/v2/cars').json()['cars']
    return render_template('index.html', cars=cars, routes=routes)


if __name__ == '__main__':
    app.register_blueprint(cars_api.blueprint)
    app.register_blueprint(places_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(cars_resource.CarsListResource, '/api/v2/cars')
    api.add_resource(cars_resource.CarsResource, '/api/v2/cars/<int:car_id>')
    api.add_resource(places_resource.PlacesListResource, '/api/v2/places')
    api.add_resource(places_resource.PlacesResource, '/api/v2/places/<int:place_id>')
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    app.run(port=8080, host='localhost')
