from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_bcrypt import check_password_hash
from flask_app.models.game import Game

class User:

    db = "game_night_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.can_host = data['can_host']
        self.phone_number = data['phone_number']
        self.user_location = data['user_location']
        self.user_description = data['user_description']
        self.user_image = data['user_image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.games = []

    def get_user_games(self):
        self.games = Game.get_user_games(self.id)

    def get_nights(self):
        from flask_app.models.night import Night
        query = "SELECT * FROM nights WHERE user_id = %(id)s;"
        data = {'id': self.id}
        results = connectToMySQL(self.db).query_db(query, data)
        night_object_list = []
        for night_data in results:
            night_object = Night(night_data)
            night_object_list.append(night_object)
        return night_object_list

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,phone_number,password,can_host,user_location,user_description,user_image) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(phone_number)s,%(password)s,%(can_host)s,%(user_location)s,%(user_description)s,%(user_image)s);"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, phone_number=%(phone_number)s, password=%(password)s, can_host = %(can_host)s, user_location=%(user_location)s, user_description=%(user_description)s, user_image=%(user_image)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, {'email': email})
        if not results:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_phone_number(cls, phone_number):
        query = "SELECT * FROM users WHERE phone_number = %(phone_number)s;"
        results = connectToMySQL(cls.db).query_db(query, {'phone_number': phone_number})
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id':id}
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return False
        return cls(result[0])

    
    @classmethod
    def get_one_game(cls, data ): 
        query = "SELECT * FROM users LEFT JOIN games on users.id = games.user_id WHERE users.id = %(id)s;" 
        results = connectToMySQL(cls.db).query_db(query,data) 
        print(results)  
        User = cls(results[0])  
        for row in results: 
            game = { 
                'id': row['games.id'],
                'game_name': row['game_name'],
                'game_type': row['game_type'],
                'game_description': row['game_description'],
                'game_image': row['game_image'],
                'host': row['host'],
                'player_amount': row['player_amount'],
                'game_location': row['game_location'],
                'game_date': row['game_date'],
                'created_at': row['games.created_at'],
                'updated_at': row['games.updated_at']
            }
            User.games.append(Game(game))  
        return User

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "regError",)
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "regError")
            is_valid= False
        if len(user['email']) < 1:
            flash("Email unusable.","regError",)
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Incorrect Email", "regError",)
            is_valid=False
        if len(user['phone_number']) < 2:
            flash("Phone number must be at least 10 characters", "regError")
            is_valid= False
        if len(user['user_location']) < 2:
            flash("Location must be at least 2 characters", "regError")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be no less then 8 characters", "regError")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Password and confirmation password do not match.", "register")
            is_valid = False
        if len(user['user_description']) < 2:
            flash("Description must be at least 2 characters", "regError")
            is_valid= False
        return is_valid

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)
