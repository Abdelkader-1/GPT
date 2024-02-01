import streamlit as st
import Db_authentication
with st.form(key='login Form'):
    st.subheader("Login Section")
    user = st.text_input("User Name")
    passWord = st.text_input("Password")
    server = st.text_input("Server")
    database = st.text_input("database")
    connect = st.form_submit_button('connect')
    auth = Db_authentication.Auth(user,passWord,server,database)
    #auth.read_credentials()
    df_dict,table_schema,engine = auth.schema_describtion()
    #connect = st.sidebar.button('connect')


if connect :#and df_dict and table_schema and engine:
    