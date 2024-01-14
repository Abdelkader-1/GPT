import os
from dotenv import load_dotenv
from langchain.llms import openai
from langchain_community.llms import AzureOpenAI
from langchain.agents import create_sql_agent,create_openai_functions_agent,create_openapi_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
import Db_authentication
import modelConnection
import model
import auth_ser
if __name__ == '__main__':
    #connect to the model
    conn = modelConnection.conn()
    conn.set_openai_environment_variables()
    #connect to the database
    auth = Db_authentication.Auth()
    auth.read_credentials()
    df_dict,table_schema,engine = auth.schema_describtion()

    models = model.models()
    
    #x = model.models(df_dict,table_schema,"what is the total sales per business line")
    text = "what is the top 5 products and there amount"

    result = models.executeSQLquery(df_dict,text,table_schema ,engine,5)
    ansuwer = models.get_result_prompt(text, df_dict, table_schema, result)
    #out = model.langChain_sqlModel()
    print(ansuwer)