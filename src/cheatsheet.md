# SQL Cheatsheet - Quick Reference Guide

## Basic Queries

### SELECT Statement
```sql
-- Select all columns
SELECT * FROM table_name;

-- Select specific columns
SELECT column1, column2 FROM table_name;

-- Select with alias
SELECT column1 AS alias_name FROM table_name;
```

### DISTINCT
```sql
-- Get unique values
SELECT DISTINCT column_name FROM table_name;

-- Multiple columns (unique combinations)
SELECT DISTINCT column1, column2 FROM table_name;
```

### WHERE Clause
```sql
-- Basic filtering
SELECT * FROM table_name WHERE condition;

-- Example
SELECT * FROM customers WHERE country = 'USA';
```

### Comparison Operators
```sql
=   -- Equal to
<>  -- Not equal to (also !=)
<   -- Less than
>   -- Greater than
<=  -- Less than or equal to
>=  -- Greater than or equal to

-- Examples
SELECT * FROM products WHERE price > 100;
SELECT * FROM orders WHERE status <> 'cancelled';
```

### Logical Operators
```sql
-- AND: All conditions must be true
SELECT * FROM products WHERE price > 50 AND stock_quantity > 0;

-- OR: At least one condition must be true
SELECT * FROM customers WHERE country = 'USA' OR country = 'Canada';

-- NOT: Negates a condition
SELECT * FROM products WHERE NOT category_id = 1;
```

### Pattern Matching (LIKE)
```sql
-- Wildcards: % (any characters), _ (single character)
SELECT * FROM customers WHERE name LIKE 'A%';      -- Starts with A
SELECT * FROM customers WHERE name LIKE '%son';    -- Ends with son
SELECT * FROM customers WHERE name LIKE '%oh%';    -- Contains oh
SELECT * FROM customers WHERE name LIKE 'A_ice';   -- A, any char, ice
```

### IN Operator
```sql
-- Match any value in a list
SELECT * FROM customers WHERE country IN ('USA', 'Canada', 'UK');

-- NOT IN
SELECT * FROM products WHERE category_id NOT IN (1, 2, 3);
```

### BETWEEN Operator
```sql
-- Range of values (inclusive)
SELECT * FROM products WHERE price BETWEEN 50 AND 100;

-- With dates
SELECT * FROM orders WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';
```

### NULL Handling
```sql
-- Check for NULL values
SELECT * FROM customers WHERE email IS NULL;

-- Check for non-NULL values
SELECT * FROM customers WHERE email IS NOT NULL;
```

### ORDER BY
```sql
-- Ascending order (default)
SELECT * FROM products ORDER BY price;
SELECT * FROM products ORDER BY price ASC;

-- Descending order
SELECT * FROM products ORDER BY price DESC;

-- Multiple columns
SELECT * FROM products ORDER BY category_id ASC, price DESC;
```

### LIMIT
```sql
-- Limit number of results
SELECT * FROM products ORDER BY price DESC LIMIT 10;

-- With OFFSET (skip first N rows)
SELECT * FROM products ORDER BY price DESC LIMIT 10 OFFSET 20;
```

---

## Aggregate Functions

### COUNT
```sql
-- Count all rows
SELECT COUNT(*) FROM customers;

-- Count non-NULL values
SELECT COUNT(email) FROM customers;

-- Count distinct values
SELECT COUNT(DISTINCT country) FROM customers;
```

### SUM
```sql
-- Total of a numeric column
SELECT SUM(total_amount) FROM orders;

-- With condition
SELECT SUM(total_amount) FROM orders WHERE status = 'completed';
```

### AVG
```sql
-- Average value
SELECT AVG(price) FROM products;

-- Rounded average
SELECT ROUND(AVG(price), 2) FROM products;
```

### MIN and MAX
```sql
-- Minimum value
SELECT MIN(price) FROM products;

-- Maximum value
SELECT MAX(order_date) FROM orders;
```

### GROUP BY
```sql
-- Group results by one or more columns
SELECT country, COUNT(*) as customer_count
FROM customers
GROUP BY country;

-- Multiple columns
SELECT category_id, status, COUNT(*) as count
FROM products
GROUP BY category_id, status;

-- With aggregate functions
SELECT customer_id, SUM(total_amount) as total_spent
FROM orders
GROUP BY customer_id;
```

