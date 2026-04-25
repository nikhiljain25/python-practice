import sys
import os

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mysql_connection import get_mysql_conn
from read_config import get_config_value


def create_questions_table():
    """Create the questions table in MySQL database"""
    try:
        conn = get_mysql_conn()
        
        if conn is None:
            print("Error: Unable to connect to the database.")
            return False
        
        cursor = conn.cursor()
        query = get_config_value('mysql', 'create_query_1')
        
        if query is None:
            print("Error: Unable to read create query from config.")
            cursor.close()
            conn.close()
            return False
        
        cursor.execute(query)
        conn.commit()
        
        print("✓ Questions table created successfully!")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: Unable to create table: {e}")
        return False


if __name__ == "__main__":
    create_questions_table()
