# 🎓 Interactive SQL Tutorial System

An **intelligent SQL learning platform** that provides hands-on practice with instant feedback powered by Claude AI. Master SQL through adaptive tutoring, progressive hints, and unlimited AI-generated exercises.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-Educational-orange)

---

## ✨ Key Features

### 🤖 **AI-Powered Adaptive Tutoring**
- **Semantic Similarity Analysis**: Uses vector embeddings to measure how close your answer is to the solution (0-100%)
- **Progressive Hints**: Get smarter hints based on your similarity score
  - 85%+ similar: "Almost there! Check small details"
  - 60-85%: "Right structure, review specific parts"
  - 40-60%: "Some elements correct, focus on SQL clauses"
  - <40%: "Different approach needed, try these concepts..."
- **Multiple Attempts**: Up to 3 tries per question with improving hints
- **Token Optimization**: AI calls only when needed (not for correct answers)

### 🎯 **Unlimited Practice**
- **36 Curated Exercises**: Across beginner, intermediate, and advanced levels
- **Exercise Completion Tracking**: Never repeat exercises you've already mastered
- **AI-Generated Exercises**: When you complete all exercises, the system automatically generates new unique challenges
- **Progress Monitoring**: See your completion rate at each level

### 📊 **Comprehensive Learning**
- **Database Preview**: View complete database structure at startup
- **Example Exercises**: See sample questions before diving in
- **Real-time Query Execution**: Practice against a real SQLite database
- **Result Comparison**: Side-by-side view of your results vs. expected results
- **Rich Sample Data**: E-commerce database with 6 tables and realistic data

### 📚 **Learning Resources**
- **Interactive Cheatsheet**: Complete SQL reference with examples
- **Concept Highlighting**: Each exercise shows which SQL concepts it covers
- **Built-in Hints**: Context-aware hints for each exercise

---

## 🏗️ Project Structure

```
sql-tutorial/
├── data/
│   ├── sample_database.sql       # E-commerce database schema + seed data
│   ├── sample_database.db        # SQLite database (auto-created)
│   └── queries.json              # 36 practice exercises
├── src/
│   ├── cheatsheet.md            # Comprehensive SQL reference
│   └── tutor.py                 # Main tutorial engine (AI-powered)
├── tests/
├── .env.example                 # Template for environment variables
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** (Download from [python.org](https://python.org))
- **Anthropic API Key** (Get from [console.anthropic.com](https://console.anthropic.com))
- **SQLite3** (Usually pre-installed)

### Installation

**1. Clone the repository**
```bash
git clone <repository-url>
cd sql-tutorial
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude AI SDK
- `sentence-transformers` - For semantic similarity
- `numpy` - Vector calculations
- `python-dotenv` - Environment variable management

**3. Configure API Key**

Copy the example environment file and add your API key:
```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your-actual-api-key-here
```

**4. Start Learning!**
```bash
python src/tutor.py
```

The database is already initialized and ready to use!

---

## 📖 How It Works

### 🎬 **Startup Flow**

When you launch the tutor:

1. **Database Structure Preview**
   ```
   ============================================================
   DATABASE STRUCTURE
   ============================================================

   📋 Table: CUSTOMERS
   ------------------------------------------------------------
     • customer_id: INTEGER (PRIMARY KEY, NOT NULL)
     • name: VARCHAR(100) (NOT NULL)
     • email: VARCHAR(100) (NOT NULL)
     • join_date: DATE (NOT NULL)
     • country: VARCHAR(50)

     Total rows: 10

   [... more tables ...]
   ```

2. **Example Exercises Preview**
   ```
   ============================================================
   EXAMPLE EXERCISES
   ============================================================

   🎯 BEGINNER Level Examples:
   ------------------------------------------------------------

     1. Select all customers from the USA
        Concepts: SELECT, WHERE
        Hint: Use WHERE clause to filter by country

   [... more examples ...]
   ```

3. **Choose Difficulty**: Beginner → Intermediate → Advanced

### 🎓 **Practice Session**

