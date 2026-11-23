"""
database/db.py
==============
MySQL Database Utility Module for Dog Breed Identification Project.

Handles connection management, parameterized SQL execution, and table operations
for users, prediction_history, favorite_breeds, and feedback.
Credentials are read securely from environment variables via config.py.
"""

import os
import json
import mysql.connector
from mysql.connector import Error
import config


def get_db_connection(include_database=True):
    """
    Establish and return a MySQL database connection.
    Uses credentials from config.py (read dynamically from environment).
    """
    try:
        db_cfg = config.get_db_config()
        kwargs = {
            'host': db_cfg['host'],
            'port': db_cfg['port'],
            'user': db_cfg['user'],
            'password': db_cfg['password'],
        }
        if include_database:
            kwargs['database'] = db_cfg['database']

        connection = mysql.connector.connect(**kwargs)
        return connection
    except Error as e:
        print(f"[!] Database Connection Error: {e} (Host: {config.DB_HOST}, User: {config.DB_USER}, DB: {config.DB_NAME})")
        return None


def test_db_connection():
    """
    Test database connection and verify presence of required tables.
    Logs status to terminal. Returns (success: bool, message: str).
    """
    conn = get_db_connection(include_database=True)
    if conn is None:
        msg = f"Failed to connect to MySQL ({config.DB_USER}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}). Check credentials in .env"
        print(f"[!] Database Status: {msg}")
        return False, msg

    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        cursor.close()
        conn.close()
        msg = f"Connected to MySQL database '{config.DB_NAME}' successfully! Tables: {', '.join(tables)}"
        print(f"[*] Database Status: {msg}")
        return True, msg
    except Error as e:
        msg = f"Error querying MySQL: {e}"
        print(f"[!] Database Status: {msg}")
        if conn and conn.is_connected():
            conn.close()
        return False, msg


