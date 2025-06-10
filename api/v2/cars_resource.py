from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.cars import Cars
from api.v2.parser import ParserCars

parser = ParserCars()


def car_not_found(car_id):
    session = db_session.create_session()
    car = session.query(Cars).get(car_id)
    if not car:
        abort(404, message=f'Car {car_id} not found')


class CarsResource(Resource):
    def get(self, car_id):
        car_not_found(car_id)
        session = db_session.create_session()
        car = session.query(Cars).get(car_id)
        return jsonify({'cars': car.to_dict(only=('id', 'brand', 'model', 'year', 'is_taken', 'place_id', 'image'))})

    def delete(self, car_id):
        car_not_found(car_id)
        session = db_session.create_session()
        car = session.query(Cars).get(car_id)
        session.delete(car)
        session.commit()
        return jsonify({'success': f'Car {car_id} was deleted'})

    def put(self, car_id):
        args = parser.parse_args()
        car_not_found(car_id)
        session = db_session.create_session()
        car = session.query(Cars).get(car_id)
        car.brand = args['brand']
        car.model = args['model']
        car.year = args['year']
        if args['is_taken'] == 'true':
            car.is_taken = True
        else:
            car.is_taken = False
        car.place_id = args['place_id']
        car.image = args['image']
        session.commit()
        return jsonify({'success': 'car was edited'})


class CarsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        cars = session.query(Cars).all()
        return jsonify(
            {'cars': [car.to_dict(only=('id', 'brand', 'model', 'year', 'is_taken', 'place_id', 'image')) for car in
                      cars]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        car = Cars()
        car.brand = args['brand']
        car.model = args['model']
        car.year = args['year']
        if args['is_taken'] == 'true':
            car.is_taken = True
        else:
            car.is_taken = False
        car.place_id = args['place_id']
        car.image = args['image']
        session.add(car)
        session.commit()
        return jsonify({'success': 'car was added'})
