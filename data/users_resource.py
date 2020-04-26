from datetime import datetime

from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from flask_restful import reqparse
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument('surname', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('age', required=False, type=int)
        parser.add_argument('position', required=False)
        parser.add_argument('speciality', required=False)
        parser.add_argument('address', required=False)
        parser.add_argument('email', required=False)
        parser.add_argument('city_from', required=False)
        parser.add_argument('hashed_password', required=False)
        return parser

    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('surname', 'name', 'position', 'speciality', 'city_from', 'email'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = self.parse().parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if args['surname'] is not None:
            user.surname = args['surname']
        if args['name'] is not None:
            user.name = args['name']
        if args['age'] is not None:
            user.age = args['age']
        if args['position'] is not None:
            user.position = args['position']
        if args['speciality'] is not None:
            user.speciality = args['speciality']
        if args['city_from'] is not None:
            user.city_from = args['city_from']
        if args['email'] is not None:
            user.email = args['email']
        if args['hashed_password'] is not None:
            user.hashed_password = args['hashed_password']
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument('surname', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('age', required=True, type=int)
        parser.add_argument('position', required=True)
        parser.add_argument('speciality', required=True)
        parser.add_argument('address', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('city_from', required=True)
        parser.add_argument('hashed_password', required=True)
        return parser

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name',
                  'position', 'speciality', 'city_from', 'email')) for item in users]})

    def post(self):
        args = self.parse().parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from'],
            hashed_password=args['hashed_password'],
            modified_date=datetime.now())
        user.set_password(user.hashed_password)
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
