import sys
import os
import re

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mysql_connection import get_mysql_conn
from read_config import get_config_value
from q1_pdf_reader import read_pdf_text


def extract_all_questions(text):
    """
    Extract ALL question-answer pairs from text using regex
    
    Returns:
        List of (question, answer) tuples
    """
    try:
        questions_data = []
        
        # Pattern to extract questions with their answers
        # Matches: "1. Question text\nAnswer: A) ..."
        pattern = r"(\d+\.\s*.*?)\s*Answer:\s*([A-D]\).*?)(?=\n\d+\.|$)"
        
        matches = re.findall(pattern, text, re.DOTALL)
        
        if not matches:
            print("❌ No questions found in PDF.")
            return []
        
        for question, answer in matches:
            # Clean up the text
            question_clean = question.strip()
            answer_clean = answer.strip()
            
            if question_clean and answer_clean:
                questions_data.append((question_clean, answer_clean))
        
        return questions_data
        
    except Exception as e:
        print(f"❌ Error extracting questions: {e}")
        return []


def insert_all_questions_to_db(questions_list):
    """
    Insert all questions into the database
    
    Args:
        questions_list: List of (question, answer) tuples
        
    Returns:
        Number of successfully inserted questions
    """
    try:
        if not questions_list:
            print("❌ No questions to insert.")
            return 0
        
        conn = get_mysql_conn()
        
        if conn is None:
            print("❌ Error: Unable to connect to the database.")
            return 0
        
        cursor = conn.cursor()
        query = get_config_value('mysql', 'insert_query_1')
        
        if query is None:
            print("❌ Error: Unable to read insert query from config.")
            cursor.close()
            conn.close()
            return 0
        
        # Remove "VALUES" if it's already in the query template
        if "VALUES" in query:
            base_query = query.split("VALUES")[0].strip()
        else:
            base_query = query
        
        inserted_count = 0
        failed_count = 0
        
        for idx, (question, answer) in enumerate(questions_list, 1):
            try:
                # Execute insert for each question
                full_query = base_query + " VALUES (%s, %s)"
                cursor.execute(full_query, (question.strip(), answer.strip()))
                inserted_count += 1
                
                # Print progress every 5 questions
                if idx % 5 == 0:
                    print(f"  ✓ Processed {idx}/{len(questions_list)} questions...")
                
            except Exception as e:
                failed_count += 1
                print(f"  ❌ Failed to insert question {idx}: {e}")
                continue
        
        # Commit all changes
        conn.commit()
        cursor.close()
        conn.close()
        
        return inserted_count, failed_count
        
    except Exception as e:
        print(f"❌ Error in insert_all_questions_to_db: {e}")
        return 0, 0


def display_insertion_summary(total, inserted, failed):
    """Display summary of insertion"""
    print("\n" + "="*80)
    print("BULK INSERT SUMMARY")
    print("="*80)
    print(f"Total questions found in PDF:        {total}")
    print(f"Successfully inserted to database:   {inserted} ✓")
    print(f"Failed to insert:                    {failed} ✗")
    print("="*80 + "\n")
    
    if inserted > 0:
        print(f"✓ {inserted} questions successfully added to database!")
    
    if failed > 0:
        print(f"⚠ {failed} questions failed to insert. Check errors above.")


def main():
    """
    Main function to extract and insert all questions from PDF
    """
    try:
        print("\n" + "="*80)
        print("PROJECT 5 - BULK INSERT ALL QUESTIONS")
        print("="*80)
        
        # Get input file path
        input_file = get_config_value('files', 'input_file')
        
        if input_file is None:
            print("❌ Error: Could not read input_file from configuration.")
            return False
        
        print(f"\n📄 Reading PDF: {input_file}")
        print("Extracting all questions...")
        
        # Read PDF text
        pdf_text = read_pdf_text(input_file)
        
        if pdf_text is None:
            print("❌ Error: Could not read PDF file.")
            return False
        
        # Extract all questions
        questions_list = extract_all_questions(pdf_text)
        
        if not questions_list:
            print("❌ No questions found in PDF.")
            return False
        
        print(f"\n✓ Found {len(questions_list)} questions in PDF")
        print("\nSample questions:")
        print("-" * 80)
        
        # Show first 3 questions as preview
        for i, (q, a) in enumerate(questions_list[:3], 1):
            q_preview = q[:60] + "..." if len(q) > 60 else q
            a_preview = a[:40] + "..." if len(a) > 40 else a
            print(f"{i}. Q: {q_preview}")
            print(f"   A: {a_preview}\n")
        
        if len(questions_list) > 3:
            print(f"... and {len(questions_list) - 3} more questions\n")
        
        # Confirm before inserting
        response = input("Do you want to insert all these questions into the database? (yes/no): ").strip().lower()
        
        if response != 'yes':
            print("❌ Insertion cancelled by user.")
            return False
        
        print("\n" + "="*80)
        print("INSERTING QUESTIONS INTO DATABASE...")
        print("="*80 + "\n")
        
        # Insert all questions
        inserted, failed = insert_all_questions_to_db(questions_list)
        
        # Display summary
        display_insertion_summary(len(questions_list), inserted, failed)
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        return False
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

