from flask import render_template,request,session,redirect,flash, send_from_directory
from flask_app import app
from flask_app.models.user import User
from flask_app.models.night import Night
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename

# from flask_app import (placeholder incase we end up needing to import some icons)

bcrypt = Bcrypt(app)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/create', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/register')

    file = request.files['user_image']
    filename = None

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            print(f"File saved to: {file_path}")  # Print the file path
        except Exception as e:
            print(f"Error saving file: {e}")

    user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "phone_number": request.form['phone_number'],
        "password": request.form['password'],
        "confirm_password": request.form['confirm_password'],
        "can_host": request.form['can_host'],
        "user_location": request.form['user_location'],
        "user_description": request.form['user_description'],
        "user_image": filename,
    }

    hashed_password = bcrypt.generate_password_hash(user_data['password'])
    user_data['password'] = hashed_password

    user_id = User.save(user_data)

    session['user_id'] = user_id

    return redirect('/dashboard')

@app.route('/returning', methods=['POST'])
def login_user():
    email_or_phone = request.form['email']
    password = request.form['password']

    user = User.get_by_email(email_or_phone)
    if not user:
        user = User.get_by_phone_number(email_or_phone)

    if not user or not User.check_password(user.password, password):
        flash("Invalid email or password", "login")
        return redirect('/login')

    session['user_id'] = user.id

    return redirect('/dashboard')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])
    game_nights = Night.get_all_by_location(user.user_location)

    return render_template('dashboard.html', user=user, game_nights=game_nights)


@app.route('/user/<int:user_id>')
def user_profile(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(user_id)

    return render_template('my_profile.html', user=user)

@app.route('/user/edit/<int:user_id>')
def edit_user(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(user_id)

    return render_template('edit_profile.html', user=user)

@app.route('/user/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if 'user_id' not in session:
        return redirect('/logout')

    if not User.validate_user(request.form):
        return redirect(f'/user/edit/{user_id}')

    user = User.get_by_id(user_id)

    if 'password' in request.form:
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password)
    else:
        hashed_password = user.password

    file = request.files['user_image']
    filename = user.user_image

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if user.user_image != filename:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.user_image))

    user_data = {
        "id": user_id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "phone_number": request.form['phone_number'],
        "can_host": request.form['can_host'],
        "user_location": request.form['user_location'],
        "user_description": request.form['user_description'],
        "password": hashed_password,
        "user_image": filename,
    }

    User.update(user_data)

    return redirect(f'/user/{user_id}')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
