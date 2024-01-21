from langchain_community.llms import AzureOpenAI
#from langchain.llms import openai
import openai
#from langchain.memory import ConversationBufferMemory
#from langchain.agents.agent_toolkits import SQLDatabaseToolkit
#from langchain.agents import create_sql_agent
#import prompts
import pandas as pd
#import history
import streamlit as st


class models:
    def __init__(self):
        self.dp = None
        self.question = None
    '''
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
        '''

    query = None
    def generate_sql_query(self,dictionary, table_schema, text,sqlmessages):
               
        request = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages= st.session_state['histsqlmassages'],
            stop=None,
        )
        global query
        query = request.choices[0].message.content
        print("from generate sql query")
        print(sqlmessages)
        total_tokens = request.usage.total_tokens
        prompt_tokens = request.usage.prompt_tokens
        completion_tokens = request.usage.completion_tokens
        return query,total_tokens,prompt_tokens,completion_tokens


    def executeSQLquery(self,df_dict,text,table_schema,engine,max_retries,sqlmessages):
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                query,total_tokens,prompt_tokens,completion_tokens = self.generate_sql_query(df_dict,text,table_schema,sqlmessages)
                result = pd.read_sql(query,engine)
                print("!!!!!!!!from executeSQLquery !!!!!!!")
                print(query)
                print(result)
                return result,query,total_tokens,prompt_tokens,completion_tokens
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
                messages= st.session_state['histmassages'],
                stop=None,
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
            )
        answer = request.choices[0].message.content
        total_tokens = request.usage.total_tokens
        prompt_tokens = request.usage.prompt_tokens
        completion_tokens = request.usage.completion_tokens
        print("!!!!!!!!from get_result_prompt !!!!!!!")
        print(massages)

        print(answer)
        return answer,total_tokens,prompt_tokens,completion_tokens
    
    
    def Business_advisor(self,answer,table_schema,question):
        prompt = """
                 You are a business consultant
                 Task: Give a business advice based on answer {}
                 Context:
                 Input question {}
                    """.format(answer,table_schema,question)
        request = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
                    stop=None,
                    temperature=0.5,
        
        )
        advice = request.choices[0].message.content
        print(advice)
        return advice
    global fig
    def graph(self,question,data):

        prompt = """Task: Generate a graph for the provided data using plotly.express as px .
                    Context
                    Input question {}
                    Data to plot {}
                    Requirements
                    make a function and return fig, store it in a variable called fig
                    don't try to display the fig
                    Handle empty data with None
                    Handle errors with None 
                    don't write any descrpition inside the function only code because i will call the function to use it later
                    Example:
                    import plotly.express as px
                    import pandas as pd
                    def generate_graph(data):
                    ---
                    ---
                    ---  columns = list(data.columns)
                    ---  fig = px.bar(data, x=columns[0], y = columns[1]) or any other suitable graph                    
                    return fig
                    """.format(question,data)


        request = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
                    stop=None,
        
        )
        
        python_code = request.choices[0].message.content
        print("python_code: ",python_code)
        function_fig = {}
        exec(python_code,globals())
        function_fig['generate_graph'] = globals()['generate_graph']
        # Now you can use the function from the dictionary
        fig=function_fig['generate_graph'](data)
        #print("result: ",fig)
        return fig
    