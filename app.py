"""
Dog Breed Identification - Main Application
B.Tech Data Science Project

Run this file to start the Flask web server.
"""

import os
import re
import json
from functools import wraps
import numpy as np
from PIL import Image
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
import config
from utils.pdf_generator import generate_prediction_pdf

# Suppress TensorFlow verbose logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input

from database.db import (
    save_prediction,
    get_prediction_history,
    get_prediction_by_id,
    delete_prediction,
    clear_all_history,
    test_db_connection,
    create_user,
    get_user_by_username,
    get_user_by_email,
    get_user_by_id,
    add_favorite_breed,
    remove_favorite_breed,
    is_favorite_breed,
    get_user_favorites,
    get_admin_stats,
    set_user_admin,
    save_feedback
)

# ---- Create Flask App ----
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Create upload folder if it does not exist
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

# ---- Load ML Models and Class Names once at startup ----
MODEL_PATH = os.path.join(config.MODEL_FOLDER, 'best_model.keras')
CLASSES_PATH = os.path.join(config.MODEL_FOLDER, 'class_names.txt')

model = None
dog_detector = None
class_names = []

# ImageNet synsets 151 to 268 (domestic dog breeds) plus 273 (dingo) & 275 (African hunting dog)
IMAGENET_DOG_INDICES = set(range(151, 269)) | {273, 275}


def format_breed_name(breed_raw):
    """Convert breed identifier like 'golden_retriever' to 'Golden Retriever'."""
    words = breed_raw.replace('_', ' ').replace('-', ' ').split()
    return ' '.join(word.capitalize() for word in words)


try:
    # 1. Load the trained dog breed identification model
    if os.path.exists(MODEL_PATH):
        print(f"[*] Loading trained model from {MODEL_PATH} ...")
        model = tf.keras.models.load_model(MODEL_PATH)
        print("[*] Model loaded successfully.")
    else:
        print(f"[!] Warning: Model file not found at {MODEL_PATH}")

    # 2. Load 120 breed class names
    if os.path.exists(CLASSES_PATH):
        with open(CLASSES_PATH, 'r', encoding='utf-8') as f:
            class_names = [line.strip() for line in f if line.strip()]
        print(f"[*] Loaded {len(class_names)} breed classes.")
    else:
        print(f"[!] Warning: Class names file not found at {CLASSES_PATH}")

    # 3. Load pre-trained MobileNetV2 for dog vs non-dog validation
    print("[*] Loading pretrained ImageNet model for dog/non-dog validation ...")
    dog_detector = MobileNetV2(weights='imagenet')
    print("[*] Dog detector loaded successfully.")
except Exception as e:
    print(f"[!] Error loading model: {e}")

# ---- Check Database Connection at Startup ----
try:
    test_db_connection()
except Exception as db_init_err:
    print(f"[!] Error checking database connection at startup: {db_init_err}")


def is_dog_image(img_array, threshold=0.20):
    """
    Check if the uploaded image contains a dog using pre-trained ImageNet classifier.
    Returns (is_dog: bool, dog_probability: float).
    """
    if dog_detector is None:
        return True, 1.0

    preds = dog_detector.predict(img_array, verbose=0)[0]
    top1_idx = int(np.argmax(preds))
    dog_prob = sum(float(preds[i]) for i in IMAGENET_DOG_INDICES)

    # Considered a dog if top-1 class is a dog, or total dog probability exceeds threshold
    is_dog = (top1_idx in IMAGENET_DOG_INDICES) or (dog_prob >= threshold)
    return is_dog, dog_prob


# ---- Helper: check allowed file extensions ----
def allowed_file(filename):
    """Return True if the file extension is allowed."""
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )


# ---- Authentication Helper: login_required decorator ----
def login_required(f):
    """
    Decorator to protect routes that require user authentication.
    Redirects unauthenticated users to the login page with a friendly warning.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


# ---- Authentication Helper: admin_required decorator ----
def admin_required(f):
    """
    Decorator to protect admin-only routes.
    Requires both a valid login session AND is_admin == True.
    Normal users are shown a 403 Forbidden error page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login', next=request.path))
        if not session.get('is_admin'):
            flash("Access denied. This page is for administrators only.", "error")
            return render_template('403.html'), 403
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle new user registration with input validation and secure
    Werkzeug cryptographic password hashing.
    """
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # 1. Required fields check
        if not username or not email or not password or not confirm_password:
            flash("Please fill in all required registration fields.", "error")
            return render_template('signup.html', active_page='signup')

        # 2. Username format validation
        if len(username) < 3 or len(username) > 30:
            flash("Username must be between 3 and 30 characters long.", "error")
            return render_template('signup.html', active_page='signup')

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            flash("Username can only contain letters, numbers, and underscores.", "error")
            return render_template('signup.html', active_page='signup')

        # 3. Email format validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            flash("Please enter a valid email address.", "error")
            return render_template('signup.html', active_page='signup')

        # 4. Password length and confirmation checks
        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template('signup.html', active_page='signup')

        if password != confirm_password:
            flash("Passwords do not match. Please re-enter your password.", "error")
            return render_template('signup.html', active_page='signup')

        # 5. Prevent duplicate username
        existing_user = get_user_by_username(username)
        if existing_user:
            flash("This username is already taken. Please choose another username.", "error")
            return render_template('signup.html', active_page='signup')

        # 6. Prevent duplicate email registration
        existing_email = get_user_by_email(email)
        if existing_email:
            flash("An account with this email address already exists. Please log in.", "error")
            return render_template('signup.html', active_page='signup')

        # 7. Secure password hashing using Werkzeug
        password_hash = generate_password_hash(password)

        # 8. Insert new user into MySQL database
        new_user_id = create_user(username=username, email=email, password_hash=password_hash)
        if new_user_id:
            flash("Account created successfully! Please log in with your credentials.", "success")
            return redirect(url_for('login'))
        else:
            flash("Database error: Could not complete registration. Please try again later.", "error")
            return render_template('signup.html', active_page='signup')

    return render_template('signup.html', active_page='signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login, password verification, and session creation.
    """
    if 'user_id' in session:
        return redirect(url_for('home'))

    next_url = request.args.get('next', '')

    if request.method == 'POST':
        login_identifier = request.form.get('login_identifier', '').strip()
        password = request.form.get('password', '')

        if not login_identifier or not password:
            flash("Please enter both username/email and password.", "error")
            return render_template('login.html', active_page='login')

        # Look up by email or username
        user = None
        if '@' in login_identifier:
            user = get_user_by_email(login_identifier)
        else:
            user = get_user_by_username(login_identifier)

        # Check password hash securely
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id']  = user['user_id']
            session['username'] = user['username']
            session['email']    = user['email']
            session['is_admin'] = bool(user.get('is_admin', 0))

            flash(f"Welcome back, {user['username']}! Logged in successfully.", "success")

            # Validate next_url to prevent open redirect vulnerabilities
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('home'))
        else:
            flash("Invalid username/email or password. Please try again.", "error")
            return render_template('login.html', active_page='login')

    return render_template('login.html', active_page='login')


@app.route('/logout')
def logout():
    """Log out current user and clear Flask session."""
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('login'))


# ==================== PAGE ROUTES ====================

@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html', active_page='home')


@app.route('/identify')
def identify():
    """Render the identify (upload) page."""
    return render_template('identify.html', active_page='identify')


@app.route('/breeds')
def breed_info():
    """Render the breed information and comparison page."""
    breeds_path = os.path.join(config.DATABASE_FOLDER, 'breeds_data.json')
    breeds = []
    if os.path.exists(breeds_path):
        with open(breeds_path, 'r', encoding='utf-8') as f:
            breeds = json.load(f)

    # Check user bookmarked breeds if logged in
    user_fav_set = set()
    if 'user_id' in session:
        favs = get_user_favorites(session['user_id'])
        user_fav_set = {f['breed_name'] for f in favs}

    return render_template('breeds.html', active_page='breed_info', breeds=breeds, user_fav_set=user_fav_set)


