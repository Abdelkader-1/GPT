from langchain_community.llms import AzureOpenAI
#from langchain.llms import openai
import openai
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
import prompts
import pandas as pd
import history

class models:
    def __init__(self):
        self.dp = None
        self.question = None
    def langChain_sqlModel(self):    
        #make an instance of the model
        model = AzureOpenAI( model_name="gpt-35-turbo-instruct",deployment_name="gpt-35-turbo-instruct",temperature=0)

        #create the prompt
        p = prompts.promptFactory()
        prompt = p.defultprompt()

        #intialize the agent
        agent_executor = create_sql_agent(
            model,
            toolkit=SQLDatabaseToolkit(db=self.dp, llm=model),
            #add memory _|_
              agent_executor_kwargs={
                 "memory": ConversationBufferMemory(
                     input_key="question", memory_key="history", return_messages=True
                 )
             },
             suffix=prompt,
             input_variables=["question", "history","agent_scratchpad"],
            verbose=True
        )
        
        
        return agent_executor.invoke(self.question)


    query = None
    def generate_sql_query(self,dictionary, table_schema, text,sqlmessages):
               
        request = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=sqlmessages,
            stop=None,
        )
        global query
        query = request.choices[0].message.content
        print("from generate sql query")
        print(sqlmessages)
        return query



    def executeSQLquery(self,df_dict,text,table_schema,engine,max_retries,sqlmessages):
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                query = self.generate_sql_query(df_dict,text,table_schema,sqlmessages)
                result = pd.read_sql(query,engine)
                print("!!!!!!!!from executeSQLquery !!!!!!!")
                print(query)
                print(result)
                return result,query
            except Exception as e:
                print(f"Error executing query: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Retrying... (Attempt {retry_count}/{max_retries})")
                else:
                    print("Max retry attempts reached. Exiting.")
                    raise
        

    def get_result_prompt(self,question, df_dict, table_schema, queryResult,massages):
        
        request = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=massages,
                stop=None,
                temperature=0,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
            )
        answer = request.choices[0].message.content
        print("!!!!!!!!from get_result_prompt !!!!!!!")
        print(massages)

        print(answer)
        return answer
        
    def graph(self,question,query,df_dict,table_schema,queryResult):

        prompt = """Task: Generate graph using pandas and plotly.
                    Context
                    Table schema {}
                    Input SQL query {}
                    Query result {}
                    Input question {}
                    Requirements
                    Handle empty results with "No data found."
                    Handle errors with "Try it another way." Example:
                    import pandas as pd
                    import plotly 
                    # ... (code to generate graph based on context)
                    """.format(table_schema, query, queryResult, question)


        request = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
                    stop=None,
        
        )
        python_code = request.choices[0].message.content
        final_graph= exec(python_code)
        return final_graph
    