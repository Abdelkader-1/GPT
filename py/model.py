from langchain_community.llms import AzureOpenAI
from langchain.llms import openai
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
import prompts

class models:
    def __init__(self, dp,question):
        self.dp = dp
        self.question = question
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
def generate_sql_query(dictionary, table_schema, text):
    prompt = """**Task:** Generate a concise SQL Server query using only function calls and parentheses.

    **Context:**
    - Available tables, columns, and data types: {}
    - Table schemas: {}

    **Requirements:**
    - **Translate natural language input:** Accurately convert the given text into a corresponding SQL query.
    - **Concise language:** Use only function calls and parentheses, omitting descriptive words.
    - **Example:** Replace "DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)" with "DATE_SUB(CURRENT_DATE(), 1)".
    - **Handle joins:** Identify and join necessary tables as required by the input text.
        Input: {} SQL Query (without descriptive words).
    """.format(dictionary, table_schema, text)

    request = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        stop=None,

    )
    global query
    query = request.choices[0].message.content
    return query



def executeSQLquery(df_dict,text,table_schema ,max_retries):
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            query = generate_sql_query(df_dict,text,table_schema)
            result = pd.read_sql(query,engine)
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"Retrying... (Attempt {retry_count}/{max_retries})")
            else:
                print("Max retry attempts reached. Exiting.")
                raise


def get_result_prompt(question, query, df_dict, table_schema, queryResult):

    prompt = """**Task:** Answer the input question in natural language based on the provided data.

    **Context:**
    - Table schemas: {}
    - Input SQL query (with potential joins): {}
    - Query result: {}
    - Input question: {}

    **Requirements:**
    - Generate a human-readable response that directly answers the question.
    - Avoid mentioning any SQL queries or table names in the response.
    - Handle empty results with "No data found."
    - Gracefully handle errors with "Try it in another way."

    **Example:**
    What were the total sales in January 2023?
    **Response:** The total sales in January 2023 were 123 million dollars.
    """.format(table_schema, query, queryResult, question)
    
    request = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stop=None,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )
    answer = request.choices[0].message.content
    answer
    return answer
        
