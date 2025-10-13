#!/usr/bin/env python3
"""
Interactive SQL Tutorial System
Provides guided learning with instant feedback
"""

import json
import sqlite3
import anthropic
import os
import numpy as np
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

class SQLTutor:
    def __init__(self, db_path: str, queries_path: str):
        """Initialize SQL Tutor with database and queries."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        with open(queries_path, 'r') as f:
            self.queries = json.load(f)

        # Initialize Anthropic client
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("Warning: ANTHROPIC_API_KEY not found in environment variables.")
            print("AI feedback will not be available.")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=api_key)

        # Initialize sentence transformer for semantic similarity
        print("Loading semantic similarity model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded successfully!\n")

        # Track completed exercises to avoid repetition
        self.completed_exercises = {
            'beginner': set(),
            'intermediate': set(),
            'advanced': set()
        }
        self.generated_exercise_counter = 0

    def get_query_by_level(self, level: str) -> Dict:
        """Get random query from specified difficulty level."""
        import random
        if level not in self.queries:
            raise ValueError(f"Invalid level: {level}. Choose from: {list(self.queries.keys())}")

        # Check if all exercises at this level have been completed
        total_exercises = len(self.queries[level])
        completed_count = len(self.completed_exercises[level])

        # If user has completed all exercises, generate a new one
        if completed_count >= total_exercises and self.client:
            print(f"\n🎉 Congratulations! You've completed all {total_exercises} {level} exercises!")
            print("🤖 Generating a new challenge for you...\n")
            new_exercise = self.generate_new_exercise(level)
            if new_exercise:
                self.queries[level].append(new_exercise)
                return new_exercise

        # Get an uncompleted exercise if possible
        uncompleted = [q for q in self.queries[level] if q['id'] not in self.completed_exercises[level]]
        if uncompleted:
            return random.choice(uncompleted)

        # If all completed but can't generate new ones, return random
        return random.choice(self.queries[level])

    def generate_new_exercise(self, level: str) -> Optional[Dict]:
        """Generate a new SQL exercise using the LLM based on existing exercises."""
        if not self.client:
            print("⚠️  Cannot generate new exercises without AI. Repeating existing exercises.")
            return None

        # Get a few examples from this level
        examples = self.queries[level][:3]
        examples_text = "\n".join([
            f"- Question: {ex['question']}\n  Solution: {ex['solution']}\n  Concepts: {', '.join(ex['concepts'])}"
            for ex in examples
        ])

        # Get table structure for context
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [row[0] for row in self.cursor.fetchall() if not row[0].startswith('sqlite_')]

        prompt = f"""You are creating a new SQL practice exercise for a student at the {level} level.

Database tables available: {', '.join(tables)}

Here are examples of {level} level exercises:
{examples_text}

Create a NEW, UNIQUE SQL exercise at the {level} level that:
1. Uses the available tables in our e-commerce database
2. Is similar in difficulty to the examples
3. Tests different aspects than the examples (avoid exact duplicates)
4. Has a clear, specific question
5. Includes the correct SQL solution
6. Lists 2-4 SQL concepts it covers

Return your response in this EXACT JSON format:
{{
  "question": "The question text here",
  "solution": "SELECT ... FROM ... WHERE ...",
  "concepts": ["concept1", "concept2", "concept3"],
  "hint": "Optional hint for the student"
}}

