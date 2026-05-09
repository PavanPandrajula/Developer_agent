from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
import os
from rich.console import Console
from rich.markdown import Markdown
from langchain.messages import HumanMessage


#DEFINE YOUR API KEYS HERE!!!

llm = init_chat_model(model = "google_genai:gemini-3.1-flash-lite-preview",
                      api_key = os.getenv("GOOGLE_API_KEY"),
                      temperature = 0.1,
                      max_retries = 3)

prompt = """ YOU ARE PLANNING AGENT. YOU PLAN THE STEPS TO BE FOLLOWED BASED TO DEVELOP THE PROJECT.
ASSIGN/DEFINE THE STEPS IN CLEAR MANNER
DO NO HALLUCINATE AND PROVIDE THE INFORMATION IN PROFESSIONAL MANNER
DO NOT DISCLOSE ANY PEROSNAL INFORMATION
"""
def get_response_C(sys_prompt):
    agent = create_agent(model = llm,
                        system_prompt = prompt,
                        name = "planning_agent")
    result = agent.invoke(
        {
            "messages" : [
                ("human", sys_prompt)
            ]
        }
    )
    raw_content = result["messages"][-1].text
    return raw_content

'''def get_response_C(sys_prompt: str):
    """Planning agent — Step 2"""
    agent = create_agent(
        model=llm,
        system_prompt=sys_prompt
    )
    def run(input: str) -> str:
        result = agent.invoke({"messages": [HumanMessage(content=input)]})
        return result["messages"][-1].text
    return run'''