### HAVING
```sql
-- Filter groups (use HAVING, not WHERE, for aggregate conditions)
SELECT country, COUNT(*) as customer_count
FROM customers
GROUP BY country
HAVING COUNT(*) > 5;

-- Multiple conditions
SELECT category_id, AVG(price) as avg_price
FROM products
GROUP BY category_id
HAVING AVG(price) > 100 AND COUNT(*) > 10;
```

---

## Joins

### INNER JOIN
```sql
-- Returns only matching rows from both tables
SELECT customers.name, orders.order_id, orders.total_amount
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id;

-- Alternative syntax
SELECT c.name, o.order_id, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

### LEFT JOIN (LEFT OUTER JOIN)
```sql
-- Returns all rows from left table, matching rows from right table
-- NULL for non-matching right table rows
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

### RIGHT JOIN (RIGHT OUTER JOIN)
```sql
-- Returns all rows from right table, matching rows from left table
-- NULL for non-matching left table rows
SELECT c.name, o.order_id
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;
```

### FULL OUTER JOIN
```sql
-- Returns all rows from both tables
-- NULL where there's no match
SELECT c.name, o.order_id
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```

### CROSS JOIN
```sql
-- Cartesian product: all possible combinations
SELECT c.name, p.product_name
FROM customers c
CROSS JOIN products p;
```

### Self Join
```sql
-- Join table to itself
SELECT e1.name as employee, e2.name as manager
FROM employees e1
JOIN employees e2 ON e1.manager_id = e2.employee_id;
```

### Multiple Joins
```sql
-- Chain multiple joins
SELECT c.name, o.order_id, p.product_name, oi.quantity
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
```

---

## Subqueries

### Subquery in WHERE
```sql
-- Find products more expensive than average
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- IN subquery
SELECT name
FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders WHERE total_amount > 1000);
```

### Subquery in FROM
```sql
-- Use subquery as a table
SELECT avg_prices.category_id, avg_prices.avg_price
FROM (
    SELECT category_id, AVG(price) as avg_price
    FROM products
    GROUP BY category_id
) as avg_prices
WHERE avg_prices.avg_price > 100;
```

### Subquery in SELECT
```sql
-- Scalar subquery in SELECT list
SELECT
    name,
    (SELECT COUNT(*) FROM orders WHERE orders.customer_id = customers.customer_id) as order_count
FROM customers;
```

### Correlated Subquery
```sql
-- Subquery references outer query
SELECT p1.product_name, p1.price
FROM products p1
WHERE p1.price > (
    SELECT AVG(p2.price)
    FROM products p2
    WHERE p2.category_id = p1.category_id
);
```

### EXISTS
```sql
-- Check if subquery returns any rows
SELECT name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

### NOT EXISTS
```sql
-- Find customers with no orders
SELECT name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

---

## Advanced Topics

### UNION
```sql
-- Combine results (removes duplicates)
SELECT customer_id FROM orders WHERE order_date > '2023-01-01'
UNION
SELECT customer_id FROM reviews WHERE review_date > '2023-01-01';
```

### UNION ALL
```sql
-- Combine results (keeps duplicates)
SELECT customer_id FROM orders
UNION ALL
SELECT customer_id FROM reviews;
```

### INTERSECT
```sql
-- Rows that appear in both queries
SELECT customer_id FROM orders
INTERSECT
SELECT customer_id FROM reviews;
```

### EXCEPT (or MINUS)
```sql
-- Rows in first query but not in second
SELECT customer_id FROM customers
EXCEPT
SELECT customer_id FROM orders;
```

### Common Table Expressions (CTEs)
```sql
-- WITH clause for readable subqueries
WITH high_value_customers AS (
    SELECT customer_id, SUM(total_amount) as total_spent
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total_amount) > 5000
)
SELECT c.name, hvc.total_spent
FROM customers c
JOIN high_value_customers hvc ON c.customer_id = hvc.customer_id;

-- Multiple CTEs
WITH
    monthly_sales AS (
        SELECT DATE_TRUNC('month', order_date) as month, SUM(total_amount) as sales
        FROM orders
        GROUP BY DATE_TRUNC('month', order_date)
    ),
    avg_monthly AS (
        SELECT AVG(sales) as avg_sales FROM monthly_sales
    )
SELECT month, sales
FROM monthly_sales, avg_monthly
WHERE sales > avg_sales;
```

