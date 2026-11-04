import psycopg2
import os 
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def get_database_connection():
    try:
        # Retrieve database connection parameters from environment variables
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")

        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        )
        print("Database connection established successfully.")
        return connection  # Return the database connection object
        return {"message": "Database connection established successfully."}

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None  # Return None if the connection fails