@app.route('/api/breeds')
def api_breeds():
    """Return all 120 breed records in JSON format for instant search & compare."""
    breeds_path = os.path.join(config.DATABASE_FOLDER, 'breeds_data.json')
    if os.path.exists(breeds_path):
        with open(breeds_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])


@app.route('/performance')
def performance():
    """Render the model performance and evaluation results page."""
    metrics_path = os.path.join(config.MODEL_FOLDER, 'performance_metrics.json')
    metrics = {}
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r', encoding='utf-8') as f:
            metrics = json.load(f)
    return render_template('performance.html', active_page='performance', metrics=metrics)


@app.route('/api/performance')
def api_performance():
    """Return model performance metrics in JSON format."""
    metrics_path = os.path.join(config.MODEL_FOLDER, 'performance_metrics.json')
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({})


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', active_page='about')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    """
    Allow users and guests to submit reviews and star ratings.
    Feedback is stored in MySQL and immediately updates the Admin Dashboard.
    """
    if request.method == 'POST':
        rating_val = request.form.get('rating')
        message_val = request.form.get('message', '').strip()

        # Validation
        if not rating_val:
            flash("Please select a star rating (1 to 5 stars).", "warning")
            return render_template('feedback.html', active_page='feedback', message=message_val)

        try:
            rating = int(rating_val)
            if rating < 1 or rating > 5:
                raise ValueError()
        except ValueError:
            flash("Invalid rating selected. Please choose between 1 and 5 stars.", "error")
            return render_template('feedback.html', active_page='feedback', message=message_val)

        if not message_val:
            flash("Please enter a short message or comment with your feedback.", "warning")
            return render_template('feedback.html', active_page='feedback', selected_rating=rating)

        # Associate with logged-in user if available, otherwise guest (user_id=None)
        user_id = session.get('user_id')
        feedback_id = save_feedback(message=message_val, rating=rating, user_id=user_id)

        if feedback_id:
            flash("Thank you! Your feedback and rating have been submitted successfully.", "success")
            return redirect(url_for('feedback_page'))
        else:
            flash("Database error: Could not save your feedback. Please try again.", "error")
            return render_template('feedback.html', active_page='feedback', message=message_val, selected_rating=rating)

    return render_template('feedback.html', active_page='feedback')


# ==================== PROTECTED USER ROUTES ====================

@app.route('/history')
@login_required
def history():
    """
    Render the prediction history page showing strictly the logged-in user's
    past identifications. Unauthenticated users are redirected to login.
    """
    user_id = session['user_id']
    predictions = []
    try:
        predictions = get_prediction_history(user_id=user_id, limit=50)
    except Exception as e:
        print(f"[!] Error loading history from database: {e}")
    return render_template('history.html', active_page='history', predictions=predictions)


@app.route('/history/details/<int:prediction_id>')
@login_required
def history_details(prediction_id):
    """
    Return detailed JSON for a specific prediction record (for modal view).
    Protects user data: only the owner can view their prediction details.
    """
    user_id = session['user_id']
    record = get_prediction_by_id(prediction_id, user_id=user_id)
    if not record:
        return jsonify({'success': False, 'message': 'Prediction record not found or access denied.'}), 404

    date_str = record['created_at'].strftime('%B %d, %Y at %I:%M %p') if record.get('created_at') else 'Recent'
    return jsonify({
        'success': True,
        'prediction_id': record['prediction_id'],
        'image_path': record['image_path'],
        'predicted_breed': record['predicted_breed'],
        'confidence': round(float(record['confidence']), 2),
        'top3': record.get('top3_parsed', []),
        'model_version': record.get('model_version', 'MobileNetV2-v1'),
        'created_at': date_str
    })


@app.route('/history/delete/<int:prediction_id>', methods=['POST'])
@login_required
def delete_history_item(prediction_id):
    """Delete an individual prediction record belonging to the logged-in user."""
    user_id = session['user_id']
    delete_prediction(prediction_id, user_id=user_id)
    flash("Prediction record deleted successfully.", "info")
    return redirect(url_for('history'))


@app.route('/history/clear', methods=['POST'])
@login_required
def clear_history():
    """Clear all prediction history belonging to the logged-in user."""
    user_id = session['user_id']
    clear_all_history(user_id=user_id)
    flash("Your prediction history has been cleared.", "info")
    return redirect(url_for('history'))


# ==================== FAVORITES ROUTES ====================

@app.route('/favorites')
@login_required
def favorites():
    """
    Display the logged-in user's personal bookmarked favorite dog breeds.
    Protected with login_required.
    """
    user_id = session['user_id']
    raw_favs = get_user_favorites(user_id)

    # Enrich with breed details from breeds_data.json
    breeds_path = os.path.join(config.DATABASE_FOLDER, 'breeds_data.json')
    breeds_dict = {}
    if os.path.exists(breeds_path):
        with open(breeds_path, 'r', encoding='utf-8') as f:
            for b in json.load(f):
                breeds_dict[b['id']] = b
                breeds_dict[b['name'].lower()] = b

    favorites_list = []
    for f_item in raw_favs:
        raw_name = f_item['breed_name']
        matched = breeds_dict.get(raw_name) or breeds_dict.get(raw_name.lower())
        if matched:
            favorites_list.append({
                'id': matched['id'],
                'raw_name': raw_name,
                'name': matched['name'],
                'origin': matched.get('origin', 'Unknown'),
                'lifespan': matched.get('lifespan', '10-14 years'),
                'temperament': matched.get('temperament', 'Loyal and friendly'),
                'image_url': url_for('static', filename=f"images/breeds/{matched['id']}.jpg")
            })
        else:
            clean_name = format_breed_name(raw_name)
            favorites_list.append({
                'id': raw_name,
                'raw_name': raw_name,
                'name': clean_name,
                'origin': 'Global',
                'lifespan': '10-14 years',
                'temperament': 'Companion dog',
                'image_url': 'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg?auto=compress&cs=tinysrgb&w=400'
            })

    return render_template('favorites.html', active_page='favorites', favorites=favorites_list)


@app.route('/favorites/remove/<breed_name>', methods=['POST'])
@login_required
def remove_favorite(breed_name):
    """Remove a breed from the logged-in user's favorites."""
    user_id = session['user_id']
    remove_favorite_breed(user_id, breed_name)
    flash(f"Removed {format_breed_name(breed_name)} from your favorites.", "info")
    return redirect(url_for('favorites'))


