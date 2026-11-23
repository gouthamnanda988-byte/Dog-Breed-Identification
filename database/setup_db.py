"""
database/setup_db.py
====================
Standalone setup and test script for the MySQL database.

Usage:
    python database/setup_db.py
"""

import sys
import os

# Add parent directory to path so imports work smoothly
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config
from database.db import init_db, get_db_connection

print("=" * 60)
print("  DOG BREED IDENTIFICATION - MySQL Database Setup")
print("=" * 60)
print(f"  Host     : {config.DB_HOST}")
print(f"  Port     : {config.DB_PORT}")
print(f"  User     : {config.DB_USER}")
print(f"  Database : {config.DB_NAME}")
print("=" * 60)

print("\n[*] Initializing database and tables from database_setup.sql ...")
success = init_db()

if success:
    print("\n[OK] Setup complete! All 4 tables are ready:")
    print("     - users")
    print("     - prediction_history")
    print("     - favorite_breeds")
    print("     - feedback")
else:
    print("\n[!] Setup did not complete.")
    print("    Please ensure:")
    print("    1. Your MySQL server (e.g. MySQL80) is running.")
    print("    2. You created a .env file with your correct DB_PASSWORD.")
    print("       (See .env.example for guidance)")
