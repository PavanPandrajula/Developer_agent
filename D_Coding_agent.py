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

prompt = """ YOU ARE A CODING AGENT. YOU DEVELOP THE CODE BASED ON THE USER REQUIREMENTS AND THE PLANNING STEPS.
PROVIDE THE CODE IN ORGANISED MANNER.
DO NOT HALLUCINATE AND PROVIDE ANY HARMFUL CODE
IF THERE ARE MULTIPLE FILES PLACE THEM IN STRUCTURED ORDER AND PROVIDE A NEAT STRUCTED AND PROFESSIONAL CODE TO THE USER.
ALSO AT THE END OF THE CODE MAKE SURE YOU PROVIDE SOME EXPLAINATION TO THE USER."""

def get_response_D(sys_prompt):
    agent = create_agent(model = llm,
                        system_prompt = prompt,
                        name = "coding_agent")
    result = agent.invoke(
        {
            "messages" : [
                ("human", sys_prompt)
            ]
        }
    )
    raw_content = result["messages"][-1].text
    return raw_content

'''def get_response_D(sys_prompt: str):
    """Coding agent — Step 3"""
    agent = create_agent(
        model=llm,
        system_prompt=sys_prompt
    )
    def run(input: str) -> str:
        result = agent.invoke({"messages": [HumanMessage(content=input)]})
        return result["messages"][-1].text
    return run'''

