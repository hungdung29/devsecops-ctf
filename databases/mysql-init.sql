-- MySQL initialization script for injection challenges
CREATE DATABASE IF NOT EXISTS injection_db;
USE injection_db;

-- Users table with vulnerable data
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2),
    description TEXT,
    category VARCHAR(50)
);

-- Secret flags table
CREATE TABLE secret_flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag_name VARCHAR(50),
    flag_value VARCHAR(255),
    challenge_type VARCHAR(50)
);

-- Insert sample data
INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@vulnerable.com', 'admin'),
('user1', 'password123', 'user1@test.com', 'user'),
('john_doe', 'qwerty', 'john@example.com', 'user'),
('alice', 'alice2025', 'alice@company.com', 'user'),
('bob', 'bob_pass', 'bob@test.org', 'moderator');

INSERT INTO products (name, price, description, category) VALUES
('Laptop', 999.99, 'High-performance laptop', 'Electronics'),
('Mouse', 29.99, 'Wireless mouse', 'Electronics'),
('Keyboard', 79.99, 'Mechanical keyboard', 'Electronics'),
('Monitor', 299.99, '4K monitor', 'Electronics'),
('Chair', 199.99, 'Ergonomic office chair', 'Furniture');

INSERT INTO secret_flags (flag_name, flag_value, challenge_type) VALUES
('sql_injection', 'CTF{sql_1nj3ct10n_m4st3r_2025}', 'A03');

-- Create a vulnerable stored procedure
DELIMITER //
CREATE PROCEDURE GetUserInfo(IN user_id INT)
BEGIN
    SET @sql = CONCAT('SELECT * FROM users WHERE id = ', user_id);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Grant permissions
GRANT SELECT, INSERT, UPDATE ON injection_db.* TO 'ctf_user'@'%'; 