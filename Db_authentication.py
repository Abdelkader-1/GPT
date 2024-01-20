import sqlalchemy as sa
import pandas as pd
from langchain.sql_database import SQLDatabase
import pyodbc
import urllib.parse

class Auth:
    def __init__(self):
        #self.email = None
        #self.password = None
        self.server = 'anmx3c2yurjethctgyba6xtuaq-vkvbn7t4322edeguc3ufhjtjeu.datawarehouse.pbidedicated.windows.net'
        self.database = 'likeCard'
        self.driver = 'ODBC Driver 18 for SQL Server'

    

    def read_credentials(self):
        """Reads email and password from Credintials.txt."""
        with open("Credintials.txt", "r") as f:
            lines = f.readlines()
        self.email = lines[0].strip()  # Assign first line to email
        self.password = lines[1].strip()  # Assign second line to password



    def LangChain_connect_to_database(self):
        """Connects to the SQL database using read credentials."""


        # Encode @ symbols for compatibility
        user = self.email.replace("@", "%40")
        password = self.password.replace("@", "%40")

        #db_string = f'mssql+pyodbc://{user}:{password}@{self.server}/{self.database}?driver={self.driver}&Trusted_Connection=no&Authentication=ActiveDirectoryInteractive'
        db_string = f'mssql+pyodbc://{user}:{password}@{self.server}/{self.database}?driver={self.driver}&Trusted_Connection=yes'

        db=SQLDatabase.from_uri(db_string)

        return db  # Return the database connection object
    def engine_connect_to_database(self):
        """Connects to the SQL database using read credentials."""

        # Encode @ symbols for compatibility
        user = self.email.replace("@", "%40")
        password = self.password.replace("@", "%40")
        db_string = f'mssql+pyodbc://{user}:{password}@{self.server}/{self.database}?driver={self.driver}&Trusted_Connection=no&Authentication=ActiveDirectoryInteractive'
        #db_string = f'mssql+pyodbc://{user}:{password}@{self.server}/{self.database}?driver={self.driver}&Trusted_Connection=no'

                
        
        print("connection string: ", db_string)
        
        
        engine = sa.create_engine(db_string, echo=True, connect_args={'autocommit': True}, fast_executemany=True,pool_pre_ping=True)
        return engine
    def schema_describtion(self):
        sql_query = '''
        SELECT 
            TABLE_SCHEMA,
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE
        FROM 
            INFORMATION_SCHEMA.COLUMNS
        WHERE 
            TABLE_NAME IN (SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE')
            and TABLE_NAME like 'dim_products' 
            or TABLE_NAME like 'fact_transactions%' 
            or TABLE_NAME like 'dim_allusers%'
            or TABLE_NAME like 'dim_stores%'
            or TABLE_NAME like 'dimDate%'
            or TABLE_NAME like 'dim_categories%'
            or TABLE_NAME like 'dim_parent_categories%'
            or TABLE_NAME like 'dim_B2B_Sales_Channel'
        '''


        engine = self.engine_connect_to_database()
        df = pd.read_sql(sql_query, engine)
        table_schema=df.loc[0][0]
        df.drop(columns=['TABLE_SCHEMA'])
        df_dict=df.to_dict(orient='records')
        return df_dict,table_schema,engine