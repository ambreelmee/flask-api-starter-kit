"""
Define the REST verbs relative to the users
"""

from flasgger import swag_from
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import Argument
from flask.json import jsonify

from repositories import UserRepository
from util import parse_params, bad_request
from util.authorized import authorized


class UserResource(Resource):
    """ Verbs relative to the users """

    @staticmethod
    @swag_from('../swagger/user/GET.yml')
    def get(last_name, first_name):
        """ Return an user key information based on his name """
        user = UserRepository.get(last_name=last_name, first_name=first_name)
        if user:
            return jsonify({'user': user.json})
        return bad_request('user not found')

    @staticmethod
    @parse_params(
        Argument(
            'age',
            location='json',
            required=True,
            help='The age of the user.'
        ),
    )
    @swag_from('../swagger/user/POST.yml')
    @authorized
    def post(last_name, first_name, age):
        """ Create an user based on the sent information """
        existing_user = UserRepository.get(
            last_name=last_name, first_name=first_name)
        if existing_user:
            return bad_request('user already in database')
        user = UserRepository.create(
            last_name=last_name,
            first_name=first_name,
            age=age
        )
        if user:
            return jsonify({'user': user.json})
        return bad_request('unable to create user')

    @staticmethod
    @parse_params(
        Argument(
            'age',
            location='json',
            required=True,
            help='The age of the user.'
        ),
    )
    @swag_from('../swagger/user/PUT.yml')
    @authorized
    def put(last_name, first_name, age):
        """ Update an user based on the sent information """
        repository = UserRepository()
        user = repository.update(
            last_name=last_name,
            first_name=first_name,
            age=age
        )
        if user:
            return jsonify({'user': user.json})
        return bad_request('unable to update user')
