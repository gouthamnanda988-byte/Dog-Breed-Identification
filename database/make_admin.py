"""
database/make_admin.py
======================
One-time utility script: grant admin privileges to an existing user.

Usage (run once from project root):
    python database/make_admin.py

You will be prompted for the username you want to promote to admin.
The user MUST already be registered via the Sign Up page.
"""

import sys
import os

# Allow importing from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db_connection, set_user_admin
from mysql.connector import Error


def main():
    print("=" * 50)
    print("  Dog Breed Identification — Grant Admin Role")
    print("=" * 50)

    username = input("\nEnter the username to grant admin: ").strip()
    if not username:
        print("[!] No username entered. Exiting.")
        sys.exit(1)

    conn = get_db_connection()
    if conn is None:
        print("[!] Could not connect to the database. Check your .env credentials.")
        sys.exit(1)

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, email, is_admin FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            print(f"[!] User '{username}' not found in the database.")
            print("    Make sure the user has signed up via the website first.")
            sys.exit(1)

        if user['is_admin']:
            print(f"[✓] User '{username}' (ID: {user['user_id']}) is already an admin.")
            sys.exit(0)

        # Grant admin
        ok = set_user_admin(user['user_id'], is_admin=True)
        if ok:
            print(f"\n[✓] SUCCESS — '{username}' (ID: {user['user_id']}) has been granted admin privileges.")
            print("    They must log out and log back in for the change to take effect.")
        else:
            print(f"[!] Failed to update admin status for '{username}'. Check database errors above.")

    except Error as e:
        print(f"[!] Database error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