def init_db():
    """
    Initialize the database and tables using database_setup.sql.
    Can be run when setting up the project.
    """
    sql_path = os.path.join(config.DATABASE_FOLDER, 'database_setup.sql')
    if not os.path.exists(sql_path):
        print(f"[!] SQL file not found at: {sql_path}")
        return False

    # Connect to MySQL server (without specifying DB, so we can create it)
    conn = get_db_connection(include_database=False)
    if conn is None:
        print("[!] Could not connect to MySQL server. Check credentials in .env.")
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Execute statements separated by semicolons
        statements = sql_script.split(';')
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)

        conn.commit()
        print("[*] Database and tables initialized successfully!")
        return True
    except Error as e:
        print(f"[!] Error initializing database: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ==============================================================
#  PREDICTION HISTORY OPERATIONS
# ==============================================================

def save_prediction(image_path, predicted_breed, confidence, top3_results, user_id=None, model_version='MobileNetV2-v1'):
    """
    Save a real prediction record into prediction_history using parameterized query.
    top3_results can be passed as a dict/list or JSON string.
    Returns the new prediction_id on success, or None on failure.
    """
    conn = get_db_connection(include_database=True)
    if conn is None:
        print("[!] Database Error: Cannot save prediction because MySQL connection failed.")
        return None

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO prediction_history
                (user_id, image_path, predicted_breed, confidence, top3_results, model_version)
            VALUES
                (%s, %s, %s, %s, %s, %s)
        """
        # Ensure top3_results is serialized as JSON string
        top3_json = top3_results if isinstance(top3_results, str) else json.dumps(top3_results)
        
        cursor.execute(query, (
            user_id,
            image_path,
            predicted_breed,
            float(confidence),
            top3_json,
            model_version
        ))
        conn.commit()
        new_id = cursor.lastrowid
        print(f"[+] Prediction recorded in database: ID #{new_id} ({predicted_breed}, {float(confidence):.2f}%)")
        return new_id
    except Error as e:
        print(f"[!] Database INSERT Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_prediction_history(user_id=None, limit=50):
    """
    Retrieve recent real predictions from prediction_history ordered by date.
    If user_id is provided, filters strictly for that user's history.
    Returns a list of dictionaries.
    """
    conn = get_db_connection(include_database=True)
    if conn is None:
        print("[!] Database Error: Cannot fetch history because MySQL connection failed.")
        return []

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        if user_id is not None:
            query = """
                SELECT
                    prediction_id, user_id, image_path, predicted_breed,
                    confidence, top3_results, model_version, created_at
                FROM prediction_history
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """
            cursor.execute(query, (user_id, int(limit)))
        else:
            query = """
                SELECT
                    prediction_id, user_id, image_path, predicted_breed,
                    confidence, top3_results, model_version, created_at
                FROM prediction_history
                ORDER BY created_at DESC
                LIMIT %s
            """
            cursor.execute(query, (int(limit),))

        rows = cursor.fetchall()

        # Parse top3_results JSON string for each row
        for row in rows:
            if row.get('top3_results'):
                try:
                    row['top3_parsed'] = json.loads(row['top3_results'])
                except Exception:
                    row['top3_parsed'] = []
            else:
                row['top3_parsed'] = []

        print(f"[*] Retrieved {len(rows)} prediction records from database.")
        return rows
    except Error as e:
        print(f"[!] Database SELECT Error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_prediction_by_id(prediction_id, user_id=None):
    """
    Fetch a single prediction record by ID.
    If user_id is provided, ensures user can only access their own prediction.
    """
    conn = get_db_connection(include_database=True)
    if conn is None:
        return None

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        if user_id is not None:
            query = """
                SELECT
                    prediction_id, user_id, image_path, predicted_breed,
                    confidence, top3_results, model_version, created_at
                FROM prediction_history
                WHERE prediction_id = %s AND user_id = %s
            """
            cursor.execute(query, (prediction_id, user_id))
        else:
            query = """
                SELECT
                    prediction_id, user_id, image_path, predicted_breed,
                    confidence, top3_results, model_version, created_at
                FROM prediction_history
                WHERE prediction_id = %s
            """
            cursor.execute(query, (prediction_id,))

        row = cursor.fetchone()
        if row and row.get('top3_results'):
            try:
                row['top3_parsed'] = json.loads(row['top3_results'])
            except Exception:
                row['top3_parsed'] = []
        return row
    except Error as e:
        print(f"[!] Error fetching prediction #{prediction_id}: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_prediction(prediction_id, user_id=None):
    """
    Delete a single prediction record from prediction_history.
    If user_id is provided, ensures user can only delete their own records.
    Returns True if deleted, False otherwise.
    """
    conn = get_db_connection(include_database=True)
    if conn is None:
        print("[!] Database Error: Cannot delete prediction because MySQL connection failed.")
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        if user_id is not None:
            query = "DELETE FROM prediction_history WHERE prediction_id = %s AND user_id = %s"
            cursor.execute(query, (prediction_id, user_id))
        else:
            query = "DELETE FROM prediction_history WHERE prediction_id = %s"
            cursor.execute(query, (prediction_id,))

        conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            print(f"[+] Prediction #{prediction_id} deleted successfully.")
        else:
            print(f"[!] No prediction record found with ID #{prediction_id} to delete.")
        return deleted
    except Error as e:
        print(f"[!] Database DELETE Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def clear_all_history(user_id=None):
    """
    Delete all prediction history.
    If user_id is provided, deletes only that user's history.
    """
    conn = get_db_connection(include_database=True)
    if conn is None:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        if user_id is not None:
            query = "DELETE FROM prediction_history WHERE user_id = %s"
            cursor.execute(query, (user_id,))
        else:
            query = "DELETE FROM prediction_history"
            cursor.execute(query)

        conn.commit()
        count = cursor.rowcount
        print(f"[+] Cleared {count} prediction history records.")
        return True
    except Error as e:
        print(f"[!] Database CLEAR Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ==============================================================
#  USER OPERATIONS
# ==============================================================

def create_user(username, email, password_hash):
    """
    Insert a new user using parameterized query.
    Returns new user_id if successful, None otherwise.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (username, email, password_hash))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"[!] Error creating user: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_user_by_username(username):
    """
    Fetch a user record by username using parameterized query.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT user_id, username, email, password_hash, is_admin, created_at FROM users WHERE username = %s"
        cursor.execute(query, (username.strip(),))
        return cursor.fetchone()
    except Error as e:
        print(f"[!] Error getting user by username: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_user_by_email(email):
    """
    Fetch a user record by email using parameterized query.
    Used to prevent duplicate email registration and allow email login.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT user_id, username, email, password_hash, is_admin, created_at FROM users WHERE email = %s"
        cursor.execute(query, (email.strip().lower(),))
        return cursor.fetchone()
    except Error as e:
        print(f"[!] Error getting user by email: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_user_by_id(user_id):
    """
    Fetch a user record by user_id.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT user_id, username, email, is_admin, created_at FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"[!] Error getting user by id: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ==============================================================
#  FAVORITE BREEDS OPERATIONS
# ==============================================================

def add_favorite_breed(user_id, breed_name):
    """
    Bookmark a breed for a user.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            INSERT IGNORE INTO favorite_breeds (user_id, breed_name)
            VALUES (%s, %s)
        """
        cursor.execute(query, (user_id, breed_name))
        conn.commit()
        return True
    except Error as e:
        print(f"[!] Error adding favorite breed: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def remove_favorite_breed(user_id, breed_name):
    """
    Remove a bookmarked breed for a user.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        query = "DELETE FROM favorite_breeds WHERE user_id = %s AND breed_name = %s"
        cursor.execute(query, (user_id, breed_name))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[!] Error removing favorite breed: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def is_favorite_breed(user_id, breed_name):
    """
    Check if a breed is bookmarked by a user.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        query = "SELECT 1 FROM favorite_breeds WHERE user_id = %s AND breed_name = %s LIMIT 1"
        cursor.execute(query, (user_id, breed_name))
        return cursor.fetchone() is not None
    except Error as e:
        print(f"[!] Error checking favorite breed: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_user_favorites(user_id):
    """
    Get all favorite breeds for a given user.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT favorite_id, breed_name FROM favorite_breeds WHERE user_id = %s ORDER BY favorite_id DESC"
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"[!] Error fetching user favorites: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ==============================================================
#  FEEDBACK OPERATIONS
# ==============================================================

def save_feedback(message, rating, user_id=None):
    """
    Save user feedback and star rating (1 to 5).
    """
    if rating < 1 or rating > 5:
        print("[!] Rating must be between 1 and 5.")
        return False

    conn = get_db_connection()
    if conn is None:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO feedback (user_id, message, rating)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (user_id, message, int(rating)))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"[!] Error saving feedback: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ==============================================================
