import Db_authentication
class history:
        def __init__(self):
                #messages to store the conversation
            auth = Db_authentication.Auth()
            auth.read_credentials()
            df_dict,table_schema,engine = auth.schema_describtion()

            self.sqlmessages = [{"role":"assistant",
                                 
                                 "content":
                                 """Task
                                 Generate a concise SQL Server query
                                 Context
                                 Available tables, columns and data types {}
                                 Table schemas {}
                                 Requirements
                                 use the correct columns names
                                 Accurately translate natural language input into SQL query.
                                 Use only function calls and parentheses (no descriptive words).
                                 Utilize SQLAlchemy supported functions and librarysales.
                                 Handle joins as required by user content.""".format(df_dict, table_schema)
                                                        
                                                        }]
            


            self.massages=[{"role":"assistant",
                            
                            "content":
                            """Task: Answer natural language questions using provided data.
                            Requirements:
                            Human-readable, direct answers.
                            Avoid technical terms.
                            output in table
                            Handle empty results with "No data found."
                            Handle errors with "Try it another way."
                            Example:
                            Question: "Total sales January 2023?"
                            Response: "123,456,789 million dollars."
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


    
            