```
Question: Find all products with price less than $50
Concepts: SELECT, WHERE, comparison operators

Enter your SQL query (end with semicolon):
> SELECT * FROM products WHERE cost < 50;

❌ Not quite right. The query runs but produces different results.
📊 Similarity to solution: 87.3%

Your results:
(No rows returned)

Expected results:
product_id | product_name | category_id | price | stock_quantity
--------------------------------------------------------------
1 | Wireless Mouse | 1 | 29.99 | 150
2 | USB-C Cable | 1 | 12.99 | 300
[... more rows ...]

💡 Generating hint based on your attempt (Attempt 1/3)...

🔍 Hint: You're very close! You're using the right structure with SELECT
and WHERE, but check your column name carefully. The database uses
'price' not 'cost'.

Would you like to try again? (y/n/s to see solution): y

Attempt 2 (end with semicolon):
> SELECT * FROM products WHERE price < 50;

✅ Correct! Great job!
   (Solved in 2 attempts)
   Progress: 3/12 exercises completed at beginner level

Your results:
[correct results shown]
```

### 🎯 **Advanced Features in Action**

#### **Similarity-Based Hints**
- System calculates vector similarity between your query and solution
- Higher similarity (>80%) = More specific hints
- Lower similarity (<40%) = Broader conceptual guidance

#### **Multiple Attempts**
- 3 attempts per question
- Progressive hints get more detailed with each attempt
- Can request solution at any time

#### **Unlimited Practice**
```
🎉 Congratulations! You've completed all 12 beginner exercises!
🤖 Generating a new challenge for you...

✅ New exercise generated: Find customers who have ordered products
from at least 3 different categories

Question: Find customers who have ordered products from at least 3
different categories
Concepts: JOIN, GROUP BY, HAVING, DISTINCT
```

---

## 🗃️ Database Schema

The tutorial uses a realistic **e-commerce database** with 6 interconnected tables:

| Table | Description | Rows |
|-------|-------------|------|
| **customers** | Customer information (id, name, email, country) | 10 |
| **categories** | Product categories (Electronics, Books, etc.) | 6 |
| **products** | Product catalog (35 products with prices) | 35 |
| **orders** | Customer orders with status tracking | 20 |
| **order_items** | Line items in each order | 33 |
| **reviews** | Product reviews with ratings (1-5 stars) | 30 |

### Entity Relationships

```
customers (1) ──→ (N) orders (1) ──→ (N) order_items (N) ──→ (1) products (N) ──→ (1) categories
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
                           reviews (N) ──→ (1)
```

---

## 📚 Learning Path

### 🟢 **Beginner (12 exercises)**
Perfect for SQL beginners or refreshing fundamentals.

**Topics Covered:**
- `SELECT`, `FROM`, `WHERE` basics
- Filtering with `=`, `<`, `>`, `LIKE`, `IN`, `BETWEEN`
- Sorting with `ORDER BY` and limiting with `LIMIT`
- Basic aggregations: `COUNT()`, `SUM()`, `AVG()`
- Pattern matching with wildcards

**Example Exercises:**
- Select all customers from a specific country
- Find products under $50
- Count total products in database
- Get top 5 most expensive items

### 🟡 **Intermediate (12 exercises)**
Build on fundamentals with multi-table queries.

**Topics Covered:**
- `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`
- `GROUP BY` with aggregations
- `HAVING` clause for filtered groups
- Multiple table joins
- Subqueries in `WHERE` clause
- Date filtering

**Example Exercises:**
- Total orders per customer with names
- Average price per category
- Products never reviewed
- Top 3 customers by spending

### 🔴 **Advanced (12 exercises)**
Master complex analytical queries.

**Topics Covered:**
- Window functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`
- `PARTITION BY` for grouped analytics
- Common Table Expressions (CTEs) with `WITH`
- Correlated subqueries
- Self-joins
- Complex multi-table analytics

**Example Exercises:**
- Rank products by revenue within each category
- Calculate running totals per customer
- Find products ordered together frequently
- Monthly sales analysis with CTEs

---

## 💡 Key Capabilities

### 1️⃣ **Adaptive Tutoring System**

The system uses **semantic similarity** to understand not just IF you're wrong, but HOW WRONG you are:

```python
# Vector embedding similarity calculation
similarity = calculate_query_similarity(your_query, solution)
# Returns: 0.873 (87.3% similar)

# Generates context-aware hints
if similarity > 0.8:
    hint = "Almost perfect! Check column name: 'country' not 'location'"
elif similarity > 0.6:
    hint = "Right approach! Missing the GROUP BY clause"
else:
    hint = "Try focusing on JOIN syntax for multi-table queries"
```

### 2️⃣ **Exercise Generation**

Never run out of practice! When you complete all exercises at a level:

```python
# Automatically triggers
generate_new_exercise(level='beginner')

