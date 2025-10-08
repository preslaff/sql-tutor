-- E-commerce Sample Database Schema
-- Interactive SQL Tutorial System

-- ============================================
-- Table Definitions
-- ============================================

-- Customers Table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    join_date DATE NOT NULL,
    country VARCHAR(50)
);

-- Categories Table
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    description TEXT
);

-- Products Table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category_id INTEGER,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Orders Table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order Items Table
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Reviews Table
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- Sample Data - Customers
-- ============================================

INSERT INTO customers (customer_id, name, email, join_date, country) VALUES
(1, 'Alice Johnson', 'alice@email.com', '2023-01-15', 'USA'),
(2, 'Bob Smith', 'bob@email.com', '2023-03-22', 'Canada'),
(3, 'Carol White', 'carol@email.com', '2023-06-10', 'UK'),
(4, 'David Brown', 'david@email.com', '2023-07-05', 'USA'),
(5, 'Emma Davis', 'emma@email.com', '2023-08-18', 'Australia'),
(6, 'Frank Miller', 'frank@email.com', '2023-09-30', 'Canada'),
(7, 'Grace Lee', 'grace@email.com', '2023-10-12', 'USA'),
(8, 'Henry Wilson', 'henry@email.com', '2023-11-25', 'UK'),
(9, 'Iris Martinez', 'iris@email.com', '2024-01-08', 'Spain'),
(10, 'Jack Taylor', 'jack@email.com', '2024-02-14', 'USA');

-- ============================================
-- Sample Data - Categories
-- ============================================

INSERT INTO categories (category_id, category_name, description) VALUES
(1, 'Electronics', 'Electronic devices and accessories'),
(2, 'Books', 'Physical and digital books'),
(3, 'Clothing', 'Apparel and fashion items'),
(4, 'Home & Garden', 'Home improvement and gardening supplies'),
(5, 'Sports', 'Sports equipment and fitness gear'),
(6, 'Toys', 'Toys and games for all ages');

-- ============================================
-- Sample Data - Products
-- ============================================

INSERT INTO products (product_id, product_name, category_id, price, stock_quantity) VALUES
-- Electronics
(1, 'Wireless Mouse', 1, 29.99, 150),
(2, 'USB-C Cable', 1, 12.99, 300),
(3, 'Bluetooth Headphones', 1, 79.99, 85),
(4, 'Laptop Stand', 1, 45.50, 120),
(5, 'Webcam HD', 1, 89.99, 60),
(6, 'Mechanical Keyboard', 1, 129.99, 45),
(7, 'External SSD 1TB', 1, 149.99, 75),
(8, 'HDMI Cable', 1, 15.99, 200),

-- Books
(9, 'SQL Mastery Guide', 2, 39.99, 200),
(10, 'Python for Beginners', 2, 34.99, 180),
(11, 'Web Development 101', 2, 44.99, 150),
(12, 'Data Science Handbook', 2, 49.99, 90),
(13, 'Clean Code', 2, 42.99, 110),
(14, 'Design Patterns', 2, 54.99, 85),

-- Clothing
(15, 'Cotton T-Shirt', 3, 19.99, 500),
(16, 'Denim Jeans', 3, 59.99, 200),
(17, 'Running Shoes', 3, 89.99, 150),
(18, 'Winter Jacket', 3, 129.99, 80),
(19, 'Baseball Cap', 3, 24.99, 300),
(20, 'Wool Sweater', 3, 69.99, 120),

-- Home & Garden
(21, 'Plant Pot Set', 4, 29.99, 180),
(22, 'LED Desk Lamp', 4, 39.99, 140),
(23, 'Kitchen Knife Set', 4, 79.99, 95),
(24, 'Throw Pillow', 4, 19.99, 250),
(25, 'Garden Tools Set', 4, 54.99, 70),

-- Sports
(26, 'Yoga Mat', 5, 34.99, 200),
(27, 'Dumbbells 20lb', 5, 49.99, 100),
(28, 'Tennis Racket', 5, 119.99, 55),
(29, 'Basketball', 5, 29.99, 150),
(30, 'Resistance Bands', 5, 24.99, 180),

