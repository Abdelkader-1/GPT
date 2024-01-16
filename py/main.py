import os
#from dotenv import load_dotenv
from langchain.llms import openai
from langchain_community.llms import AzureOpenAI
from langchain.agents import create_sql_agent,create_openai_functions_agent,create_openapi_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
import Db_authentication
import modelConnection
import model
import keyboard
import history
if __name__ == '__main__':
    #connect to the model
    conn = modelConnection.conn()
    conn.set_openai_environment_variables()
    #connect to the database
    auth = Db_authentication.Auth()
    auth.read_credentials()
    df_dict,table_schema,engine = auth.schema_describtion()

    models = model.models()
    history=history.history()
    
    while True:
        # x = model.models(df_dict, table_schema, "what is the total sales per business line")
        massages=history.massages
        sqlmessages=history.sqlmessages
        text = input("Enter your question: ")
        user_prompt=f"{text}"
        history.add_messages("user", user_prompt)
        history.add_messagesql("user", user_prompt)
        #history.process_user_querysql(text)
        #text = "what is the top 5 products and their amount"
       
        result,query = models.executeSQLquery(df_dict, text, table_schema, engine, 5,sqlmessages)
        history.add_messagesql("assistant", f"{query}")
        print(query)
        print(result)
        history.add_messages("user", f"{result}")
        try:
            answer = models.get_result_prompt(text, df_dict, table_schema, result,massages)
            out_graph = models.graph(text,query,df_dict,table_schema,result)
        except Exception as e:
            continue
        history.add_messages("assistant", f"{answer}")
        # out = model.langChain_sqlModel()
        # Check if 'esc' key is pressed to exit the loop
        if keyboard.is_pressed('Esc'):
            print("Exiting the loop.")
            break