# LLM creates:
{
  "question": "Find the average rating for products in the Electronics category",
  "solution": "SELECT AVG(r.rating) FROM products p JOIN reviews r ON p.product_id = r.product_id JOIN categories c ON p.category_id = c.category_id WHERE c.category_name = 'Electronics';",
  "concepts": ["JOIN", "AVG", "WHERE", "multi-table"],
  "hint": "You'll need to join three tables: products, reviews, and categories"
}
```

### 3️⃣ **Progress Tracking**

```
Exercise Completion Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Beginner:     ████████████ 12/12 (100%) ✅
Intermediate: ████████░░░░  8/12 (67%)
Advanced:     ██░░░░░░░░░░  2/12 (17%)
```

### 4️⃣ **Token Optimization**

Smart API usage to save costs:

| Scenario | LLM Called? | Tokens Used |
|----------|-------------|-------------|
| Correct answer | ❌ No | ~0 |
| Wrong answer (hint) | ✅ Yes | ~300-500 |
| Request solution | ✅ Yes | ~500 |
| Generate exercise | ✅ Yes | ~500 |

**Average savings**: 50-70% reduction in API costs!

---

## 🎯 Usage Examples

### Basic Practice Session

```bash
$ python src/tutor.py

Loading semantic similarity model...
Model loaded successfully!

[Database structure shown]
[Example exercises shown]

Ready to start practicing?
Press Enter to continue or 'q' to quit:

Choose difficulty level:
1. Beginner
2. Intermediate
3. Advanced

Enter choice (1/2/3): 1

============================================================
SQL Practice Session - BEGINNER Level
============================================================

Question: Count how many customers are from Canada
Concepts: COUNT, WHERE

Enter your SQL query (end with semicolon):
> SELECT COUNT(*) FROM customers WHERE country = 'Canada';

✅ Correct! Great job!
   Progress: 1/12 exercises completed at beginner level

Your results:
COUNT(*)
--------
2

Try another question? (y/n): y
```

### Programmatic Usage

```python
from src.tutor import SQLTutor

# Initialize tutor
tutor = SQLTutor('data/sample_database.db', 'data/queries.json')

# Get exercise
exercise = tutor.get_query_by_level('beginner')
print(f"Question: {exercise['question']}")

# Check answer
user_query = "SELECT * FROM customers WHERE country = 'USA';"
similarity = tutor.calculate_query_similarity(user_query, exercise['solution'])
print(f"Similarity: {similarity*100:.1f}%")

# Get hint if needed
if similarity < 0.9:
    hint = tutor.get_progressive_hint(exercise, user_query, similarity, attempt=1)
    print(f"Hint: {hint}")

# Validate answer
is_correct = tutor.compare_results(user_query, exercise['solution'])
print(f"Correct: {is_correct}")

tutor.close()
```

---

## 🛠️ Customization

### Add Custom Exercises

Edit `data/queries.json`:

```json
{
  "beginner": [
    {
      "id": "b_custom1",
      "question": "Find all orders placed in March 2024",
      "solution": "SELECT * FROM orders WHERE order_date >= '2024-03-01' AND order_date < '2024-04-01';",
      "concepts": ["SELECT", "WHERE", "date filtering"],
      "hint": "Use date comparison with >= and <"
    }
  ]
}
```

### Modify Database Schema

Edit `data/sample_database.sql` to add tables, data, or create different scenarios:

```sql
-- Add a new table
CREATE TABLE suppliers (
    supplier_id INTEGER PRIMARY KEY,
    supplier_name VARCHAR(100),
    country VARCHAR(50)
);

