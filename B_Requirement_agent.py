from langchain_classic.agents import create_tool_calling_agent
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.memory import ConversationBufferMemory
import os
from rich.console import Console
from rich.markdown import Markdown
from langchain.messages import HumanMessage

#DEFINE YOUR API KEYS HERE!!!

llm = init_chat_model(model = "google_genai:gemini-3.1-flash-lite-preview",
                      api_key = os.getenv("GOOGLE_API_KEY"),
                      temperature = 0.1)

prompt = """ YOU ARE REQUIREMENT ANALYSIS AGENT. YOU PROVIDE THE REQUIREMENTS FOR THE USER BASED ON THE PROJECT THE USER HAS DEFINED.
PLEASE PROVIDE THE RESPONSES IN A STRUCTURED AND PROFESSIONAL MANNER.
DO NO DISCLOSE ANY PERSOAL INFORMATION AND NO HATE COMMENTS
DO NOT HALLUCINATE, IF YOU DONT KNOW ANYTHING PLEASE INFORM THAT YOU DONT KNOW."""

def get_response_B(sys_prompt):
    agent = create_agent(model = llm,
                        system_prompt = prompt,
                        name = "requirement_agent")
    result = agent.invoke(
        {
            "messages" : [
                ("human", sys_prompt)
            ]
        }
    )
    raw_content = result["messages"][-1].text
    return raw_content

'''def get_response_B(sys_prompt: str):
    """Requirements agent — Step 1"""
    agent = create_agent(
        model=llm,
        system_prompt=sys_prompt
    )
    def run(input: str) -> str:
        result = agent.invoke({"messages": [HumanMessage(content=input)]})
        return result["messages"][-1].text
    return run'''
