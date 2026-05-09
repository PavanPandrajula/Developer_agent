# 🤖 Developer Agent

An AI-powered multi-agent pipeline that takes a plain-English software idea and automatically produces requirements, an execution plan, working code, and deployment instructions — all in one run.

---

## How It Works

When you describe what you want to build, a master **orchestrator agent** kicks off a sequential pipeline of four specialized sub-agents:

```
Your Query
    │
    ▼
[A] Orchestrator (Parent Agent)
    │
    ├─► [B] Requirements Agent   → Structured requirements doc
    │
    ├─► [C] Planning Agent       → Architecture & step-by-step plan
    │
    ├─► [D] Coding Agent         → Full working source code
    │
    └─► [E] Deployment Agent     → Deployment instructions & env setup
```

Each agent has a single, focused responsibility and passes its output to the next. No agent skips ahead or does another agent's job.

---

## Project Structure

| File | Role |
|------|------|
| `A_Parent_agent.py` | Orchestrator — wires all agents together and runs the pipeline |
| `B_Requirement_agent.py` | Gathers functional/non-functional requirements & acceptance criteria |
| `C_Planning_agent.py` | Converts requirements into an architecture overview and implementation steps |
| `D_Coding_agent.py` | Writes clean, commented code based on the plan |
| `E_Deployment_agent.py` | Packages the code and provides run/deploy instructions |
| `requirements.txt` | Python dependencies |

---

## Prerequisites

- Python 3.9+
- A running **Redis** instance (used for shared conversation memory across agents)
- A **Google AI API key** (the pipeline uses `gemini-3.1-flash-lite-preview`)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/PavanPandrajula/Developer_agent.git
cd Developer_agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Redis

```bash
redis-server
```

> Redis must be running at `localhost:6379` before you start the pipeline.

### 4. Set your API key

In `A_Parent_agent.py`, set your Google AI API key as an environment variable:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

Or add it directly in the script where indicated (`#DEFINE YOUR API KEYS HERE!!!`).

---

## Usage

Run the orchestrator:

```bash
python A_Parent_agent.py
```

You'll be prompted:

```
PLEASE PROVIDE YOUR QUERY...
```

Type a description of what you want to build, for example:

```
Build a REST API for a to-do app with user authentication and a PostgreSQL database.
```

The pipeline will then run all four agents sequentially, printing each agent's output to the console as it completes.

---

## Example Output Flow

```
PIPELINE STARTING !!!
==================================================
[Requirements Agent Output]
- Functional Requirements: ...
- Non-Functional Requirements: ...
==================================================

==================================================
[Planning Agent Output]
- Architecture overview: ...
- Implementation steps: ...
==================================================

==================================================
[Coding Agent Output]
- File structure: ...
- Source code: ...
==================================================

==================================================
[Deployment Agent Output]
- How to run: ...
- Environment variables needed: ...
==================================================

PIPELINE COMPLETE...
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `deepagents` | Deep agent orchestration framework |
| `langchain` | Core agent and tool abstractions |
| `langchain_community` | Redis chat message history |
| `langchain_classic` | Conversation buffer memory |
| `tavily-python` | Web search tool (available to agents) |
| `arxiv` | Research paper retrieval tool |
| `redis` | Shared memory backend |
| `rich` | Pretty console output |
| `dotenv` | Environment variable loading |

---

## Notes

- The pipeline is **strictly sequential** — each agent waits for the previous one to finish before starting.
- Conversation history is persisted in Redis under the session key `multi-agent-session`, so context is shared across all agents.
- If any agent fails, the pipeline stops and reports the error rather than continuing with incomplete input.
