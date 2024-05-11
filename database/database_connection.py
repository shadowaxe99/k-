```python
import os
import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None or self.connection.closed:
            try:
                self.connection = psycopg2.connect(
                    os.getenv('DATABASE_URL'),
                    cursor_factory=RealDictCursor
                )
            except psycopg2.DatabaseError as e:
                print(f"Database connection error: {e}")
                raise e
        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()

# Singleton pattern to ensure only one connection is used
database_connection = DatabaseConnection()
```