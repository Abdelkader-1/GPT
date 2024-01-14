import os
from dotenv import load_dotenv
from langchain.llms import openai
if __name__ == 'main':
    load_dotenv('.env') 
    llm = AzureOpenAI( model_name="gpt-35-turbo-instruct",deployment_name="gpt-35-turbo-instruct",temperature=0.2)
    input = 'what is the capital of egypt'
    output = llm(input)
    print(f'answer :'{output})