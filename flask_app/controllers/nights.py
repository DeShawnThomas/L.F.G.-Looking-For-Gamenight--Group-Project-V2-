from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.night import Night
from flask_app.models.rate import Rating
# from flask_app import placeholder in case we need icons!

@app.route('/new/night')
def new_game_night():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(session['user_id'])

    return render_template('new_game_night.html', user=user)

@app.route('/new/night/entry', methods=['POST'])
def game_night_hosting():
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Night.validate_night(request.form):
        return redirect('/new/night')

    data = {
        'user_id': session['user_id'],
        'host': request.form['host'],
        'alt_host': request.form['alt_host'],
        'player_amount': request.form['player_amount'],
        'game_location': request.form['game_location'],
        'game_date': request.form['game_date'],
        'game_time': request.form['game_time'],
        'night_description': request.formS['night_description']
    }
    
    Night.save_night(data)
    return redirect('/dashboard')

@app.route('/gamenights')
def my_game_nights():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(session['user_id'])

    game_nights = Night.get_all(user.id)
    # Might need to look into this one based on how we have the games table set atm. Looked into it and fixed.

    return render_template('my_game_nights.html', user=user, game_nights=game_nights)

@app.route('/gamenights/<int:night_id>')
def game_night_details(night_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(session['user_id'])

    night = Night.get_by_id(night_id)

    return render_template('game_night_details.html', user=user, night=night)

@app.route('/gamenights/<int:night_id>/edit')
def edit_game_night(night_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(session['user_id'])
    night = Night.get_by_id({'id': night_id})

    return render_template('edit_game_night.html', user=user, night=night)

@app.route('/gamenights/<int:night_id>/update', methods=['POST'])
def update_game_night(night_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Night.validate_night(request.form):
        return redirect(f'/gamenights/{night_id}/edit')

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

    Night.update(data)

    return redirect('/dashboard')

@app.route('/gamenights/<int:night_id>/delete')
def delete_game_night(night_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': night_id
    }

    Night.delete(data)

    return redirect('/dashboard')
