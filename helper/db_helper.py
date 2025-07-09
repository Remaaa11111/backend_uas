import os
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_POOL_NAME = os.environ.get('DB_POOL_NAME')
POOL_SIZE = int(os.environ.get('POOL_SIZE', 5))  # Default to 5 if POOL_SIZE not set

# Initialize the DB connection pool
try:
    db_pool = MySQLConnectionPool(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        pool_size=POOL_SIZE,
        pool_name=DB_POOL_NAME
    )
    print("Database connection pool created successfully.")
except Error as e:
    print(f"Error creating database connection pool: {e}")
    raise  # Reraise the exception to stop execution if the pool can't be created


def get_connection():
    """
    Get a connection from the database pool.
    This function ensures that the connection is available.
    """
    try:
        connection = db_pool.get_connection()
        if connection.is_connected():
            connection.autocommit = True  # Set auto-commit if needed
            return connection
        else:
            raise Exception("Failed to get a connection from the pool.")
    except Error as e:
        print(f"Error getting connection from the pool: {e}")
        raise  # Reraise to allow handling at the caller level

