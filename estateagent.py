from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.llms.openai import OpenAI 
from langchain.agents import AgentExecutor 
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
pg_uri = f"postgresql+psycopg2://postgres:90909090@localhost:5432/Properties"

db = SQLDatabase.from_uri(pg_uri)

gpt = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
toolkit = SQLDatabaseToolkit(db=db, llm=gpt)
agent_executor = create_sql_agent(
    llm=gpt,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

question = "the url of the latest rental house in New Malden"
agent_executor.run(question)