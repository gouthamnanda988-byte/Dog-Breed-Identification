-- ==============================================================
-- Database Setup Script: Dog Breed Identification
-- B.Tech Data Science Project
-- ==============================================================

-- 1. Create the database
CREATE DATABASE IF NOT EXISTS dog_breed_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE dog_breed_db;

-- ==============================================================
-- 2. Table: users
-- Stores registered users of the platform
-- ==============================================================
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ==============================================================
-- 3. Table: prediction_history
-- Stores real predictions made by the deep learning model
-- ==============================================================
CREATE TABLE IF NOT EXISTS prediction_history (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    image_path VARCHAR(255) NOT NULL,
    predicted_breed VARCHAR(100) NOT NULL,
    confidence FLOAT NOT NULL,
    top3_results TEXT NULL,
    model_version VARCHAR(50) DEFAULT 'MobileNetV2-v1',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_history_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ==============================================================
-- 4. Table: favorite_breeds
-- Allows users to bookmark their favorite dog breeds
-- ==============================================================
CREATE TABLE IF NOT EXISTS favorite_breeds (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    breed_name VARCHAR(100) NOT NULL,
    CONSTRAINT fk_fav_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    UNIQUE KEY uq_user_breed (user_id, breed_name)
) ENGINE=InnoDB;

-- ==============================================================
-- 5. Table: feedback
-- Collects user reviews and ratings (1 to 5 stars)
-- ==============================================================
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    message TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_feedback_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;
