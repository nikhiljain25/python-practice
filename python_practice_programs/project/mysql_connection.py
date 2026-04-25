import sys
import os
import mysql.connector

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from read_config import get_config_value


def get_mysql_conn():
    """Establish MySQL database connection with proper error handling"""
    try:
        conn = mysql.connector.connect(
            host=get_config_value('mysql', 'host'),
            user=get_config_value('mysql', 'user'),
            password=get_config_value('mysql', 'password'),
            database=get_config_value('mysql', 'database'),
            port=int(get_config_value('mysql', 'port'))  # Convert port to integer
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error: Unable to connect to MySQL database: {e}")
        return None
    except ValueError:
        print(f"Error: Port number must be a valid integer")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while connecting to the database: {e}")
        return None
