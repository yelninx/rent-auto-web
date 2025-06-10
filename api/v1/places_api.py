from flask import Blueprint, jsonify, request
from data import db_session
from data.places import Place

blueprint = Blueprint('places_api', __name__, template_folder='../templates')


@blueprint.route('/api/v1/places')
def get_places():
    places = db_session.create_session().query(Place).all()
    return jsonify(
        {'places': [place.to_dict(only=('id', 'name', 'owner_id', 'address')) for place in places]}
    )


@blueprint.route('/api/v1/places/<int:place_id>', methods=['GET'])
def get_one_place(place_id):
    session = db_session.create_session()
    place = session.query(Place).get(place_id)
    if not place:
        return jsonify({'error': 'place not found'})
    return jsonify({
        'place': place.to_dict(only=('id', 'name', 'owner_id', 'address'))
    })


@blueprint.route('/api/v1/places', methods=['POST'])
def create_place():
    session = db_session.create_session()
    places = session.query(Place).all()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['name', 'owner_id', 'address']):
        return jsonify({'error': 'not enough arguments in request'})

    place = Place(
        name=request.json['name'],
        owner_id=request.json['owner_id'],
        address=request.json['address']
    )
    session.add(place)
    session.commit()
    return jsonify({'success': 'place added'})


@blueprint.route('/api/v1/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    session = db_session.create_session()
    place = session.query(Place).get(place_id)
    if not place:
        return jsonify({'error': 'place not found'})
    session.delete(place)
    session.commit()
    return jsonify({'success': 'place was deleted'})


@blueprint.route('/api/v1/places/<int:place_id>', methods=['PUT'])
def edit_place(place_id):
    if not request.json:
        return jsonify({'error': 'empty requesr'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['name', 'owner_id', 'address']):
        return jsonify({'error': 'not enough arguments in request'})
    session = db_session.create_session()
    place = session.query(Place).get(place_id)
    if not place:
        return jsonify({'error': 'place not found'})
    place.name = request.json['name']
    place.owner_id = request.json['owner_id']
    place.address = request.json['address']
    session.commit()
    return jsonify({'success': 'place was edited'})
