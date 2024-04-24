from langchain.agents import create_sql_agent 
from langchain_community.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.agents import AgentExecutor 
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import streamlit as st 

load_dotenv()
pg_uri = os.environ["POSTGRES_CONNECTION_STRING"]


st.set_page_config(page_title="Talk to your estate agent")
st.header("Talk to your estate agent")

db = SQLDatabase.from_uri(pg_uri)

gpt = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
toolkit = SQLDatabaseToolkit(db=db, llm=gpt)
agent_executor = create_sql_agent(
    llm=gpt,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# question = "the url of the latest rental house in New Malden"
# agent_executor.run(question)



user_question = st.text_input("Ask a question about property for sale or rent:")

if user_question is not None and user_question != "":
    with st.spinner(text="In progress..."):
        response = agent_executor.run(user_question)
        st.write(response["output"])