-- Insert data
INSERT INTO suppliers VALUES (1, 'TechSupply Inc', 'USA');
```

Then recreate the database:
```bash
rm data/sample_database.db
python -c "import sqlite3; conn = sqlite3.connect('data/sample_database.db'); conn.executescript(open('data/sample_database.sql').read()); conn.close()"
```

### Adjust AI Prompts

Edit `src/tutor.py` to customize:

**Hint generation** (line ~121):
```python
prompt = f"""You are a friendly SQL tutor...
[customize tone, detail level, examples]
"""
```

**Exercise generation** (line ~91):
```python
prompt = f"""Create a {level} exercise that focuses on {specific_topic}...
"""
```

---

## 🔧 Troubleshooting

### Common Issues

**❌ `ModuleNotFoundError: No module named 'anthropic'`**
```bash
pip install -r requirements.txt
```

**❌ `ANTHROPIC_API_KEY not found`**
```bash
# Check .env file exists and contains:
ANTHROPIC_API_KEY=sk-ant-...
```

**❌ `Database not found`**
```bash
# Database should be auto-created. If not:
python -c "import sqlite3; conn = sqlite3.connect('data/sample_database.db'); conn.executescript(open('data/sample_database.sql').read()); conn.close()"
```

**❌ Model download slow**

First run downloads ~90MB sentence transformer model. Subsequent runs are instant.

### Performance Tips

- Run in virtual environment for clean dependencies
- First exercise loads embedding model (~5 seconds)
- Use SSD for faster database queries
- Disable AI features for offline practice (uses template hints)

---

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14+, Linux
- **Python**: 3.7 or higher
- **RAM**: 2 GB (4 GB recommended for AI features)
- **Storage**: 500 MB (including model cache)
- **Internet**: Required for AI features

### Dependencies

```
anthropic>=0.40.0           # Claude AI SDK
python-dotenv>=1.0.0        # Environment management
sentence-transformers>=2.2.0 # Semantic similarity
numpy>=1.24.0               # Vector math
```

---

## 🎓 Learning Tips

1. **📖 Read the cheatsheet first** - Skim `src/cheatsheet.md` for SQL syntax reference
2. **🎯 Start with beginner** - Even if experienced, get familiar with the database
3. **🧪 Experiment freely** - Try different approaches, learn from mistakes
4. **💡 Use hints wisely** - Try once without hints, then use them to learn
5. **📊 Check similarity scores** - They show you how close you are
6. **🔄 Practice regularly** - 10-15 minutes daily beats 2-hour weekend sessions
7. **🤖 Learn from AI feedback** - Understand WHY your answer was close but not exact
8. **✅ Complete all levels** - Don't skip to advanced too quickly

---

## 🔮 Future Enhancements

- [ ] **Progress persistence** - Save completion across sessions
- [ ] **Spaced repetition** - Smart scheduling of review exercises
- [ ] **Difficulty customization** - Adjust hint detail level
- [ ] **Performance metrics** - Track avg attempts, time per exercise
- [ ] **Web interface** - Browser-based version with syntax highlighting
- [ ] **Multi-database support** - PostgreSQL, MySQL connectors
- [ ] **Team mode** - Shared progress for classrooms
- [ ] **Export progress** - Generate completion certificates
- [ ] **Voice hints** - Optional audio explanations
- [ ] **VSCode extension** - Practice within your IDE

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- 📝 Add more exercises (especially intermediate/advanced)
- 🗄️ Create alternative database schemas (healthcare, finance, social media)
- 🌍 Translations (internationalization)
- 🎨 Improve hint quality with better prompts
- 🧪 Add unit tests
- 📚 Create video tutorials
- 🐛 Bug fixes and optimizations

**How to contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is provided as an **educational tool** for learning SQL.

**API Usage**: When using the Anthropic API, ensure compliance with [Anthropic's Usage Policies](https://www.anthropic.com/legal/aup).

**Code**: Feel free to modify, extend, and share for educational purposes.

---

## 📚 Resources

### SQL Learning
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQL Style Guide](https://www.sqlstyle.guide/)
- [SQL Zoo](https://sqlzoo.net/) - Additional practice
- [Mode SQL Tutorial](https://mode.com/sql-tutorial/)

### AI & APIs
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Claude AI Overview](https://www.anthropic.com/claude)
- [Sentence Transformers](https://www.sbert.net/)

### Project Documentation
- `CLAUDE.md` - Original design specification
- `src/cheatsheet.md` - Complete SQL reference
- `data/queries.json` - All exercise definitions

---

## 💬 Support

**Need help?**
1. 📖 Check the [Troubleshooting](#-troubleshooting) section
2. 📝 Review `src/cheatsheet.md` for SQL syntax
3. 🔍 Read exercise hints carefully
4. 💬 Open an issue on GitHub

**Found a bug?** Please report with:
- Python version (`python --version`)
- Error message
- Steps to reproduce

---

## 🌟 Acknowledgments

Built with:
- [Claude AI](https://www.anthropic.com/claude) by Anthropic
- [Sentence Transformers](https://www.sbert.net/) for semantic similarity
- [SQLite](https://www.sqlite.org/) for the database engine

---

<div align="center">

**🚀 Happy Learning! Master SQL through intelligent practice.**

Made with ❤️ for SQL learners everywhere

[⬆ Back to Top](#-interactive-sql-tutorial-system)

</div>
