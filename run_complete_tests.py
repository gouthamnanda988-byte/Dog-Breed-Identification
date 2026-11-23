"""
run_complete_tests.py
======================
Comprehensive automated testing suite for Dog Breed Identification project.
Validates all 18 checkpoints and prints genuine results.
"""

import os
import sys
import io
import json
from datetime import datetime

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from app import app, model, class_names, dog_detector
import config
from database.db import (
    get_db_connection,
    test_db_connection,
    create_user,
    get_user_by_username,
    get_admin_stats
)

results = {}

def report(item_no, title, passed, details=""):
    status = "PASS" if passed else "FAIL"
    results[item_no] = (status, title, details)
    tag = "[PASS]" if passed else "[FAIL]"
    print(f"{tag} #{item_no:02d}: {title}")
    if details:
        print(f"       -> {details}")

print("=" * 70)
print("  DOG BREED IDENTIFICATION - COMPLETE 18-POINT SYSTEM REVIEW")
print("=" * 70)

created_user_id = None

with app.test_client() as client:

    # -------------------------------------------------------------
    # 1. Flask Application Startup
    # -------------------------------------------------------------
    try:
        is_flask = (app is not None and app.name == 'app')
        has_secret = bool(app.secret_key)
        report(1, "Flask application startup", is_flask and has_secret,
               f"App initialized. Secret key configured: {has_secret}")
    except Exception as e:
        report(1, "Flask application startup", False, str(e))

    # -------------------------------------------------------------
    # 2. Homepage Navigation
    # -------------------------------------------------------------
    try:
        res = client.get('/')
        has_home = (res.status_code == 200 and b"Dog Breed Identification" in res.data)
        has_nav_links = (b"/identify" in res.data and b"/breeds" in res.data and b"/performance" in res.data)
        report(2, "Homepage navigation", has_home and has_nav_links,
               f"Status: {res.status_code}, Navigation links verified in base template.")
    except Exception as e:
        report(2, "Homepage navigation", False, str(e))

    # -------------------------------------------------------------
    # 3. Image Upload
    # -------------------------------------------------------------
    dog_img_path = os.path.join(config.UPLOAD_FOLDER, 'dog.jpg')
    try:
        with open(dog_img_path, 'rb') as f:
            data = {'file': (io.BytesIO(f.read()), 'test_dog_upload.jpg')}
        res = client.post('/predict', data=data, content_type='multipart/form-data')
        json_data = res.get_json()
        upload_success = (res.status_code == 200 and json_data and json_data.get('success') is True)
        report(3, "Image upload", upload_success,
               f"Status: {res.status_code}, Image saved and processed successfully.")
    except Exception as e:
        report(3, "Image upload", False, str(e))

    # -------------------------------------------------------------
    # 4. Invalid Image Handling
    # -------------------------------------------------------------
    try:
        # Case A: No file in request
        res1 = client.post('/predict', data={})
        j1 = res1.get_json()
        ok1 = (j1.get('title') == 'No File Received')

        # Case B: Disallowed extension
        data_bad_ext = {'file': (io.BytesIO(b"Hello world"), 'test.txt')}
        res2 = client.post('/predict', data=data_bad_ext, content_type='multipart/form-data')
        j2 = res2.get_json()
        ok2 = (j2.get('title') == 'Invalid File Type')

        # Case C: Corrupted image file with jpg extension
        data_corrupt = {'file': (io.BytesIO(b"Not a real JPEG content"), 'corrupt.jpg')}
        res3 = client.post('/predict', data=data_corrupt, content_type='multipart/form-data')
        j3 = res3.get_json()
        ok3 = (j3.get('title') == 'Prediction Error')

        all_invalid_ok = ok1 and ok2 and ok3
        report(4, "Invalid image handling", all_invalid_ok,
               f"No-file: {ok1}, Bad-extension: {ok2}, Corrupted-data: {ok3}")
    except Exception as e:
        report(4, "Invalid image handling", False, str(e))

    # -------------------------------------------------------------
    # 5. Dog/Non-Dog Validation
    # -------------------------------------------------------------
    try:
        horse_img_path = os.path.join(config.UPLOAD_FOLDER, 'Black-Horse-Names-with-Meanings.jpeg')
        with open(horse_img_path, 'rb') as f:
            data_horse = {'file': (io.BytesIO(f.read()), 'test_horse.jpeg')}
        res_horse = client.post('/predict', data=data_horse, content_type='multipart/form-data')
        j_horse = res_horse.get_json()
        is_rejected = (j_horse.get('success') is False and j_horse.get('is_dog') is False)

        with open(dog_img_path, 'rb') as f:
            data_dog = {'file': (io.BytesIO(f.read()), 'test_dog.jpg')}
        res_dog = client.post('/predict', data=data_dog, content_type='multipart/form-data')
        j_dog = res_dog.get_json()
        is_accepted = (j_dog.get('success') is True)

        dog_val_ok = is_rejected and is_accepted
        report(5, "Dog/non-dog validation", dog_val_ok,
               f"Non-dog rejected: {is_rejected} ('{j_horse.get('title')}'), Dog accepted: {is_accepted}")
    except Exception as e:
        report(5, "Dog/non-dog validation", False, str(e))

    # -------------------------------------------------------------
    # 6. ML Model Loading
    # -------------------------------------------------------------
    try:
        model_loaded = (model is not None)
        in_shape = model.input_shape if model else None
        out_shape = model.output_shape if model else None
        classes_ok = (len(class_names) == 120)
        report(6, "ML model loading", model_loaded and classes_ok,
               f"Model: MobileNetV2, Input shape: {in_shape}, Output shape: {out_shape}, Classes: {len(class_names)}")
    except Exception as e:
        report(6, "ML model loading", False, str(e))

    # -------------------------------------------------------------
    # 7. Breed Prediction
    # -------------------------------------------------------------
    try:
        with open(dog_img_path, 'rb') as f:
            data_pred = {'file': (io.BytesIO(f.read()), 'predict_check.jpg')}
        res_pred = client.post('/predict', data=data_pred, content_type='multipart/form-data')
        j_pred = res_pred.get_json()
        top_breed = j_pred.get('top_breed')
        top_conf = j_pred.get('top_confidence')
        pred_ok = (j_pred.get('success') is True and bool(top_breed) and top_conf > 0)
        report(7, "Breed prediction", pred_ok,
               f"Predicted: '{top_breed}' with {top_conf}% confidence.")
    except Exception as e:
        report(7, "Breed prediction", False, str(e))

    # -------------------------------------------------------------
    # 8. Top 3 Confidence Scores
    # -------------------------------------------------------------
    try:
        top3 = j_pred.get('top3', [])
        has_3 = (len(top3) == 3)
        sorted_desc = (top3[0]['confidence'] >= top3[1]['confidence'] >= top3[2]['confidence'])
        valid_ranges = all(0 <= item['confidence'] <= 100 for item in top3)
        top3_ok = has_3 and sorted_desc and valid_ranges
        scores_str = ", ".join(f"#{i+1} {item['breed']} ({item['confidence']}%)" for i, item in enumerate(top3))
        report(8, "Top 3 confidence scores", top3_ok,
               f"Scores: {scores_str} | Sorted descending: {sorted_desc}")
    except Exception as e:
        report(8, "Top 3 confidence scores", False, str(e))

    # -------------------------------------------------------------
    # 9. MySQL Database Connection
    # -------------------------------------------------------------
    try:
        conn = get_db_connection()
        db_connected = (conn is not None and conn.is_connected())
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        expected_tables = {'users', 'prediction_history', 'favorite_breeds', 'feedback'}
        has_all_tables = expected_tables.issubset(set(tables))
        cursor.execute("SHOW COLUMNS FROM users LIKE 'is_admin'")
        has_is_admin = bool(cursor.fetchone())
        cursor.close()
        conn.close()
        db_ok = db_connected and has_all_tables and has_is_admin
        report(9, "MySQL database connection", db_ok,
               f"Connected to '{config.DB_NAME}'. Tables: {tables}. Admin column present: {has_is_admin}")
    except Exception as e:
        report(9, "MySQL database connection", False, str(e))

    # -------------------------------------------------------------
    # 10. Signup and Login
    # -------------------------------------------------------------
    test_user = "test_review_bot"
    test_email = "test_review_bot@example.com"
    test_pass = "SecurePass123!"
    try:
        # Cleanup if previously exists
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE username = %s OR email = %s", (test_user, test_email))
            conn.commit()
            cur.close()
            conn.close()

        # Signup
        res_signup = client.post('/signup', data={
            'username': test_user,
            'email': test_email,
            'password': test_pass,
            'confirm_password': test_pass
        }, follow_redirects=False)
        signup_ok = (res_signup.status_code == 302 and '/login' in res_signup.headers['Location'])

        # Duplicate signup prevention
        res_dup = client.post('/signup', data={
            'username': test_user,
            'email': test_email,
            'password': test_pass,
            'confirm_password': test_pass
        }, follow_redirects=True)
        dup_prevented = (b"already registered" in res_dup.data or b"already taken" in res_dup.data)

        # Login with correct password
        res_login = client.post('/login', data={
            'login_identifier': test_user,
            'password': test_pass
        }, follow_redirects=False)
        login_ok = (res_login.status_code == 302)

        # Check session
        with client.session_transaction() as sess:
            session_ok = (sess.get('username') == test_user and 'user_id' in sess)
            created_user_id = sess.get('user_id')

        # Logout
        client.get('/logout')
        with client.session_transaction() as sess:
            logout_ok = ('user_id' not in sess)

        auth_ok = signup_ok and dup_prevented and login_ok and session_ok and logout_ok
        report(10, "Signup and login", auth_ok,
               f"Signup: {signup_ok}, Duplicate check: {dup_prevented}, Login: {login_ok}, Session: {session_ok}, Logout: {logout_ok}")
    except Exception as e:
        report(10, "Signup and login", False, str(e))

    # -------------------------------------------------------------
    # 11. Prediction History
    # -------------------------------------------------------------
    try:
        # Guest access blocked
        res_guest = client.get('/history')
        guest_blocked = (res_guest.status_code == 302 and 'login' in res_guest.headers['Location'])

        # Log in as test user
        with client.session_transaction() as sess:
            sess['user_id'] = created_user_id or 2
            sess['username'] = test_user
            sess['is_admin'] = False

        res_auth_hist = client.get('/history')
        auth_hist_ok = (res_auth_hist.status_code == 200 and b"Prediction History" in res_auth_hist.data)

        report(11, "Prediction history", guest_blocked and auth_hist_ok,
               f"Guest blocked: {guest_blocked} (302->Login), Authenticated history: {auth_hist_ok} (200 OK)")
    except Exception as e:
        report(11, "Prediction history", False, str(e))

    # -------------------------------------------------------------
    # 12. Favourite Breeds
    # -------------------------------------------------------------
    try:
        with client.session_transaction() as sess:
            sess['user_id'] = created_user_id or 2
            sess['username'] = test_user

        # Toggle add favorite
        res_fav_add = client.post('/api/favorites/toggle', json={'breed_name': 'Samoyed'})
        j_fav1 = res_fav_add.get_json()
        added_ok = (j_fav1.get('success') is True and j_fav1.get('is_favorite') is True)

        # Favorites page renders
        res_fav_page = client.get('/favorites')
        fav_page_ok = (res_fav_page.status_code == 200 and b"Favorite Breeds" in res_fav_page.data)

        # Toggle remove favorite
        res_fav_rem = client.post('/api/favorites/toggle', json={'breed_name': 'Samoyed'})
        j_fav2 = res_fav_rem.get_json()
        removed_ok = (j_fav2.get('success') is True and j_fav2.get('is_favorite') is False)

        fav_ok = added_ok and fav_page_ok and removed_ok
        report(12, "Favourite breeds", fav_ok,
               f"Add favorite: {added_ok}, Favorites page: {fav_page_ok}, Remove favorite: {removed_ok}")
    except Exception as e:
        report(12, "Favourite breeds", False, str(e))

    # -------------------------------------------------------------
    # 13. Breed Info Page
    # -------------------------------------------------------------
    try:
        res_breeds = client.get('/breeds')
        res_api_breeds = client.get('/api/breeds')
        breeds_json = res_api_breeds.get_json()
        has_120 = (len(breeds_json) == 120)
        breeds_page_ok = (res_breeds.status_code == 200 and b"Dog Breed Directory" in res_breeds.data)
        report(13, "Breed Info page", breeds_page_ok and has_120,
               f"Status: {res_breeds.status_code}, Loaded all 120 breeds via /api/breeds.")
    except Exception as e:
        report(13, "Breed Info page", False, str(e))

    # -------------------------------------------------------------
    # 14. Breed Comparison
    # -------------------------------------------------------------
    try:
        b1 = breeds_json[0]
        b2 = breeds_json[1]
        fields = ['temperament', 'size', 'lifespan', 'origin', 'description']
        all_fields_present = all(f in b1 and f in b2 for f in fields)
        has_compare_markup = (b"compareSection" in res_breeds.data and b"breedSelect1" in res_breeds.data and b"breedSelect2" in res_breeds.data)
        report(14, "Breed comparison", all_fields_present and has_compare_markup,
               f"Side-by-side comparison fields: {fields}. Markup present: {has_compare_markup}")
    except Exception as e:
        report(14, "Breed comparison", False, str(e))

    # -------------------------------------------------------------
    # 15. Model Performance Charts
    # -------------------------------------------------------------
    try:
        res_perf = client.get('/performance')
        res_api_perf = client.get('/api/performance')
        j_perf = res_api_perf.get_json()
        has_acc = ('overall' in j_perf and 'test_accuracy' in j_perf['overall'])
        has_confusions = (len(j_perf.get('top_confusions', [])) >= 10)
        perf_page_ok = (res_perf.status_code == 200 and b"Model Performance Analysis" in res_perf.data)
        report(15, "Model performance charts", perf_page_ok and has_acc and has_confusions,
               f"Performance page: 200 OK, Test accuracy: {j_perf['overall']['test_accuracy']}%, Confused breed pairs: {len(j_perf.get('top_confusions', []))}")
    except Exception as e:
        report(15, "Model performance charts", False, str(e))

    # -------------------------------------------------------------
    # 16. PDF Report Download
    # -------------------------------------------------------------
    try:
        pdf_payload = {
            'predicted_breed': 'Golden Retriever',
            'confidence': 94.50,
            'top3': [
                {'breed': 'Golden Retriever', 'confidence': 94.50},
                {'breed': 'Labrador Retriever', 'confidence': 3.20},
                {'breed': 'Chesapeake Bay Retriever', 'confidence': 1.10}
            ],
            'filename': 'dog.jpg',
            'model_version': 'MobileNetV2-v1'
        }
        res_pdf = client.post('/download_report', json=pdf_payload)
        is_pdf_content = (res_pdf.status_code == 200 and res_pdf.mimetype == 'application/pdf')
        has_pdf_header = res_pdf.data.startswith(b'%PDF')
        report(16, "PDF report download", is_pdf_content and has_pdf_header,
               f"Status: {res_pdf.status_code}, Mime: {res_pdf.mimetype}, Size: {len(res_pdf.data)} bytes, Header: %PDF")
    except Exception as e:
        report(16, "PDF report download", False, str(e))

    # -------------------------------------------------------------
    # 17. Admin Dashboard Access Control
    # -------------------------------------------------------------
    try:
        # A. Guest -> 302 to login
        client.get('/logout')
        res_adm_guest = client.get('/admin')
        guest_blocked_adm = (res_adm_guest.status_code == 302 and 'login' in res_adm_guest.headers['Location'])

        # B. Non-admin user -> 403 Forbidden
        with client.session_transaction() as sess:
            sess['user_id'] = created_user_id or 999
            sess['username'] = test_user
            sess['is_admin'] = False
        res_adm_user = client.get('/admin')
        user_blocked_adm = (res_adm_user.status_code == 403 and b"403" in res_adm_user.data)

        # C. Admin user -> 200 OK
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['username'] = 'Goutham'
            sess['is_admin'] = True
        res_adm_ok = client.get('/admin')
        admin_allowed = (res_adm_ok.status_code == 200 and b"Admin Dashboard" in res_adm_ok.data)

        adm_ok = guest_blocked_adm and user_blocked_adm and admin_allowed
        report(17, "Admin dashboard access control", adm_ok,
               f"Guest: {res_adm_guest.status_code} (302), Regular User: {res_adm_user.status_code} (403), Admin: {res_adm_ok.status_code} (200)")
    except Exception as e:
        report(17, "Admin dashboard access control", False, str(e))

    # -------------------------------------------------------------
    # 18. Responsive Design
    # -------------------------------------------------------------
    try:
        with open('templates/base.html', encoding='utf-8') as f:
            base_html = f.read()
        has_viewport = ('name="viewport"' in base_html and 'width=device-width' in base_html)
        has_nav_toggle = ('id="navToggle"' in base_html)

        with open('static/css/style.css', encoding='utf-8') as f:
            css_content = f.read()
        breakpoints = ['max-width: 900px', 'max-width: 768px', 'max-width: 600px', 'max-width: 480px']
        has_all_bp = all(bp in css_content for bp in breakpoints)

        report(18, "Responsive design", has_viewport and has_nav_toggle and has_all_bp,
               f"Viewport meta: {has_viewport}, Mobile nav toggle: {has_nav_toggle}, Breakpoints (480px, 600px, 768px, 900px): {has_all_bp}")
    except Exception as e:
        report(18, "Responsive design", False, str(e))

    # Cleanup test user
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE username = %s OR email = %s", (test_user, test_email))
            conn.commit()
            cur.close()
            conn.close()
    except Exception:
        pass

print("=" * 70)
total_tests = len(results)
passed_tests = sum(1 for s, _, _ in results.values() if s == "PASS")
print(f"  TOTAL REVIEW SCORE: {passed_tests} / {total_tests} PASSED")
print("=" * 70)
