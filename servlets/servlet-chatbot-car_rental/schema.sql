-- Create car_rental database if not exists
CREATE DATABASE IF NOT EXISTS car_rental;
USE car_rental;

-- Create cars table
CREATE TABLE IF NOT EXISTS cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    color VARCHAR(30),
    price_per_day DECIMAL(10,2) NOT NULL,
    available BOOLEAN DEFAULT true
);

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create rentals table
CREATE TABLE IF NOT EXISTS rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT NOT NULL,
    customer_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status ENUM('reserved', 'active', 'completed', 'cancelled') DEFAULT 'reserved',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES cars(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Insert sample car data
INSERT INTO cars (make, model, year, color, price_per_day) VALUES
('Toyota', 'Corolla', 2022, 'Silver', 45.00),
('Honda', 'Civic', 2021, 'Blue', 42.00),
('Ford', 'Mustang', 2023, 'Red', 85.00),
('Volkswagen', 'Golf', 2022, 'White', 48.00),
('BMW', '3 Series', 2021, 'Black', 95.00);