#  ADMIN OPERATIONS
# ==============================================================

def set_user_admin(user_id, is_admin=True):
    """
    Grant or revoke admin privileges for a user.
    Returns True on success, False otherwise.
    """
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET is_admin = %s WHERE user_id = %s",
            (1 if is_admin else 0, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[!] Error updating admin status: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_admin_stats():
    """
    Gather all statistics for the admin dashboard in a single DB session.
    Returns a dict with keys:
      total_users, total_admins, total_predictions, total_feedback,
      avg_rating, avg_confidence, top_breeds, breed_chart_labels,
      breed_chart_data, recent_users, recent_feedback,
      daily_labels, daily_data, model_versions.
    """
    conn = get_db_connection()
    if conn is None:
        return {}
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        stats = {}

        # 1. Total users & admins
        cursor.execute("SELECT COUNT(*) AS cnt FROM users")
        stats['total_users'] = cursor.fetchone()['cnt']

        cursor.execute("SELECT COUNT(*) AS cnt FROM users WHERE is_admin = 1")
        stats['total_admins'] = cursor.fetchone()['cnt']

        # 2. Total predictions
        cursor.execute("SELECT COUNT(*) AS cnt FROM prediction_history")
        stats['total_predictions'] = cursor.fetchone()['cnt']

        # 3. Total feedback + avg rating
        cursor.execute(
            "SELECT COUNT(*) AS cnt, COALESCE(AVG(rating), 0) AS avg_r FROM feedback"
        )
        row = cursor.fetchone()
        stats['total_feedback'] = row['cnt']
        stats['avg_rating'] = round(float(row['avg_r']), 2)

        # 4. Average confidence across all predictions
        cursor.execute(
            "SELECT COALESCE(AVG(confidence), 0) AS avg_c FROM prediction_history"
        )
        stats['avg_confidence'] = round(float(cursor.fetchone()['avg_c']), 2)

        # 5. Top 10 most predicted breeds
        cursor.execute("""
            SELECT predicted_breed AS breed, COUNT(*) AS cnt
            FROM prediction_history
            GROUP BY predicted_breed
            ORDER BY cnt DESC
            LIMIT 10
        """)
        top_breeds = cursor.fetchall()
        stats['top_breeds'] = top_breeds
        stats['breed_chart_labels'] = [b['breed'] for b in top_breeds]
        stats['breed_chart_data']   = [int(b['cnt']) for b in top_breeds]

        # 6. Last 10 registered users
        cursor.execute("""
            SELECT user_id, username, email, is_admin, created_at
            FROM users
            ORDER BY created_at DESC
            LIMIT 10
        """)
        stats['recent_users'] = cursor.fetchall()

        # 7. Last 5 feedback rows
        cursor.execute("""
            SELECT f.feedback_id, f.message, f.rating, f.created_at,
                   COALESCE(u.username, 'Guest') AS username
            FROM feedback f
            LEFT JOIN users u ON f.user_id = u.user_id
            ORDER BY f.created_at DESC
            LIMIT 5
        """)
        stats['recent_feedback'] = cursor.fetchall()

        # 8. Predictions per day — last 14 calendar days
        cursor.execute("""
            SELECT DATE(created_at) AS day, COUNT(*) AS cnt
            FROM prediction_history
            WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 13 DAY)
            GROUP BY DATE(created_at)
            ORDER BY day ASC
        """)
        daily_rows = cursor.fetchall()
        stats['daily_labels'] = [str(r['day']) for r in daily_rows]
        stats['daily_data']   = [int(r['cnt']) for r in daily_rows]

        # 9. Model version breakdown
        cursor.execute("""
            SELECT COALESCE(model_version, 'Unknown') AS model_version,
                   COUNT(*) AS cnt
            FROM prediction_history
            GROUP BY model_version
            ORDER BY cnt DESC
        """)
        stats['model_versions'] = cursor.fetchall()

        return stats
    except Error as e:
        print(f"[!] Admin stats query error: {e}")
        return {}
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
