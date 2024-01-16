import openai
import os
import streamlit as st
from streamlit_chat import message
import os
import Db_authentication
import model
import history
import pyodbc
import plotly.graph_objects as go  
import graphviz as graphviz


os.environ['OPENAI_API_BASE'] = 'https://like-card-test.openai.azure.com/'
os.environ['OPENAI_API_KEY'] = '85889c7998dd4adb9a4c89abe56b1242'
auth = Db_authentication.Auth()
auth.read_credentials()
models = model.models()
history=history.history()
massages=history.massages
sqlmessages=history.sqlmessages
df_dict,table_schema,engine = auth.schema_describtion()
st.set_page_config(page_title="Custom ChatGPT")

st.markdown("<h1 style='text-align: center;'>Your ABI Assistant 😬</h1>", unsafe_allow_html=True)

# Configure Azure OpenAI Service API
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'generatedadv' not in st.session_state:
    st.session_state['generatedadv'] = []

if 'generatedGraph' not in st.session_state:
    st.session_state['generatedGraph'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Sidebar")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-35-turbo"
else:
    model = "gpt-4"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['generatedadv'] = []
    st.session_state['generatedGraph'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")


# generate a response
def generate_response(text):
    st.session_state['messages'].append(massages)    
    #text = input("Enter your question: ")
    user_prompt=f"{text}"
    history.add_messages("user", user_prompt)
    history.add_messagesql("user", user_prompt)
        #history.process_user_querysql(text)
        #text = "what is the top 5 products and their amount"

    result,query,total_tokens1,prompt_tokens1,completion_tokens1 = models.executeSQLquery(df_dict, text, table_schema, engine, 5,sqlmessages)
    history.add_messagesql("assistant", f"{query}")
    history.add_messages("user", f"{result}")
    answer,total_tokens2,prompt_tokens2,completion_tokens2= models.get_result_prompt(text, df_dict, table_schema, result,massages)
    advice = models.Business_advisor(answer,table_schema,text)
    graph = graphviz.Digraph()
    graph = models.graph(text,query,df_dict,table_schema,result)
    print(graph)
    #final_graph= exec(python_code)
    history.add_messages("assistant", f"{answer}")

    response = answer
    st.session_state['messages'].append({"role": "assistant", "content": response})
    st.session_state['messages'].append({"role": "assistant", "content": advice})

    # print(st.session_state['messages'])
    total_tokens = total_tokens1+total_tokens2
    prompt_tokens = prompt_tokens1+prompt_tokens2
    completion_tokens = completion_tokens1+completion_tokens2

    #fig = go.Figure(data=df)  # Assuming `graph` has a `data` attribute
    #st.session_state["generatedGraph"].append(fig)
    
    return response,advice,graph, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output,advice,graph, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['generatedadv'].append(advice)
        st.session_state['generatedGraph'].append(graph)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["generatedadv"][i], key=str(i)+ '_advice')
            st.graphviz_chart(graph)


            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")