@app.route('/api/favorites/toggle', methods=['POST'])
def api_toggle_favorite():
    """Toggle a favorite breed for the current user via AJAX."""
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'require_login': True,
            'message': 'Please log in to save your favorite breeds.'
        }), 401

    data = request.get_json(silent=True) or request.form.to_dict()
    breed_name = data.get('breed_name')
    if not breed_name:
        return jsonify({'success': False, 'message': 'Breed name is required'}), 400

    user_id = session['user_id']
    if is_favorite_breed(user_id, breed_name):
        remove_favorite_breed(user_id, breed_name)
        return jsonify({'success': True, 'is_favorite': False, 'message': 'Removed from favorites'})
    else:
        add_favorite_breed(user_id, breed_name)
        return jsonify({'success': True, 'is_favorite': True, 'message': 'Saved to favorites'})


# ==================== REPORT DOWNLOAD ROUTES ====================

@app.route('/download_report/<int:prediction_id>')
def download_report_by_id(prediction_id):
    """
    Generate and download a professional PDF prediction report for a saved prediction by ID.
    Uses Python ReportLab.
    """
    user_id = session.get('user_id')
    record = get_prediction_by_id(prediction_id, user_id=user_id)
    if not record:
        flash("Prediction record not found.", "error")
        return redirect(url_for('history'))

    # Prepare data for report generator
    prediction_data = {
        'predicted_breed': record.get('predicted_breed', 'Unknown Breed'),
        'confidence': record.get('confidence', 0.0),
        'top3': record.get('top3_parsed') or [],
        'image_path': record.get('image_path', ''),
        'model_version': record.get('model_version', 'MobileNetV2-v1'),
        'created_at': record.get('created_at')
    }

    try:
        pdf_buffer = generate_prediction_pdf(prediction_data)
        clean_breed = "".join(c for c in record['predicted_breed'] if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
        download_name = f"DogBreedReport_{clean_breed}_{prediction_id}.pdf"
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=download_name,
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"[!] Error generating PDF report: {e}")
        flash(f"Could not generate report: {e}", "error")
        return redirect(url_for('history'))


