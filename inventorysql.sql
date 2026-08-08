CREATE DATABASE if not exists inventory;
SHOW DATABASES;
USE inventory;
SHOW TABLES;
SELECT*FROM items;

-- =========================
-- ITEMS TABLE
-- =========================

CREATE TABLE if not exists items (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    unit_price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL
);

-- =========================
-- CUSTOMERS TABLE
-- =========================

CREATE TABLE if not exists customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    contact VARCHAR(15)
);

-- =========================
-- SUPPLIERS TABLE
-- =========================

CREATE TABLE if not exists suppliers (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact VARCHAR(15)
);

-- =========================
-- SALES TRANSACTION TABLE
-- =========================

CREATE TABLE if not exists sales_transaction (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME,
    customer_id INT,
    total_amount DECIMAL(10,2),

    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
);

-- =========================
-- SALE DETAILS TABLE
-- =========================

CREATE TABLE if not exists sale_details (
    sale_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),

    FOREIGN KEY (sale_id)
    REFERENCES sales_transaction(sale_id),

    FOREIGN KEY (product_id)
    REFERENCES items(product_id)
);

-- =========================
-- PURCHASE TRANSACTION TABLE
-- =========================

CREATE TABLE if not exists purchase_transaction (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME,
    supplier_id INT,
    total_amount DECIMAL(10,2),

    FOREIGN KEY (supplier_id)
    REFERENCES suppliers(supplier_id)
);

-- =========================
-- PURCHASE DETAILS TABLE
-- =========================

CREATE TABLE if not exists purchase_details (
    purchase_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),

    FOREIGN KEY (purchase_id)
    REFERENCES purchase_transaction(purchase_id),

    FOREIGN KEY (product_id)
    REFERENCES items(product_id)
);