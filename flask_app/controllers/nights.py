from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.night import Night
from flask_app.models.rate import Rating
# from flask_app import placeholder in case we need icons!

@app.route('/new/night')
def new_game_night():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    # Get user by ID
    user = User.get_by_id(session['user_id'])

    return render_template('new_game_night.html', user=user)

@app.route('/new/night/entry', methods=['POST'])
def game_night_hosting():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    # Validate the night data
    if not Night.validate_night(request.form):
        return redirect('/new/night')

    # Create a dictionary with the night data
    data = {
        'user_id': session['user_id'],
        'host': request.form['host'],
        'alt_host': request.form['alt_host'],
        'player_amount': request.form['player_amount'],
        'game_location': request.form['game_location'],
        'game_date': request.form['game_date'],
        'game_time': request.form['game_time'],
        'night_description': request.form['night_description']
    }
    
    # Save the night data
    Night.save_night(data)
    return redirect('/dashboard')

@app.route('/gamenights')
def my_game_nights():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    # Get user by ID
    user = User.get_by_id(session['user_id'])

    # Get all game nights associated with the user
    game_nights = Night.get_all(user.id)

    return render_template('my_game_nights.html', user=user, game_nights=game_nights)

@app.route('/gamenights/<int:night_id>')
def game_night_details(night_id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    # Get user by ID
    user = User.get_by_id(session['user_id'])

    # Get the details of a specific game night
    night = Night.get_by_id(night_id)

    return render_template('game_night_details.html', user=user, night=night)

@app.route('/gamenights/<int:night_id>/edit')
def edit_game_night(night_id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    # Get user by ID
    user = User.get_by_id(session['user_id'])

    # Get the details of a specific game night to be edited
    night = Night.get_by_id({'id': night_id})

    return render_template('edit_game_night.html', user=user, night=night)

@app.route('/gamenights/<int:night_id>/update', methods=['POST'])
def update_game_night(night_id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    # Validate the updated night data
    if not Night.validate_night(request.form):
        return redirect(f'/gamenights/{night_id}/edit')

    # Create a dictionary with the updated night data
    data = {
        'id': night_id,
        'host': request.form['host'],
        'alt_host': request.form['alt_host'],
        'player_amount': request.form['player_amount'],
        'game_location': request.form['game_location'],
        'game_date': request.form['game_date'],
        'game_time': request.form['game_time'],
        'night_description': request.form['night_description'],
    }

    # Update the night data
    Night.update(data)

    return redirect('/dashboard')

@app.route('/gamenights/<int:night_id>/delete')
def delete_game_night(night_id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    # Create a dictionary with the night ID to be deleted
    data = {
        'id': night_id
    }

    # Delete the night data
    Night.delete(data)

    return redirect('/dashboard')