@app.route('/download_report', methods=['GET', 'POST'])
def download_report():
    """
    Generate and download a professional PDF report immediately from request data.
    Allows instant download from the /identify prediction result card even before/without DB access.
    """
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form.to_dict()
    else:
        data = request.args.to_dict()

    if not data:
        return jsonify({'error': 'No prediction data provided for report.'}), 400

    # Parse top3 if passed as a JSON string
    top3 = data.get('top3', [])
    if isinstance(top3, str):
        try:
            top3 = json.loads(top3)
        except Exception:
            top3 = []

    breed_name = data.get('predicted_breed') or data.get('top_breed', 'Unknown Breed')
    conf_val = data.get('confidence') or data.get('top_confidence', 0.0)
    img_name = data.get('image_path') or data.get('filename', '')
    mod_ver = data.get('model_version', 'MobileNetV2-v1')
    dt_str = data.get('created_at') or data.get('timestamp') or datetime.now().strftime('%B %d, %Y at %I:%M %p')

    prediction_data = {
        'predicted_breed': breed_name,
        'confidence': conf_val,
        'top3': top3,
        'image_path': img_name,
        'model_version': mod_ver,
        'created_at': dt_str
    }

    try:
        pdf_buffer = generate_prediction_pdf(prediction_data)
        clean_breed = "".join(c for c in str(breed_name) if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
        timestamp_tag = datetime.now().strftime('%Y%m%d_%H%M%S')
        download_name = f"DogBreedReport_{clean_breed}_{timestamp_tag}.pdf"
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=download_name,
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"[!] Error generating PDF report: {e}")
        return jsonify({'error': f"Failed to generate PDF: {str(e)}"}), 500


