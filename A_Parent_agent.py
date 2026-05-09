from langchain.agents import create_agent
from deepagents import create_deep_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_classic.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
import os
import redis

#DEFINE YOUR API KEYS HERE!!!

#starting redis server
r = redis.Redis(host='127.0.0.1', port=6379)

#MEMORY CREATION !!!
chat_history = RedisChatMessageHistory(
    session_id = "multi-agent-session",
    url = "redis://localhost:6379/0"
)

shared_memory = ConversationBufferMemory(
    chat_memory = chat_history,
    memory_key = "chat_history",
    return_messages = True
)


#PROMPTS FOR ALL THE AGENTS!!!
req_prompt = """
You are a requirements gathering agent.
Your ONLY job is to analyze the user query and produce a clear, structured 
requirements document.
Output format:
- Functional Requirements
- Non-Functional Requirements  
- Constraints
- Acceptance Criteria
Do NOT write any code. Do NOT make plans. ONLY gather requirements.
"""
planning_prompt = """
You are a planning agent.
You will receive a requirements document as input.
Your ONLY job is to convert it into a detailed step-by-step execution plan.
Output format:
- Architecture overview
- List of components to build
- Step-by-step implementation order
- Dependencies between steps
Do NOT write any code. ONLY produce the plan.
"""

coding_prompt = """
You are a coding agent.
You will receive an execution plan as input.
Your ONLY job is to write clean, working code that implements the plan exactly.
Output format:
- File structure
- Full source code for each file
- Inline comments explaining logic
Do NOT deploy. Do NOT plan. ONLY write the code.
"""

deploy_prompt = """
You are a deployment and delivery agent.
You will receive working code as input.
Your ONLY job is to:
1. Provide the final code clearly formatted
2. Provide step-by-step instructions to run/deploy it
3. List any environment variables or dependencies needed
Do NOT rewrite the code. ONLY package and explain the deployment steps.
"""

#ORCHESTRATION PROMPTS!!!
orchestrator_prompt = """ 
You are an orchestrator agent responsible for managing a software delivery pipeline.
You have access to 4 specialized sub-agents. You MUST call them in this exact order:

═══════════════════════════════════════════
PIPELINE ORDER (strictly sequential):
═══════════════════════════════════════════

STEP 1 → call: get_response_B
  - Purpose: Gather and clarify all requirements
  - Wait for its output before proceeding
  - Do NOT move to Step 2 until req_agent returns a requirements document
  - PRINT THE RESPONSE IN CONSOLE

STEP 2 → call: get_response_C
  - Purpose: Convert requirements into a structured execution plan
  - Input: Pass the FULL output from req_agent
  - Do NOT move to Step 3 until planning_agent returns a plan
  - PRINT THE RESPONSE IN CONSOLE

STEP 3 → call: get_response_D
  - Purpose: Write the code based on the plan
  - Input: Pass the FULL output from planning_agent
  - Do NOT move to Step 4 until coding_agent returns working code
  - PRINT THE RESPONSE IN CONSOLE

STEP 4 → call: get_response_E
  - Purpose: Provide me the code and steps
  - Input: Pass the FULL output from coding_agent
  - Once deploy_agent completes, summarize the entire pipeline result
  - PRINT THE RESPONSE IN CONSOLE

═══════════════════════════════════════════
STRICT RULES:
═══════════════════════════════════════════
1. NEVER skip a step or change the order
2. ALWAYS pass the previous agent's output as input to the next agent
3. If any agent fails or returns an error, STOP and report the failure — do not proceed
4. NEVER attempt to do the work of a sub-agent yourself
5. Your only job is to orchestrate, pass context, and summarize
6. DO NOT ASK ANYTHING TO THE USER JUST GIVE WHAT YOU CAN

"""

# DECLARING LLM!!!
llm = init_chat_model(model = "google_genai:gemini-3.1-flash-lite-preview",
                      api_key = os.getenv("GOOGLE_API_KEY"),
                      temperature = 0.1)

# REQUIREMENT ANALYSIS AGENT
req_agent = create_agent(model = llm,
                        system_prompt = req_prompt,
                        name = "requirement_agent")

# PLANNING AGENT
planning_agent = create_agent(model = llm,
                  system_prompt = planning_prompt,
                  name = "planning_agent")

# CODING AGENT
coding_agent = create_agent(model = llm,
                      system_prompt = coding_prompt,
                      name = "coding_agent")

#DEPLOY AGENT
deploy_agent = create_agent(model = llm,
                  system_prompt = deploy_prompt,
                  name = "deployment_agent")

#CORE AGENT!!!
core_agent = create_deep_agent(
    model = "google_genai:gemini-3.1-flash-lite-preview",
    memory = shared_memory,
    system_prompt = orchestrator_prompt,
    subagents= [
        {
            "name" : "req_agent",
            "description" : "handles software requirements",
            "graph" : req_agent,
            "model" : llm,
            "system_prompt" : req_prompt
        },
        {
            "name" : "planning_agent",
            "description" : "handles software development planning",
            "graph" : planning_agent,
            "model" : llm,
            "system_prompt" : planning_prompt
        },
        {
            "name" : "coding_agent",
            "description" : "develops code in structured manner",
            "graph" : coding_agent,
            "model" : llm,
            "system_prompt": coding_prompt
        },
        {
            "name" : "deploy_agent",
            "description" : "handles the deployment part",
            "graph" : deploy_agent,
            "model" : llm,
            "system_prompt" : deploy_prompt
        },
        {
            "name" : "Security_agent",
            "description" : ""
        }],
)

query = str(input("PLEASE PROVIDE YOUR QUERY..."))
print("PIPELINE STARTING !!!")
response = core_agent.invoke(
    {
        "messages": [
            ("human", query)
        ]
    }
)
print("PIPELINE COMPLETE...")
for message in response["messages"]:
    text = getattr(message, "content", None) or getattr(message, "text", None)
    if text:
        print(f"\n{'='*50}")
        print(text)
        print(f"{'='*50}\n")
print("PIPLELINE COMPLETE...")
print(response["messages"][-1].text)
