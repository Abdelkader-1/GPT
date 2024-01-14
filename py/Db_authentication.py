import sqlalchemy as sa
import pandas as pd
from langchain.sql_database import SQLDatabase
class Auth:
    def __init__(self):
        self.email = None
        self.password = None

    

    def read_credentials(self):
        """Reads email and password from Credintials.txt."""
        with open("Credintials.txt", "r") as f:
            lines = f.readlines()
        self.email = lines[0].strip()  # Assign first line to email
        self.password = lines[1].strip()  # Assign second line to password



    def connect_to_database(self):
        """Connects to the SQL database using read credentials."""
        server = 'anmx3c2yurjethctgyba6xtuaq-vkvbn7t4322edeguc3ufhjtjeu.datawarehouse.pbidedicated.windows.net'
        database = 'likeCard'
        driver = 'ODBC Driver 18 for SQL Server'

        # Encode @ symbols for compatibility
        user = self.email.replace("@", "%40")
        password = self.password.replace("@", "%40")

        db_string = f'mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver}&Trusted_Connection=no&Authentication=ActiveDirectoryInteractive'
        db=SQLDatabase.from_uri(db_string)

        return db  # Return the database connection object