-- Toys
(31, 'Building Blocks Set', 6, 39.99, 160),
(32, 'Puzzle 1000 Pieces', 6, 24.99, 200),
(33, 'Remote Control Car', 6, 59.99, 90),
(34, 'Board Game Classic', 6, 34.99, 130),
(35, 'Action Figure', 6, 19.99, 220);

-- ============================================
-- Sample Data - Orders
-- ============================================

INSERT INTO orders (order_id, customer_id, order_date, total_amount, status) VALUES
(1, 1, '2024-01-10', 119.98, 'completed'),
(2, 2, '2024-01-15', 89.99, 'completed'),
(3, 1, '2024-01-20', 229.97, 'completed'),
(4, 3, '2024-01-25', 59.99, 'completed'),
(5, 4, '2024-02-01', 149.99, 'completed'),
(6, 2, '2024-02-05', 79.99, 'shipped'),
(7, 5, '2024-02-10', 299.96, 'completed'),
(8, 6, '2024-02-14', 44.99, 'completed'),
(9, 1, '2024-02-18', 189.98, 'completed'),
(10, 7, '2024-02-22', 129.99, 'shipped'),
(11, 3, '2024-02-25', 94.98, 'completed'),
(12, 8, '2024-03-01', 169.98, 'processing'),
(13, 4, '2024-03-05', 249.97, 'completed'),
(14, 9, '2024-03-08', 119.98, 'shipped'),
(15, 5, '2024-03-12', 79.99, 'completed'),
(16, 10, '2024-03-15', 199.98, 'processing'),
(17, 2, '2024-03-18', 54.99, 'completed'),
(18, 6, '2024-03-20', 134.98, 'completed'),
(19, 7, '2024-03-22', 89.99, 'pending'),
(20, 3, '2024-03-25', 179.98, 'completed');

-- ============================================
-- Sample Data - Order Items
-- ============================================

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, price_at_purchase) VALUES
-- Order 1 (Alice)
(1, 1, 1, 2, 29.99),
(2, 1, 2, 5, 12.99),

-- Order 2 (Bob)
(3, 2, 3, 1, 89.99),

-- Order 3 (Alice)
(4, 3, 6, 1, 129.99),
(5, 3, 9, 2, 39.99),
(6, 3, 15, 1, 19.99),

-- Order 4 (Carol)
(7, 4, 16, 1, 59.99),

-- Order 5 (David)
(8, 5, 7, 1, 149.99),

-- Order 6 (Bob)
(9, 6, 26, 2, 39.99),

-- Order 7 (Emma)
(10, 7, 17, 2, 89.99),
(11, 7, 27, 2, 59.99),

-- Order 8 (Frank)
(12, 8, 11, 1, 44.99),

-- Order 9 (Alice)
(13, 9, 4, 2, 45.50),
(14, 9, 5, 1, 89.99),

-- Order 10 (Grace)
(15, 10, 18, 1, 129.99),

-- Order 11 (Carol)
(16, 11, 19, 1, 24.99),
(17, 11, 20, 1, 69.99),

-- Order 12 (Henry)
(18, 12, 3, 2, 84.99),

-- Order 13 (David)
(19, 13, 23, 1, 79.99),
(20, 13, 28, 1, 119.99),
(21, 13, 26, 1, 49.99),

-- Order 14 (Iris)
(22, 14, 31, 2, 39.99),
(23, 14, 32, 1, 24.99),

-- Order 15 (Emma)
(24, 15, 3, 1, 79.99),

-- Order 16 (Jack)
(25, 16, 6, 1, 129.99),
(26, 16, 20, 1, 69.99),

-- Order 17 (Bob)
(27, 17, 25, 1, 54.99),

-- Order 18 (Frank)
(28, 18, 13, 1, 42.99),
(29, 18, 12, 1, 49.99),
(30, 18, 10, 1, 34.99),

-- Order 19 (Grace)
(31, 19, 5, 1, 89.99),

-- Order 20 (Carol)
(32, 20, 27, 2, 49.99),
(33, 20, 26, 2, 34.99);

