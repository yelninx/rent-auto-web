from flask import Blueprint, jsonify, request
from data import db_session
from data.users import User

blueprint = Blueprint('users_api', __name__, template_folder='../templates')


@blueprint.route('/api/v1/users')
def get_users():
    users = db_session.create_session().query(User).all()
    return jsonify({
        'users': [user.to_dict(only=('id', 'login', 'is_admin')) for user in users]
    })


@blueprint.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = db_session.create_session().query(User).get(user_id)
    if not user:
        return jsonify({'error': 'user not found'})
    return jsonify({
        'users': [user.to_dict(only=('id', 'login', 'is_admin'))]
    })


@blueprint.route('/api/v1/users', methods=['POST'])
def create_user():
    session = db_session.create_session()
    users = session.query(User).all()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['login', 'password', 'is_admin']):
        return jsonify({'error': 'not enough arguments in request'})
    else:
        for user in users:
            if request.json['login'] == user.login:
                return jsonify({'error': 'user with this login already exists'})

    user = User(
        login=request.json['login'],
        is_admin=request.json['is_admin']
    )
    user.set_password(request.json['password'])
    session.add(user)
    session.commit()
    return jsonify({'success': 'user added'})


@blueprint.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'user not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'user was deleted'})


@blueprint.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['login', 'password', 'is_admin']):
        return jsonify({'error': 'not enough arguments in request'})
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'user not found'})

    user.login = request.json['login']
    user.is_admin = request.json['is_admin']
    user.set_password(request.json['password'])
    session.commit()
    return jsonify({'success': 'user was edited'})