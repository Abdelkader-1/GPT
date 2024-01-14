class history:
        def __init__(self,massagesql,massages):
                #messages to store the conversation
            self.sqlmessages = []
            self.massages=[]
        
        def add_messagesql(self,role, message):
                
                self.sqlmessages.append({"role": role, "content": message})

        def add_messages(self,role, message):
                
            self.massages.append({"role": role, "content": message})
        
        # process user prompt
        def process_user_querysql(self,prompt):

            user_prompt = (f"{prompt}")
            self.add_messagesql("user", user_prompt)
            self.add_message("user", user_prompt)


    
            