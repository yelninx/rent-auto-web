from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.places import Place
from api.v2.parser import ParserPlaces

parser = ParserPlaces()


def place_not_found(place_id):
    session = db_session.create_session()
    places = session.query(Place).get(place_id)
    if not places:
        abort(404, message=f'Place {place_id} not found')


class PlacesResource(Resource):
    def get(self, place_id):
        place_not_found(place_id)
        session = db_session.create_session()
        place = session.query(Place).get(place_id)
        return jsonify({'places': place.to_dict(only=('id', 'name', 'owner_id', 'address'))})

    def delete(self, place_id):
        place_not_found(place_id)
        session = db_session.create_session()
        place = session.query(Place).get(place_id)
        session.delete(place)
        session.commit()
        return jsonify({'success': f'place {place_id} was deleted'})

    def put(self, place_id):
        args = parser.parse_args()
        place_not_found(place_id)
        session = db_session.create_session()
        place = session.query(Place).get(place_id)
        place.name = args['name']
        place.owner_id = args['owner_id']
        place.address = args['address']
        session.commit()
        return jsonify({'success': 'place edited'})


class PlacesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        places = session.query(Place).all()
        return jsonify({'places': [place.to_dict(only=('id', 'name', 'owner_id', 'address')) for place in places]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        place = Place(
            name=args['name'],
            owner_id=args['owner_id'],
            address=args['address']
        )
        session.add(place)
        session.commit()
        return jsonify({'success': 'place was added'})
