# utils.py

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            # Initialize the database connection here
            cls._instance.connection = "Initialized database connection"
        return cls._instance

# med/utils.py

class SingletonMeta(type):
    """
    Singleton metaclass to ensure only one instance of a class is created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# med/utils.py
from django.db import connections
from django.db.utils import OperationalError

class DatabaseConnection:
    def __init__(self, database_alias='default'):
        self.database_alias = database_alias

    def get_connection_status(self):
        try:
            with connections[self.database_alias].cursor() as cursor:
                cursor.execute("SELECT 1")
            return "Connected"
        except OperationalError:
            return "Disconnected"