# ==================== PREDICTION ROUTE ====================

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receive an uploaded dog image, preprocess to 224x224 RGB,
    run prediction using MobileNetV2, and return top 3 breeds.
    """
    if model is None or not class_names:
        return jsonify({
            'success': False,
            'title': 'Model Not Available',
            'message': 'The prediction model could not be loaded. Please ensure best_model.keras exists in the model folder.'
        })

    # Check if a file was included in the request
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'title': 'No File Received',
            'message': 'Please select an image file before clicking Predict.'
        })

    file = request.files['file']

    # Check if a filename is present
    if file.filename == '':
        return jsonify({
            'success': False,
            'title': 'No File Selected',
            'message': 'The uploaded file has no name. Please try again.'
        })

    # Validate file extension
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'title': 'Invalid File Type',
            'message': 'Only JPG, JPEG, and PNG files are allowed.'
        })

    try:
        # Sanitize filename and fallback if needed
        raw_filename = file.filename
        safe_name = secure_filename(raw_filename)
        if not safe_name:
            ext = raw_filename.rsplit('.', 1)[-1].lower() if '.' in raw_filename else 'jpg'
            safe_name = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"

        filename = safe_name
        save_path = os.path.join(config.UPLOAD_FOLDER, filename)
        file.save(save_path)

        # Preprocess image: convert to RGB and resize to 224x224
        img = Image.open(save_path).convert('RGB')
        img = img.resize((224, 224))

        # Convert to numpy array and apply MobileNetV2 preprocessing [-1, 1]
        img_array = np.array(img, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Stage 1: Validate whether the image contains a dog
        is_dog, dog_prob = is_dog_image(img_array)
        if not is_dog:
            return jsonify({
                'success': False,
                'is_dog': False,
                'title': 'No Dog Detected',
                'message': 'No dog detected. Please upload a valid dog image.'
            })

        # Stage 2: Dog Breed Identification (120 breeds)
        predictions = model.predict(img_array, verbose=0)[0]

        # Extract top 3 predictions
        top3_indices = np.argsort(predictions)[-3:][::-1]

        top3 = []
        for idx in top3_indices:
            raw_name = class_names[idx]
            conf = float(predictions[idx]) * 100.0
            top3.append({
                'breed': format_breed_name(raw_name),
                'raw_breed': raw_name,
                'confidence': round(conf, 2)
            })

        top_pred = top3[0]

        # Stage 3: Save real prediction history to database (if available)
        saved_id = None
        try:
            user_id = session.get('user_id')
            saved_id = save_prediction(
                image_path=filename,
                predicted_breed=top_pred['breed'],
                confidence=top_pred['confidence'],
                top3_results=top3,
                user_id=user_id,
                model_version='MobileNetV2-v1'
            )
            if saved_id:
                print(f"[+] Prediction recorded in database: ID #{saved_id} ({top_pred['breed']}, {top_pred['confidence']}%)")
            else:
                print("[!] Notice: Prediction was not saved to database. Check database connection and .env credentials.")
        except Exception as db_err:
            print(f"[!] Warning: Could not save prediction to database: {db_err}")

        timestamp_str = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        return jsonify({
            'success': True,
            'top_breed': top_pred['breed'],
            'top_confidence': top_pred['confidence'],
            'top3': top3,
            'filename': filename,
            'prediction_id': saved_id,
            'model_version': 'MobileNetV2-v1',
            'timestamp': timestamp_str
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'title': 'Prediction Error',
            'message': f'Failed to process the image: {str(e)}'
        })



# ==================== ADMIN DASHBOARD ROUTES ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """
    Admin-only dashboard: aggregated statistics from MySQL.
    Requires is_admin = 1 in the users table.
    """
    stats = get_admin_stats()
    return render_template('admin.html', stats=stats, active_page='admin')


@app.route('/admin/grant', methods=['GET', 'POST'])
@admin_required
def admin_grant():
    """
    Admin helper: grant or revoke admin status for another user by user_id.
    POST body: { user_id, action }  action = 'grant' | 'revoke'
    Returns JSON for AJAX calls.
    """
    if request.method == 'POST':
        data      = request.get_json(silent=True) or request.form
        target_id = data.get('user_id')
        action    = data.get('action', 'grant')
        if not target_id:
            return jsonify({'success': False, 'message': 'user_id required'}), 400
        is_admin_flag = (action == 'grant')
        ok = set_user_admin(int(target_id), is_admin=is_admin_flag)
        verb = 'granted' if is_admin_flag else 'revoked'
        return jsonify({'success': ok, 'message': f'Admin {verb}.' if ok else 'Update failed.'})
    # GET — just redirect back to dashboard
    return redirect(url_for('admin_dashboard'))


# ==================== RUN SERVER ====================

if __name__ == '__main__':
    print("\n[*] Dog Breed Identification Server Starting...")
    print("    Open http://127.0.0.1:5000 in your browser\n")
    app.run(debug=config.DEBUG)
