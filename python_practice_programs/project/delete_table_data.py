import sys
import os

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mysql_connection import get_mysql_conn
from read_config import get_config_value


def delete_all_saved_questions():
    """Delete all data from the questions table"""
    try:
        conn = get_mysql_conn()
        
        if conn is None:
            print("Error: Unable to connect to the database.")
            return False
        
        cursor = conn.cursor()
        query = get_config_value('mysql', 'delete_query_1')
        
        if query is None:
            print("Error: Unable to read delete query from config.")
            cursor.close()
            conn.close()
            return False
        
        cursor.execute(query)
        conn.commit()
        
        rows_affected = cursor.rowcount
        
        if rows_affected > 0:
            print(f"✓ Successfully deleted {rows_affected} rows from the questions table!")
        else:
            print("ℹ No rows were deleted (table may be empty)")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: Unable to delete data: {e}")
        return False


if __name__ == "__main__":
    delete_all_saved_questions()