Only return the JSON object, nothing else."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # Extract JSON from response (in case there's extra text)
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)

            exercise_data = json.loads(response_text)

            # Add generated ID
            self.generated_exercise_counter += 1
            exercise_data['id'] = f"{level[0]}gen{self.generated_exercise_counter}"

            print(f"✅ New exercise generated: {exercise_data['question']}\n")
            return exercise_data

        except Exception as e:
            print(f"⚠️  Error generating new exercise: {str(e)}")
            return None

    def execute_query(self, query: str) -> Tuple[bool, Optional[List], Optional[List], Optional[str]]:
        """
        Execute query and return results with error handling.

        Returns:
            Tuple of (success, results, columns, error_message)
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
            return True, results, columns, None
        except Exception as e:
            return False, None, None, str(e)

    def compare_results(self, user_query: str, solution_query: str) -> bool:
        """Compare results of user query with solution."""
        success1, results1, cols1, _ = self.execute_query(user_query)
        success2, results2, cols2, _ = self.execute_query(solution_query)

        if not success1 or not success2:
            return False

        # Sort results to handle different ordering
        sorted_results1 = sorted(results1) if results1 else []
        sorted_results2 = sorted(results2) if results2 else []

        return sorted_results1 == sorted_results2 and cols1 == cols2

    def calculate_query_similarity(self, query1: str, query2: str) -> float:
        """
        Calculate semantic similarity between two SQL queries using embeddings.

        Returns:
            Similarity score between 0 and 1 (1 being identical)
        """
        # Normalize queries (lowercase, strip whitespace)
        q1 = query1.lower().strip()
        q2 = query2.lower().strip()

        # Generate embeddings
        embeddings = self.embedder.encode([q1, q2])

        # Calculate cosine similarity
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )

        return float(similarity)

    def get_progressive_hint(self, query_data: Dict, user_query: str, similarity_score: float, attempt: int) -> str:
        """
        Generate progressive hints based on similarity score and attempt number.

        Args:
            query_data: The exercise data
            user_query: User's SQL query
            similarity_score: Semantic similarity to solution (0-1)
            attempt: Current attempt number

        Returns:
            Hint text based on how close the user is
        """
        if not self.client:
            # Provide basic hints without AI
            if similarity_score > 0.8:
                return "You're very close! Check your column names or table joins."
            elif similarity_score > 0.6:
                return "You're on the right track. Review the required columns and conditions."
            elif similarity_score > 0.4:
                return "You have some correct elements. Check the SQL clauses you're using."
            else:
                return f"Try a different approach. Remember the concepts: {', '.join(query_data['concepts'])}"

        # Use AI for more detailed hints
        prompt = f"""You are an SQL tutor helping a student who is struggling with a problem.

Question: {query_data['question']}
Required concepts: {', '.join(query_data['concepts'])}
Expected solution: {query_data['solution']}
Student's query: {user_query}
Similarity score: {similarity_score:.2f} (0=completely different, 1=identical)
Attempt number: {attempt}

Based on the similarity score:
- If > 0.8: The student is VERY CLOSE. Point out the specific small difference (column name, condition, etc.)
- If 0.6-0.8: The student has the right structure. Guide them on what's missing or incorrect.
- If 0.4-0.6: The student has some correct elements. Give a hint about which SQL clause needs work.
- If < 0.4: The student needs more guidance. Suggest which SQL concepts to focus on without giving the answer.

