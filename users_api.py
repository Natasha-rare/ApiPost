from flask import Flask, jsonify, Blueprint, request

from data import db_session
from data.users import User
import datetime
blueprint = Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict()
                 for item in users]
        }
    )

@blueprint.route('/api/users/<int:users_id>',  methods=['GET'])
def get_one_users(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                       'speciality', 'address', 'email', 'city_from', 'hashed_password'))
        }
    )


@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def correct_users(users_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    k = ['surname', 'name', 'age', 'position',
         'speciality', 'address', 'email', 'city_from', 'hashed_password']
    for key in k:
        if key in request.json:
            if key == 'surname':
                users.surname = request.json[key]
            if key == 'name':
                users.name = request.json[key]
            if key == 'age':
                users.age = request.json[key]
            if key == 'position':
                users.position = request.json[key]
            if key == 'speciality':
                users.speciality = request.json[key]
            if key == 'city_from':
                users.city_from = request.json[key]
            if key == 'address':
                users.address = request.json[key]
            if key == 'email':
                users.email = request.json[key]
            if key == 'hashed_password':
                users.hashed_password = request.json[key]
    # session.add(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position',
         'speciality', 'address', 'email', 'city_from', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    users = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        city_from=request.json['city_from'],
        hashed_password=request.json['hashed_password'],
        modified_date=request.json['modified_date']
    )
    if session.query(User).filter(User.id == users.id).first():
        return jsonify({'error': 'Id already exists'})
    session.add(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_news(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    session.delete(users)
    session.commit()
    return jsonify({'success': 'OK'})
