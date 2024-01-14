import Db_authentication
class history:
        def __init__(self):
                #messages to store the conversation
            auth = Db_authentication.Auth()
            auth.read_credentials()
            df_dict,table_schema,engine = auth.schema_describtion()

            self.sqlmessages = [{"role":"assistant",
                                 
                                 "content":
                                 """**Task:** Generate a concise SQL Server query using only function calls and parentheses.

                                **Context:**
                                - Available tables, columns, and data types: {}
                                - Table schemas: {}

                                **Requirements:**
                                - **Translate natural language input:** Accurately convert the given text into a corresponding SQL query.
                                - **Concise language:** Use only function calls and parentheses, omitting descriptive words.
                                - **Example:** Replace "DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)" with "DATE_SUB(CURRENT_DATE(), 1)".
                                - **Handle joins:** Identify and join necessary tables as required by the user content.""".format(df_dict, table_schema)
                                                        
                                                        }]
            

            self.massages=[{"role":"assistant",
                            
                            "content":
                            """
                            **Task:** Answer the input question in natural language based on the provided data.

                            **Requirements:**
                            - Generate a human-readable response that directly answers the question.
                            - Avoid mentioning any SQL queries or table names in the response.
                            - Handle empty results with "No data found."
                            - Gracefully handle errors with "Try it in another way."

                            **Example:**
                            What were the total sales in January 2023?
                            **Response:** The total sales in January 2023 were 123 million dollars
                            """
            }]
        
        def add_messagesql(self,role, message):
                
                self.sqlmessages.append({"role": role, "content": message})

        def add_messages(self,role, message):
                
            self.massages.append({"role": role, "content": message})
        
        # process user prompt
        def process_user_querysql(self,prompt):

            user_prompt = (f"{prompt}")
            self.add_messagesql("user", user_prompt)
            self.add_message("user", user_prompt)


    
            