Provide a concise, encouraging hint (2-3 sentences max) that helps them get closer without revealing the full solution."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error generating hint: {str(e)}"

    def get_ai_feedback(self, query_data: Dict, user_query: str, is_correct: bool) -> str:
        """Get detailed feedback from Claude."""
        if not self.client:
            return "AI feedback is not available. Please set ANTHROPIC_API_KEY environment variable."

        prompt = f"""You are an SQL tutor. A student attempted this problem:

Question: {query_data['question']}
Expected solution: {query_data['solution']}
Student's query: {user_query}
Result: {'Correct' if is_correct else 'Incorrect'}

Provide encouraging, educational feedback:
1. If correct: Praise the solution and explain what concepts they used well
2. If incorrect: Gently explain what went wrong and provide hints without giving away the full answer
3. Suggest optimizations or alternative approaches if relevant
4. Keep it concise (2-3 paragraphs max)

Focus on teaching, not just correcting."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error getting AI feedback: {str(e)}"

    def practice_session(self, level: str = "beginner"):
        """Run an interactive practice session with multiple attempts and progressive hints."""
        print(f"\n{'='*60}")
        print(f"SQL Practice Session - {level.upper()} Level")
        print(f"{'='*60}\n")

        query_data = self.get_query_by_level(level)

        print(f"Question: {query_data['question']}")
        print(f"Concepts: {', '.join(query_data['concepts'])}")

        if 'hint' in query_data:
            show_hint = input("\nWould you like a hint? (y/n): ").lower()
            if show_hint == 'y':
                print(f"Hint: {query_data['hint']}")

        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            attempt += 1
            print(f"\n{'Attempt ' + str(attempt) if attempt > 1 else 'Enter your SQL query'} (end with semicolon):")
            user_query = input("> ").strip()

            # Validate syntax first
            success, results, columns, error = self.execute_query(user_query)

            if not success:
                print(f"\n❌ Syntax Error: {error}")

                # Calculate similarity even with syntax errors
                try:
                    similarity = self.calculate_query_similarity(user_query, query_data['solution'])
                    print(f"📊 Similarity to solution: {similarity*100:.1f}%")
                except:
                    pass

                # Show hint from query data
                if 'hint' in query_data and query_data['hint']:
                    print(f"\n💡 Hint: {query_data['hint']}")

                print("\nWould you like to:")
                print("1. Try again")
                print("2. See the solution")
                print("3. Get AI help")
                choice = input("Enter choice (1/2/3): ")

                if choice == '2':
                    print(f"\n💡 Solution: {query_data['solution']}")
                    break
                elif choice == '3':
                    feedback = self.get_ai_feedback(query_data, user_query, False)
                    print(f"\n🤖 AI Tutor says:\n{feedback}")

                    # Ask if they want to try again with the same lesson
                    retry = input("\nWould you like to try again? (y/n): ").lower()
                    if retry == 'y':
                        continue  # Go back for another attempt
                    else:
                        break  # Exit to "Try another question?"
                # If choice is '1', continue to next attempt
                continue

            # Compare results
            is_correct = self.compare_results(user_query, query_data['solution'])

            if is_correct:
                print("\n✅ Correct! Great job!")
                if attempt > 1:
                    print(f"   (Solved in {attempt} attempts)")

                # Mark exercise as completed
                self.completed_exercises[level].add(query_data['id'])

                # Show progress
                total = len(self.queries[level])
                completed = len(self.completed_exercises[level])
                print(f"   Progress: {completed}/{total} exercises completed at {level} level")

                print(f"\nYour results:")
                self.display_results(results, columns)
                break
            else:
                # Calculate semantic similarity
                similarity = self.calculate_query_similarity(user_query, query_data['solution'])

                print("\n❌ Not quite right. The query runs but produces different results.")
                print(f"📊 Similarity to solution: {similarity*100:.1f}%")

                # Show results comparison
                print(f"\nYour results:")
                self.display_results(results, columns)

                print(f"\nExpected results:")
                success_sol, results_sol, columns_sol, _ = self.execute_query(query_data['solution'])
                self.display_results(results_sol, columns_sol)

                # Show hint from query data first
                if 'hint' in query_data and query_data['hint']:
                    print(f"\n💡 Hint: {query_data['hint']}")

                # Provide progressive hints based on similarity
                if attempt < max_attempts:
                    print(f"\n💡 Generating AI hint based on your attempt (Attempt {attempt}/{max_attempts})...")
                    ai_hint = self.get_progressive_hint(query_data, user_query, similarity, attempt)
                    print(f"\n🔍 AI Hint: {ai_hint}")

                    print("\nWould you like to:")
                    print("1. Try again")
                    print("2. See the solution")
                    print("3. Get AI help")
                    choice = input("Enter choice (1/2/3): ")

                    if choice == '2':
                        print(f"\n💡 Solution: {query_data['solution']}")

                        # Get AI feedback showing the difference
                        print("\n📚 Understanding the solution...\n")
                        feedback = self.get_ai_feedback(query_data, user_query, False)
                        print(f"🤖 {feedback}")
                        break
                    elif choice == '3':
                        print("\n📚 Getting detailed feedback...\n")
                        feedback = self.get_ai_feedback(query_data, user_query, False)
                        print(f"🤖 {feedback}")

                        # Ask if they want to try again
                        retry = input("\nWould you like to try again? (y/n): ").lower()
                        if retry == 'y':
                            continue
                        else:
                            break
                    # If choice is '1', continue to next attempt
                else:
                    # Max attempts reached
                    print(f"\n⏰ You've used all {max_attempts} attempts.")

                    # Show hint from query data
                    if 'hint' in query_data and query_data['hint']:
                        print(f"\n💡 Hint: {query_data['hint']}")

                    print(f"\n💡 Solution: {query_data['solution']}")

                    # Get comprehensive feedback
                    print("\n📚 Getting comprehensive feedback...\n")
                    feedback = self.get_ai_feedback(query_data, user_query, False)
                    print(f"🤖 {feedback}")
                    break

        # Continue or exit
        print("\n" + "="*60)
        cont = input("Try another question? (y/n): ").lower()
        if cont == 'y':
            self.practice_session(level)

    def display_results(self, results: List, columns: List):
        """Pretty print query results."""
        if not results:
            print("(No rows returned)")
            return

        # Print column headers
        header = " | ".join(str(col) for col in columns)
        print(header)
        print("-" * len(header))

        # Print rows
        for row in results[:10]:  # Limit to first 10 rows
            print(" | ".join(str(val) for val in row))

        if len(results) > 10:
            print(f"... ({len(results) - 10} more rows)")

    def show_database_structure(self):
        """Display the database schema and structure."""
        print("\n" + "="*60)
        print("DATABASE STRUCTURE")
        print("="*60 + "\n")

        # Get all tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [row[0] for row in self.cursor.fetchall()]

        for table in tables:
            # Skip SQLite internal tables
            if table.startswith('sqlite_'):
                continue

            print(f"\n📋 Table: {table.upper()}")
            print("-" * 60)

            # Get table info
            self.cursor.execute(f"PRAGMA table_info({table});")
            columns = self.cursor.fetchall()

            for col in columns:
                col_id, name, col_type, not_null, default_val, pk = col
                constraints = []
                if pk:
                    constraints.append("PRIMARY KEY")
                if not_null:
                    constraints.append("NOT NULL")
                if default_val:
                    constraints.append(f"DEFAULT {default_val}")

                constraint_str = f" ({', '.join(constraints)})" if constraints else ""
                print(f"  • {name}: {col_type}{constraint_str}")

            # Get row count
            self.cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = self.cursor.fetchone()[0]
            print(f"\n  Total rows: {count}")

        print("\n" + "="*60 + "\n")

    def show_example_exercises(self):
        """Display example exercises for each difficulty level."""
        print("="*60)
        print("EXAMPLE EXERCISES")
        print("="*60 + "\n")

        for level in ['beginner', 'intermediate', 'advanced']:
            print(f"\n🎯 {level.upper()} Level Examples:")
            print("-" * 60)

            # Show first 3 exercises from each level
            examples = self.queries[level][:3]

            for i, exercise in enumerate(examples, 1):
                print(f"\n  {i}. {exercise['question']}")
                print(f"     Concepts: {', '.join(exercise['concepts'])}")
                if 'hint' in exercise:
                    print(f"     Hint: {exercise['hint']}")

        print("\n" + "="*60 + "\n")

    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    """Main entry point for the SQL tutor."""
    # Load environment variables from .env file
    load_dotenv()

    print("""
