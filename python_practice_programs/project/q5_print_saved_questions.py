import sys
import os

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mysql_connection import get_mysql_conn
from read_config import get_config_value


def print_all_saved_questions():
    """Display all questions stored in the database"""
    try:
        conn = get_mysql_conn()
        
        if conn is None:
            print("Error: Unable to connect to the database.")
            return False
        
        cursor = conn.cursor()
        query = get_config_value('mysql', 'select_query_1')
        
        if query is None:
            print("Error: Unable to read select query from config.")
            cursor.close()
            conn.close()
            return False
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("ℹ No questions found in the database.")
            cursor.close()
            conn.close()
            return True
        
        print(f"\n{'='*80}")
        print(f"{'ID':<5} | {'QUESTION':<40} | {'ANSWER':<20}")
        print(f"{'='*80}")
        
        for row in results:
            question_preview = row[1][:40] if len(row[1]) > 40 else row[1]
            answer_preview = row[2][:20] if len(row[2]) > 20 else row[2]
            print(f"{row[0]:<5} | {question_preview:<40} | {answer_preview:<20}")
        
        print(f"{'='*80}")
        print(f"✓ Total questions in database: {len(results)}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: Unable to fetch questions: {e}")
        return False


if __name__ == "__main__":
    print_all_saved_questions()
