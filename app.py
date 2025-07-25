import sqlite3
from pathlib import Path

import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy import create_engine

st.set_page_config(page_title="EcommerceIQ", page_icon="🤖")
st.title("EcommerceIQ: AI Agent to Answer E-commerce Data Questions")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["Use SQLLite 3 Database- sales_analysis.db","Connect to you MySQL Database"]

selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide MySQL Host")
    mysql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL password",type="password")
    mysql_db=st.sidebar.text_input("MySQL database")
else:
    db_uri=LOCALDB

api_key=st.sidebar.text_input(label="Gemini API Key",type="password")

if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please add the gemini api key")
    st.stop()  # Stop execution until API key is provided

## LLM model - only create if API key is provided
# llm=ChatGoogleGenerativeAI(google_api_key=api_key,model="gemini-pro",streaming=True)
try:
    import asyncio
    import threading
    
    def create_llm():
        # Create a new event loop for this thread if one doesn't exist
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model="gemini-1.5-flash",
            streaming=False,
            convert_system_message_to_human=True
        )
    
    llm = create_llm()
    
except Exception as e:
    st.error(f"Error initializing Gemini LLM: {str(e)}")
    st.info("Falling back to a different LLM or check your API key.")
    st.stop()

@st.cache_resource(ttl="2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"sales_analysis.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        
        # Fix: URL encode the password to handle special characters
        from urllib.parse import quote_plus
        encoded_password = quote_plus(mysql_password)
        connection_string = f"mysql+mysqlconnector://{mysql_user}:{encoded_password}@{mysql_host}/{mysql_db}"
        
        try:
            engine = create_engine(connection_string)
            # Test the connection with proper SQLAlchemy 2.0 syntax
            with engine.connect() as conn:
                from sqlalchemy import text
                conn.execute(text("SELECT 1"))
            return SQLDatabase(engine)
        except Exception as e:
            st.error(f"Failed to connect to MySQL database: {str(e)}")
            st.info("Please check your connection details:")
            st.info(f"Host: {mysql_host}")
            st.info(f"User: {mysql_user}")
            st.info(f"Database: {mysql_db}")
            st.info("Make sure MySQL server is running and credentials are correct.")
            st.stop()

# Only proceed if we have an API key
if api_key:
    if db_uri==MYSQL:
        db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
    else:
        db=configure_db(db_uri)

    ## toolkit
    toolkit=SQLDatabaseToolkit(db=db,llm=llm)

    agent=create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_query=st.chat_input(placeholder="Ask anything from the database")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        with st.chat_message("assistant"):
            streamlit_callback=StreamlitCallbackHandler(st.container())
            response=agent.run(user_query,callbacks=[streamlit_callback])
            st.session_state.messages.append({"role":"assistant","content":response})
            st.write(response)