╔════════════════════════════════════════════╗
║     Interactive SQL Tutorial System        ║
║          Powered by Claude AI              ║
╚════════════════════════════════════════════╝
    """)

    # Get paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, 'data', 'sample_database.db')
    queries_path = os.path.join(project_root, 'data', 'queries.json')

    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        print("Please run the following command to create the database:")
        print(f"  sqlite3 {db_path} < {os.path.join(project_root, 'data', 'sample_database.sql')}")
        return

    # Check if queries file exists
    if not os.path.exists(queries_path):
        print(f"Error: Queries file not found at {queries_path}")
        return

    tutor = SQLTutor(db_path, queries_path)

    try:
        # Show database structure
        tutor.show_database_structure()

        # Show example exercises
        tutor.show_example_exercises()

        # Ask user if they want to continue
        print("Ready to start practicing?")
        ready = input("Press Enter to continue or 'q' to quit: ").lower()
        if ready == 'q':
            print("\nGoodbye! Come back when you're ready to learn SQL! 👋")
            return

        print("\nChoose difficulty level:")
        print("1. Beginner")
        print("2. Intermediate")
        print("3. Advanced")

        choice = input("\nEnter choice (1/2/3): ")
        level_map = {'1': 'beginner', '2': 'intermediate', '3': 'advanced'}
        level = level_map.get(choice, 'beginner')

        tutor.practice_session(level)
    finally:
        tutor.close()
        print("\nThank you for using SQL Tutor! Keep practicing! 🚀")


if __name__ == "__main__":
    main()
