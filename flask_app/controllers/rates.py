from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.game import Game
from flask_app.models.user import User
from flask_app.models.night import Night
from flask_app.models.rate import Rating
# from flask_app import placeholder in case we need icons!

@app.route('/rate')
def rate_game(id):
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_one(session['user_id'])

    return render_template('past_game_nights.html', user=user, game=Game.get_all())