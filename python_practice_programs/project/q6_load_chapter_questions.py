import sys
import os

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mysql_connection import get_mysql_conn
from read_config import get_config_value


def load_questions_by_chapter(chapter_name):
    """
    Load all questions from a specific chapter in the database
    
    Args:
        chapter_name: Name of the chapter to search for
        
    Returns:
        List of (id, question, answer) tuples or empty list if not found
    """
    try:
        # Validate input
        if not chapter_name or chapter_name.strip() == "":
            print("✗ Error: Chapter name cannot be empty!")
            return []
        
        chapter_name = chapter_name.strip()
        
        conn = get_mysql_conn()
        
        if conn is None:
            print("✗ Error: Unable to connect to the database.")
            return []
        
        cursor = conn.cursor()
        
        # Query to search for questions containing the chapter name
        # Using LIKE for flexible matching
        query = f"SELECT * FROM questions WHERE question LIKE '%{chapter_name}%' OR answer LIKE '%{chapter_name}%'"
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"✗ Error executing query: {e}")
            cursor.close()
            conn.close()
            return []
        
    except Exception as e:
        print(f"✗ Error in load_questions_by_chapter: {e}")
        return []


def display_chapter_questions(chapter_name, results):
    """
    Display questions from a chapter in a formatted table
    
    Args:
        chapter_name: Name of the chapter
        results: List of question tuples from database
    """
    if not results:
        print(f"\n✗ No questions found for chapter: '{chapter_name}'")
        print("   Please check the spelling and try again.")
        return False
    
    print(f"\n{'='*100}")
    print(f"QUESTIONS FROM CHAPTER: {chapter_name}")
    print(f"{'='*100}")
    print(f"{'ID':<5} | {'QUESTION':<50} | {'ANSWER':<35}")
    print(f"{'-'*100}")
    
    count = 0
    for row in results:
        question_preview = row[1][:50] if len(row[1]) > 50 else row[1]
        answer_preview = row[2][:35] if len(row[2]) > 35 else row[2]
        print(f"{row[0]:<5} | {question_preview:<50} | {answer_preview:<35}")
        count += 1
    
    print(f"{'='*100}")
    print(f"✓ Total questions found: {count}")
    print(f"{'='*100}\n")
    
    return True


def main():
    """
    Main function with command-line argument handling
    
    Usage:
        python q6_load_chapter_questions.py "Chapter Name"
        python q6_load_chapter_questions.py "states of matter"
    """
    try:
        # Check command-line arguments
        if len(sys.argv) < 2:
            print("\n" + "="*80)
            print("PROJECT 6: LOAD QUESTIONS FROM CHAPTER")
            print("="*80)
            print("\nUsage: python q6_load_chapter_questions.py <chapter_name>")
            print("\nExamples:")
            print("  python q6_load_chapter_questions.py 'Chapter 1'")
            print("  python q6_load_chapter_questions.py 'states of matter'")
            print("  python q6_load_chapter_questions.py 'atoms'")
            print("\nError Handling:")
            print("  - Empty string input: Error message displayed")
            print("  - No matching questions: 'Not found' message")
            print("="*80 + "\n")
            sys.exit(1)
        
        # Get chapter name from command line
        chapter_name = " ".join(sys.argv[1:])
        
        # Validate input
        if not chapter_name or chapter_name.strip() == "":
            print("✗ Error: Chapter name cannot be empty!")
            print("Usage: python q6_load_chapter_questions.py <chapter_name>")
            sys.exit(1)
        
        chapter_name = chapter_name.strip()
        
        print(f"\nℹ Searching for questions in: '{chapter_name}'...")
        print("Please wait...")
        
        # Load questions from database
        results = load_questions_by_chapter(chapter_name)
        
        # Display results
        if results:
            success = display_chapter_questions(chapter_name, results)
            if success:
                sys.exit(0)
        else:
            print(f"\n✗ No questions found for chapter: '{chapter_name}'")
            print("Possible reasons:")
            print("  1. Chapter name doesn't exist in database")
            print("  2. No questions have been inserted for this chapter")
            print("  3. Check spelling of chapter name")
            print("\nTip: Run q5_print_saved_questions.py to see all available questions\n")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\nℹ Search cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