### Window Functions

#### ROW_NUMBER
```sql
-- Assign unique number to each row
SELECT
    product_name,
    price,
    ROW_NUMBER() OVER (ORDER BY price DESC) as row_num
FROM products;
```

#### RANK and DENSE_RANK
```sql
-- RANK: same values get same rank, gaps in sequence
SELECT
    product_name,
    price,
    RANK() OVER (ORDER BY price DESC) as rank
FROM products;

-- DENSE_RANK: no gaps in ranking
SELECT
    product_name,
    price,
    DENSE_RANK() OVER (ORDER BY price DESC) as dense_rank
FROM products;
```

#### PARTITION BY
```sql
-- Window function per group
SELECT
    category_id,
    product_name,
    price,
    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as rank_in_category
FROM products;

-- Running total per partition
SELECT
    customer_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total
FROM orders;
```

#### Other Window Functions
```sql
-- LAG: previous row value
SELECT
    order_date,
    total_amount,
    LAG(total_amount, 1) OVER (ORDER BY order_date) as previous_amount
FROM orders;

-- LEAD: next row value
SELECT
    order_date,
    total_amount,
    LEAD(total_amount, 1) OVER (ORDER BY order_date) as next_amount
FROM orders;

-- FIRST_VALUE and LAST_VALUE
SELECT
    product_name,
    price,
    FIRST_VALUE(price) OVER (ORDER BY price) as min_price,
    LAST_VALUE(price) OVER (ORDER BY price ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as max_price
FROM products;
```

### CASE WHEN
```sql
-- Simple CASE
SELECT
    product_name,
    price,
    CASE
        WHEN price < 50 THEN 'Budget'
        WHEN price < 200 THEN 'Mid-range'
        ELSE 'Premium'
    END as price_category
FROM products;

-- CASE in aggregation
SELECT
    SUM(CASE WHEN status = 'completed' THEN total_amount ELSE 0 END) as completed_sales,
    SUM(CASE WHEN status = 'pending' THEN total_amount ELSE 0 END) as pending_sales
FROM orders;
```

---

## Data Modification

### INSERT INTO
```sql
-- Insert single row
INSERT INTO customers (customer_id, name, email, join_date, country)
VALUES (4, 'David Brown', 'david@email.com', '2024-01-15', 'USA');

-- Insert multiple rows
INSERT INTO customers (customer_id, name, email, join_date, country)
VALUES
    (5, 'Eve Wilson', 'eve@email.com', '2024-02-01', 'Canada'),
    (6, 'Frank Miller', 'frank@email.com', '2024-02-15', 'UK');

-- Insert from SELECT
INSERT INTO archived_orders (order_id, customer_id, order_date, total_amount)
SELECT order_id, customer_id, order_date, total_amount
FROM orders
WHERE order_date < '2022-01-01';
```

### UPDATE
```sql
-- Update single column
UPDATE products
SET price = 99.99
WHERE product_id = 1;

-- Update multiple columns
UPDATE customers
SET email = 'newemail@example.com', country = 'USA'
WHERE customer_id = 2;

-- Update with calculation
UPDATE products
SET price = price * 1.1
WHERE category_id = 1;

-- Update with subquery
UPDATE products
SET stock_quantity = 0
WHERE product_id IN (SELECT product_id FROM discontinued_products);
```

### DELETE
```sql
-- Delete specific rows
DELETE FROM orders
WHERE status = 'cancelled';

-- Delete with subquery
DELETE FROM reviews
WHERE customer_id IN (SELECT customer_id FROM banned_customers);

-- Delete all rows (keep table structure)
DELETE FROM temp_table;
```

### TRUNCATE
```sql
-- Fast delete of all rows (resets auto-increment)
TRUNCATE TABLE temp_table;
```

---

## Schema Operations

### CREATE TABLE
```sql
-- Basic table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE,
    salary DECIMAL(10, 2)
);

-- With constraints
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10, 2) CHECK (total_amount >= 0),
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

### Constraints

#### PRIMARY KEY
```sql
-- Single column
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(200)
);

-- Composite primary key
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

#### FOREIGN KEY
```sql
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- With actions
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

#### UNIQUE
```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    email VARCHAR(100) UNIQUE
);

