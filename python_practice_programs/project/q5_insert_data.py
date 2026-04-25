import sys
import os
import random
import re

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mysql_connection import get_mysql_conn
from q4_and_q6_read_regex_content import search_by_regex
from q5_print_saved_questions import print_all_saved_questions
from read_config import get_config_value


def insert_question(question, answer):
    """Insert a question and answer into the database"""
    try:
        conn = get_mysql_conn()
        
        if conn is None:
            print("Error: Unable to connect to the database.")
            return False
        
        cursor = conn.cursor()
        query = get_config_value('mysql', 'insert_query_1')
        
        if query is None:
            print("Error: Unable to read insert query from config.")
            cursor.close()
            conn.close()
            return False
        
        cursor.execute(query + '(%s, %s)', (question.strip(), answer.strip()))
        conn.commit()
        
        if cursor.rowcount > 0:
            print('✓ Question inserted successfully!')
            print_all_saved_questions()
            cursor.close()
            conn.close()
            return True
        else:
            print('✗ Insert failed.')
            cursor.close()
            conn.close()
            return False
            
    except Exception as e:
        print(f"Error: Unable to insert question: {e}")
        return False


def main():
    """Main function to search and insert a random question"""
    try:
        input_file = get_config_value('files', 'input_file')
        
        if input_file is None:
            print("Error: Unable to read input file path from config.")
            return False
        
        # Select a random search pattern
        search_key_num = str(random.randint(0, 9))
        search_key = 'search_' + search_key_num
        
        regex_key = get_config_value('search', search_key)
        
        if regex_key is None:
            print(f"Error: Unable to read {search_key} from config.")
            return False
        
        print(f"Searching for: '{regex_key}'")
        
        matches = search_by_regex(input_file, regex_key)
        
        if not matches:
            print("No matches found for the search pattern.")
            return False
        
        # Extract question and answer from first match
        match = re.search(r'\d+\.\s*(.*?)\n.*?Answer:\s*([A-D]\)\s*.*)', matches[0], re.DOTALL)
        
        if match:
            question = match.group(1)
            answer = match.group(2)
            insert_question(question, answer)
            return True
        else:
            print("Error: Unable to parse question and answer from match.")
            return False
            
    except Exception as e:
        print(f"Error in main: {e}")
        return False


if __name__ == "__main__":
    main()
