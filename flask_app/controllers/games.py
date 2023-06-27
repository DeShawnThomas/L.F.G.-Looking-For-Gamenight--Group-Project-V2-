from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.game import Game
from flask_app.models.user import User
from flask_app.models.night import Night
from flask_app.models.rate import Rating
import os
from werkzeug.utils import secure_filename
# Import necessary modules

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Set the upload folder for game images

@app.route('/new/game')
def add_a_game():
    if 'user_id' not in session:
        return redirect('/logout')
    # Check if user is logged in, otherwise redirect to logout

    user = User.get_by_id(session['user_id'])
    # Get the user object using the session user_id

    return render_template('add_a_game.html', user=user)
    # Render the 'add_a_game.html' template, passing the user object

@app.route('/new/game/entry', methods=['POST'])
def addition_to_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    # Check if user is logged in, otherwise redirect to logout
    
    user_id = session['user_id']
    # Get the user_id from the session
    
    if not Game.validate_game(request.form):
        return redirect('/new/game')
    # Validate the game data received from the form, if validation fails, redirect to '/new/game'

    file = request.files['game_image']
    if file:
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'])
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file.save(os.path.join(upload_folder, filename))
    else:
        filename = 'default_image.jpg'
    # Save the uploaded game image file to the appropriate folder or use a default image name

    data = {
        'user_id': user_id,
        'game_name': request.form['game_name'],
        'game_type': request.form['game_type'],
        'game_description': request.form['game_description'],
        'game_image': filename,
    }
    # Create a dictionary containing the game data

    Game.save_game(data)
    # Save the game using the data dictionary
    
    return redirect('/dashboard')
    # Redirect to the dashboard after saving the game

@app.route('/collection')
def my_game_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    # Check if user is logged in, otherwise redirect to logout
    
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    # Get the user object using the session user_id

    if user:
        games = user.get_user_games()
    else:
        games = []
    # Get the games associated with the user, or an empty list if user is not found

    return render_template('collection.html', user=user, games=games)
    # Render the 'collection.html' template, passing the user object and the games

@app.route('/game/<int:id>')
def view_game(id):
    if 'user_id' not in session:
        return redirect('/logout')
    # Check if user is logged in, otherwise redirect to logout

    user = User.get_by_id(session['user_id'])
    # Get the user object using the session user_id

    return render_template('view_game.html', user=user, game=Game.get_one_by_id({'id': id}))
    # Render the 'view_game.html' template, passing the user object and the game object

@app.route('/edit/game/<int:id>')
def edit_game(id):
    if 'user_id' not in session:
        return redirect('/logout')
    # Check if user is logged in, otherwise redirect to logout

    user = User.get_by_id(session['user_id'])
    game = Game.get_by_id({'id': id})
    # Get the user object and the game object using the session user_id and the provided game id

    return render_template('edit_game.html', user=user, game=game)
    # Render the 'edit_game.html' template, passing the user object and the game object

@app.route('/edit/game/<int:id>/update', methods=['POST'])
def edit_collection(id):
    if 'user_id' not in session:
        return redirect('/logout')
    # Check if user is logged in, otherwise redirect to logout
    
    if not Game.validate_game(request.form):
        return redirect(f'/edit/game/{id}')
    # Validate the game data received from the form, if validation fails, redirect to the edit page

    data = {
        'id': id,
        'game_name': request.form['game_name'],
        'game_type': request.form['game_type'],
        'game_description': request.form['game_description'],
        'game_image': request.files['game_image'],
    }
    # Create a dictionary containing the updated game data

    Game.update(data)
    # Update the game using the data dictionary
    
    return redirect('/dashboard')
    # Redirect to the dashboard after updating the game

@app.route('/delete/game/<int:id>')
def never_happened(id):
    if 'user_id' not in session:
        return redirect('/logout')
    # Check if user is logged in, otherwise redirect to logout

    Game.delete({'id':id})
    # Delete the game with the provided id

    return redirect('/dashboard')
    # Redirect to the dashboard after deleting the game