-- Multiple columns
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    sku VARCHAR(50),
    supplier_id INTEGER,
    UNIQUE (sku, supplier_id)
);
```

#### NOT NULL
```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);
```

#### CHECK
```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    price DECIMAL(10, 2) CHECK (price > 0),
    stock_quantity INTEGER CHECK (stock_quantity >= 0)
);

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5)
);
```

#### DEFAULT
```sql
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'pending',
    quantity INTEGER DEFAULT 1
);
```

### ALTER TABLE
```sql
-- Add column
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);

-- Drop column
ALTER TABLE customers DROP COLUMN phone;

-- Rename column
ALTER TABLE customers RENAME COLUMN name TO full_name;

-- Rename table
ALTER TABLE customers RENAME TO clients;

-- Add constraint
ALTER TABLE products ADD CONSTRAINT check_price CHECK (price > 0);
```

### DROP TABLE
```sql
-- Delete table and all data
DROP TABLE temp_table;

-- Only if exists
DROP TABLE IF EXISTS temp_table;

-- With cascade (also drops dependent objects)
DROP TABLE orders CASCADE;
```

---

## Common Patterns and Tips

### Find Duplicates
```sql
SELECT email, COUNT(*) as count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```

### Remove Duplicates (keeping one)
```sql
DELETE FROM customers
WHERE customer_id NOT IN (
    SELECT MIN(customer_id)
    FROM customers
    GROUP BY email
);
```

### Pagination
```sql
-- Page 1 (10 items per page)
SELECT * FROM products ORDER BY product_id LIMIT 10 OFFSET 0;

-- Page 2
SELECT * FROM products ORDER BY product_id LIMIT 10 OFFSET 10;

-- Page N
SELECT * FROM products ORDER BY product_id LIMIT 10 OFFSET ((N-1) * 10);
```

### Top N per Group
```sql
-- Top 3 products by price in each category
WITH ranked_products AS (
    SELECT
        product_name,
        category_id,
        price,
        ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as rank
    FROM products
)
SELECT product_name, category_id, price
FROM ranked_products
WHERE rank <= 3;
```

### Running Total
```sql
SELECT
    order_date,
    total_amount,
    SUM(total_amount) OVER (ORDER BY order_date) as running_total
FROM orders
ORDER BY order_date;
```

### Pivot Data
```sql
-- Convert rows to columns
SELECT
    customer_id,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 1 THEN total_amount ELSE 0 END) as jan_sales,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 2 THEN total_amount ELSE 0 END) as feb_sales,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 3 THEN total_amount ELSE 0 END) as mar_sales
FROM orders
GROUP BY customer_id;
```

---

## Performance Tips

1. **Use indexes** on columns frequently used in WHERE, JOIN, and ORDER BY
2. **Avoid SELECT *** - specify only needed columns
3. **Use LIMIT** when you don't need all results
4. **Use EXISTS instead of IN** for correlated queries
5. **Avoid functions on indexed columns** in WHERE clauses
6. **Use UNION ALL instead of UNION** when duplicates don't matter
7. **Analyze query plans** to identify bottlenecks

---

## Common Functions

### String Functions
```sql
UPPER('text')           -- Convert to uppercase
LOWER('text')           -- Convert to lowercase
LENGTH('text')          -- String length
CONCAT(str1, str2)      -- Concatenate strings
SUBSTRING(str, pos, len) -- Extract substring
TRIM('  text  ')        -- Remove leading/trailing spaces
REPLACE(str, find, replace) -- Replace text
```

### Date Functions
```sql
CURRENT_DATE            -- Current date
CURRENT_TIME            -- Current time
CURRENT_TIMESTAMP       -- Current date and time
DATE('2024-01-15')      -- Create date
EXTRACT(YEAR FROM date) -- Get year, month, day, etc.
DATE_ADD(date, INTERVAL 1 DAY) -- Add time interval
DATEDIFF(date1, date2)  -- Difference between dates
```

### Math Functions
```sql
ROUND(number, decimals) -- Round number
CEIL(number)            -- Round up
FLOOR(number)           -- Round down
ABS(number)             -- Absolute value
POWER(base, exponent)   -- Exponentiation
SQRT(number)            -- Square root
```

### Conditional Functions
```sql
COALESCE(val1, val2, ...) -- First non-NULL value
NULLIF(val1, val2)        -- NULL if equal, else val1
IFNULL(val, default)      -- Replace NULL with default
```

---

**Happy querying!** 🚀
