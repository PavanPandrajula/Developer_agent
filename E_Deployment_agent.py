from langchain.agents import create_agent
from deepagents import create_deep_agent
from langchain.tools import tool
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

prompt = """ YOU ARE A DEPLOYMENT AGENT. YOU PROVIDE THE CODE FOR DEPLOYING THE GIVEN CODE THROUGH VARIOUS APPROACHES SO THAT USER HAS A FLEXIBILITY FROM SELECTING ABOVE METHODS.
DO NOT HALLUCINATE AND PROVIDE A CLEAN STRUCTURED APPROACH.
EXPLAIN THE USER EACH AND EVERY STEP SO THAT THE USER IS NOT STUCK OR CONFUSED AT ANY STEP
BE PROFESSIONAL AND DONT DISCLOSE ANY PERSONAL INFORMATION."""


def get_response_E(sys_prompt):
    agent = create_agent(model = llm,
                        system_prompt = prompt,
                        name = "deployment_agent")
    result = agent.invoke(
        {
            "messages" : [
                ("human", sys_prompt)
            ]
        }
    )
    raw_content = result["messages"][-1].text
    return raw_content

'''def get_response_E(sys_prompt: str):
    """Deploy agent — Step 4"""
    agent = create_agent(
        model=llm,
        system_prompt=sys_prompt
    )
    def run(input: str) -> str:
        result = agent.invoke({"messages": [HumanMessage(content=input)]})
        return result["messages"][-1].text
    return run'''