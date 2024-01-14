import os
import openai
class conn:
   def __init__(self):
       self.set_environment_variables()

   def set_environment_variables(self):
       os.environ["OPENAI_API_TYPE"] = "azure"
       os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"
       os.environ["OPENAI_API_BASE"] = "https://like-card-test.openai.azure.com/"
       os.environ["OPENAI_API_KEY"] = "85889c7998dd4adb9a4c89abe56b1242"
       os.environ["OPENAI_API_ENDPOINT"] = "https://like-card-test.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-07-01-preview"

   def set_openai_environment_variables(self):
       openai.api_type = "azure"
       openai.api_version = "2023-07-01-preview"
       openai.api_base = "https://like-card-test.openai.azure.com/"
       openai.api_key = "85889c7998dd4adb9a4c89abe56b1242"
       openai.azure_endpoint = "https://like-card-test.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-07-01-preview"
