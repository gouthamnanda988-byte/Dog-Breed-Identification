"""
Database package for Dog Breed Identification
"""
from database.db import (
    get_db_connection,
    test_db_connection,
    init_db,
    save_prediction,
    get_prediction_history,
    get_prediction_by_id,
    delete_prediction,
    clear_all_history,
    create_user,
    get_user_by_username,
    add_favorite_breed,
    get_user_favorites,
    save_feedback
)
