import sqlalchemy as sa
import pandas as pd
#from langchain.sql_database import SQLDatabase
import pyodbc
import streamlit as st
import urllib
#from urllib.parse import quote_plus


class Auth:
    def __init__(self):
        self.server ='like4.database.windows.net'
        self.user1="CloudSA42bee827"
        self.pass1="XP2U@X3R5EOQ23"
        self.database="like"

        self.driver="ODBC Driver 17 for SQL Server"

    def read_credentials(self):
        """Reads email and password from Credintials.txt."""
        with open("Credintials.txt", "r") as f:
            lines = f.readlines()
        self.email = lines[0].strip()  # Assign first line to email
        self.password = lines[1].strip()  # Assign second line to password

    def engine_connect_to_database(self):
        """Connects to the SQL database using read credentials."""
        #user = self.email#.replace("@", "%40")
        #password = self.password#.replace("@", "%40")
        #db_string = f'mssql+pyodbc://{user}:{password}@{self.server}/{self.database}?driver={self.driver}&Trusted_Connection=no&Authentication=ActiveDirectoryInteractive'
       
        odbc_str = 'DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;UID='+self.user1+';DATABASE='+ self.database + ';PWD='+ self.pass1
        db_string = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
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
                    and TABLE_NAME like 'transactions'
                    '''
        engine = self.engine_connect_to_database()
        df = pd.read_sql(sql_query, engine)
        table_schema=df.loc[0][0]
        df.drop(columns=['TABLE_SCHEMA'])
        df_dict=df.to_dict(orient='records')
        return df_dict,table_schema,engine