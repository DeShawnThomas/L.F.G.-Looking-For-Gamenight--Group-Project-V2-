from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Game:

    db = "game_night_schema"

    def __init__(self, data):
        self.id = data['id']
        self.game_name = data['game_name']
        self.game_type = data['game_type']
        self.game_description = data['game_description']
        self.game_image = data['game_image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        self.players = []

    
    def get_creator(self):
        from flask_app.models.user import User
        creator = User.get_by_id({'id': self.user_id})
        return creator

    @classmethod
    def save_game(cls, data):
        query = "INSERT INTO games (game_name, game_type, game_description, game_image, user_id) VALUES (%(game_name)s, %(game_type)s, %(game_description)s, %(game_image)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_game(game):
        is_valid = True
        if len(game['game_name']) < 2:
            flash("Game name must be at least 2 characters")
            is_valid = False
        if len(game['game_type']) < 2:
            flash("Game type must be at least 2 characters")
            is_valid = False
        if len(game['game_description']) < 2:
            flash("Description must be at least 2 characters")
            is_valid = False
        return is_valid

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM games WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE games SET game_name = %(game_name)s, game_type = %(game_type)s, game_description = %(game_description)s, game_image = %(game_image)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        from flask_app.models.user import User
        query = "SELECT * FROM games JOIN users ON games.user_id = users.id WHERE games.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            user_d = results[0]
            game_object = cls(user_d)
            new_user_d = {
                'id': user_d['users.id'],
                'first_name': user_d['first_name'],
                'last_name': user_d['last_name'],
                'email': user_d['email'],
                'phone_number': user_d['phone_number'],
                'password': user_d['password'],
                'can_host': user_d['can_host'],
                'user_location': user_d['user_location'],
                'user_description': user_d['user_description'],
                'user_image': user_d['user_image'],
                'created_at': user_d['users.created_at'],
                'updated_at': user_d['users.updated_at']
            }
            user_object = User(new_user_d)
            game_object.creator = user_object
            return game_object
        
    @classmethod
    def get_all(cls):
        query = "SELECT games.id AS game_id, games.game_name, games.game_type, games.game_description, games.game_image, games.created_at, games.updated_at, users.id AS user_id, users.first_name, users.last_name, users.email, users.phone_number, users.password, users.can_host, users.user_location, users.user_description, users.user_image, users.created_at AS user_created_at, users.updated_at AS user_updated_at FROM games JOIN users ON games.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        game_object_list = []
        for result in results:
            game_data = {
                'id': result['game_id'],
                'game_name': result['game_name'],
                'game_type': result['game_type'],
                'game_description': result['game_description'],
                'game_image': result['game_image'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'user_id': result['user_id']
            }
            game_object = cls(game_data)
            game_object_list.append(game_object)
        return game_object_list

    @classmethod
    def get_user_games(cls, user_id):
        query = "SELECT * FROM games WHERE user_id = %(user_id)s;"
        data = {'user_id': user_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        game_object_list = []
        for game_data in results:
            game_object = cls(game_data)
            game_object_list.append(game_object)
        return game_object_list
    
    @staticmethod
    def validate_game(game):
        is_valid = True
        if len(game['game_name']) < 2:
            flash("The name of the game must be at least 2 characters")
            is_valid= False
        if len(game['game_type']) < 2:
            flash("Type of game must be at least 2 characters. If you don't have one please enter 'N/A'.")
            is_valid= False
        if len(game['game_description']) < 1:
            flash("Please enter a sentence or two describing the game.")
            is_valid=False
        return is_valid
