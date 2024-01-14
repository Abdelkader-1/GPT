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
    def sqlModel(self):    
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