-- ============================================
-- Sample Data - Reviews
-- ============================================

INSERT INTO reviews (review_id, product_id, customer_id, rating, review_text, review_date) VALUES
(1, 1, 1, 5, 'Excellent wireless mouse! Very responsive and comfortable.', '2024-01-15'),
(2, 3, 2, 4, 'Good headphones for the price. Sound quality is decent.', '2024-01-20'),
(3, 6, 1, 5, 'Best mechanical keyboard I have ever used!', '2024-01-25'),
(4, 16, 3, 4, 'Good quality jeans, fit well.', '2024-01-28'),
(5, 7, 4, 5, 'Fast SSD, works great!', '2024-02-05'),
(6, 26, 2, 5, 'Perfect yoga mat, good grip and comfortable.', '2024-02-08'),
(7, 17, 5, 4, 'Comfortable running shoes, great for daily exercise.', '2024-02-15'),
(8, 11, 6, 5, 'Very comprehensive book on web development!', '2024-02-18'),
(9, 4, 1, 5, 'Sturdy laptop stand, improved my posture significantly.', '2024-02-22'),
(10, 5, 1, 4, 'Good webcam for video calls.', '2024-02-22'),
(11, 18, 7, 5, 'Warm and stylish winter jacket!', '2024-02-25'),
(12, 19, 3, 4, 'Nice baseball cap, good quality material.', '2024-02-28'),
(13, 20, 3, 5, 'Cozy wool sweater, perfect for winter.', '2024-02-28'),
(14, 3, 8, 3, 'Decent headphones but could be better.', '2024-03-05'),
(15, 23, 4, 5, 'Sharp knives, great for cooking!', '2024-03-08'),
(16, 28, 4, 4, 'Good tennis racket for beginners.', '2024-03-08'),
(17, 31, 9, 5, 'Kids love these building blocks!', '2024-03-12'),
(18, 32, 9, 4, 'Challenging puzzle, good quality pieces.', '2024-03-12'),
(19, 3, 5, 5, 'Amazing sound quality and battery life!', '2024-03-15'),
(20, 6, 10, 5, 'Perfect mechanical keyboard for gaming and typing.', '2024-03-18'),
(21, 20, 10, 4, 'Nice sweater but a bit pricey.', '2024-03-18'),
(22, 25, 2, 4, 'Good set of garden tools, everything you need.', '2024-03-20'),
(23, 13, 6, 5, 'Must-read book for any programmer!', '2024-03-23'),
(24, 12, 6, 5, 'Comprehensive guide to data science.', '2024-03-23'),
(25, 10, 6, 4, 'Great introduction to Python programming.', '2024-03-23'),
(26, 5, 7, 4, 'Clear video quality, good for remote work.', '2024-03-25'),
(27, 27, 3, 5, 'Perfect weight for home workouts!', '2024-03-28'),
(28, 26, 3, 5, 'Excellent yoga mat, highly recommend!', '2024-03-28'),
(29, 9, 1, 5, 'The best SQL book I have read!', '2024-03-30'),
(30, 15, 1, 4, 'Comfortable t-shirt, good fabric.', '2024-03-30');

-- ============================================
-- Create Indexes for Better Performance
-- ============================================

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_reviews_product ON reviews(product_id);
CREATE INDEX idx_reviews_customer ON reviews(customer_id);

-- ============================================
-- Useful Views for Common Queries
-- ============================================

-- View: Product details with category names
CREATE VIEW product_details AS
SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    p.price,
    p.stock_quantity
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id;

-- View: Customer order summary
CREATE VIEW customer_order_summary AS
SELECT
    c.customer_id,
    c.name,
    c.email,
    COUNT(o.order_id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email;

-- View: Product ratings
CREATE VIEW product_ratings AS
SELECT
    p.product_id,
    p.product_name,
    COUNT(r.review_id) as review_count,
    ROUND(AVG(r.rating), 2) as average_rating
FROM products p
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, p.product_name;

-- ============================================
-- End of Sample Database
-- ============================================
