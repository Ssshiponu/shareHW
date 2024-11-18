-- Create database
CREATE DATABASE IF NOT EXISTS sharehw_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user and grant privileges
CREATE USER IF NOT EXISTS 'sharehw_user'@'localhost' IDENTIFIED BY 'sharehw_password';
GRANT ALL PRIVILEGES ON sharehw_db.* TO 'sharehw_user'@'localhost';
FLUSH PRIVILEGES;
