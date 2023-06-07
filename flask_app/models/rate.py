from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.game import Game
from flask_app.models.night import Night


class Rating:
    def __init__(self, data):
        self.id = data['id']
        self.rating = data['rating']
        self.user_id = data['user_id']
        self.game_id = data['game_id']
        self.night_id = data['night_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = None
        self.game = None
        self.night = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO ratings (rating, user_id, game_id, night_id) VALUES (%(rating)s, %(user_id)s, %(game_id)s, %(night_id)s);"
        return connectToMySQL("game_night_schema").query_db(query, data)

    @classmethod
    def get_all_join_user(cls, data):
        query = "SELECT * FROM ratings " \
                "JOIN users ON ratings.user_id = users.id " \
                "JOIN games ON ratings.game_id = games.id " \
                "JOIN nights ON ratings.night_id = nights.id " \
                "WHERE ratings.game_id = %(id)s;"
        results = connectToMySQL("game_night_schema").query_db(query, data)
        if len(results) == 0:
            return []
        else:
            rating_object_list = []
            for rating_data in results:
                rating_object = cls(rating_data)

                from flask_app.models.user import User  # Importing here to avoid circular import
                user_data = {
                    'id': rating_data['users.id'],
                    'first_name': rating_data['first_name'],
                    'last_name': rating_data['last_name'],
                    'email': rating_data['email'],
                    'phone_number': rating_data['phone_number'],
                    'user_location': rating_data['user_location'],
                    'user_description': rating_data['user_description'],
                    'user_image': rating_data['user_image'],
                    'password': rating_data['password'],
                    'created_at': rating_data['users.created_at'],
                    'updated_at': rating_data['users.updated_at']
                }
                user_object = User(user_data)
                rating_object.sender = user_object

                game_data = {
                    'id': rating_data['games.id'],
                    'game_name': rating_data['game_name'],
                    'game_type': rating_data['game_type'],
                    'game_description': rating_data['game_description'],
                    'game_image': rating_data['game_image'],
                    'created_at': rating_data['games.created_at'],
                    'updated_at': rating_data['games.updated_at'],
                    'user_id': rating_data['games.user_id']
                }
                game_object = Game(game_data)
                rating_object.game = game_object

                night_data = {
                    'id': rating_data['nights.id'],
                    'night_name': rating_data['night_name'],
                    'night_description': rating_data['night_description'],
                    'created_at': rating_data['nights.created_at'],
                    'updated_at': rating_data['nights.updated_at'],
                    'user_id': rating_data['nights.user_id']
                }
                night_object = Night(night_data)
                rating_object.night = night_object

                rating_object_list.append(rating_object)

            return rating_object_list
