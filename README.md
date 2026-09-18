# AI Travel Agent — OpenAI Agents SDK Demo

An AI-powered travel planning assistant built with Python and the OpenAI Agents SDK.

This project demonstrates how to build AI agents step by step, starting from a basic agent and gradually adding structured outputs, tool calling, agent handoffs, guardrails, user context, conversation memory, and a Streamlit web interface.

---

## Project Structure

```text
ai-travel-agent/
│
├── v1_basic_agent.py
├── v2_structured_output.py
├── v3_tool_calls.py
├── v4_handoffs.py
├── v5_guardrails_and_context.py
├── v6_streamlit_agent.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### Files

| File | Description |
|---|---|
| `v1_basic_agent.py` | Basic agent example demonstrating agent configuration and execution |
| `v2_structured_output.py` | Travel agent with structured output using Pydantic models |
| `v3_tool_calls.py` | Travel agent with tool calling for weather forecasting |
| `v4_handoffs.py` | Travel agent with specialized sub-agents for flights and hotels |
| `v5_guardrails_and_context.py` | Travel agent with budget guardrails and user context |
| `v6_streamlit_agent.py` | Streamlit web interface with chat memory and user preferences |

---

## Features

This project demonstrates:

- Basic AI agent configuration
- OpenAI Agents SDK
- Structured output with Pydantic
- Custom tool calling
- Weather forecasting tools
- Agent handoffs
- Specialized flight and hotel agents
- Budget guardrails
- User context and preferences
- Conversation memory
- Multi-turn conversations
- Streamlit web interface
- Optional Logfire tracing

---

## Agent Development Progression

```text
Basic Agent
    ↓
Structured Output
    ↓
Tool Calling
    ↓
Agent Handoffs
    ↓
Guardrails + Context
    ↓
Streamlit Chat Application
```

Each version introduces new capabilities and builds on the concepts demonstrated in the previous version.

---

## Requirements

Make sure Python is installed on your computer.

Recommended:

```text
Python 3.10+
```

Check your Python version:

```bash
python --version
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/therash08/ai-travel-agent.git
```

Go inside the project folder:

```bash
cd ai-travel-agent
```

---

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory of the project.

Add:

```env
BASE_URL="https://models.github.ai/inference/v1"
API_KEY="your_api_key_here"
MODEL_NAME="openai/gpt-4.1-nano"
```

Replace:

```text
your_api_key_here
```

with your actual API key.

### Important

Never upload your API key to GitHub.

The `.env` file should be included in `.gitignore`.

---

## .gitignore

Create a `.gitignore` file and add:

```gitignore
# Environment variables
.env

# Virtual environment
venv/
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# VS Code
.vscode/

# Operating system files
.DS_Store
Thumbs.db

# Log files
*.log
```

---

# Running the Examples

## V1 — Basic Agent

Run:

```bash
python v1_basic_agent.py
```

This version demonstrates the basic configuration and execution of an AI agent.

It is a simple introduction to how agents work before moving into the travel planning features.

---

## V2 — Structured Output Agent

Run:

```bash
python v2_structured_output.py
```

This version demonstrates structured outputs using Pydantic models.

Instead of returning only plain text, the agent can organize travel information into structured fields such as:

- Destination
- Activities
- Budget
- Travel recommendations

---

## V3 — Tool Calling Agent

Run:

```bash
python v3_tool_calls.py
```

This version introduces custom tool calling.

The travel agent can call a weather forecasting tool when weather information is needed for a destination.

This demonstrates how AI agents can use external functions and tools to complete tasks.

---

## V4 — Agent Handoffs

Run:

```bash
python v4_handoffs.py
```

This version introduces multiple specialized agents.

The main travel agent can hand off tasks to specialized sub-agents.

Examples include:

- Flight Agent
- Hotel Agent

The flight agent handles flight-related requests, while the hotel agent handles accommodation-related requests.

This demonstrates multi-agent collaboration using the OpenAI Agents SDK.

---

## V5 — Guardrails and Context

Run:

```bash
python v5_guardrails_and_context.py
```

This version adds guardrails and user context.

### Budget Guardrails

The agent checks whether the user's travel budget is realistic for the requested trip.

### User Context

The agent can use user preferences such as:

- Preferred airlines
- Hotel preferences
- Hotel amenities
- Travel preferences

This allows the agent to generate more personalized travel recommendations.

---

## Optional Logfire Tracing

Logfire can be used to monitor and trace agent execution.

More information:

https://logfire.pydantic.dev/docs/

The project will still work without Logfire configured, but tracing information will not be available.

---

# V6 — Streamlit Travel Assistant

Run:

```bash
streamlit run v6_streamlit_agent.py
```

After running the command, Streamlit will start a local web server.

A browser window should open automatically.

Usually, the application will be available at:

```text
http://localhost:8501
```

---

## Streamlit Application Features

The Streamlit version includes:

- Interactive chat interface
- Travel planning assistant
- Conversation history
- Multi-turn conversations
- Session-based memory
- User preference management
- Flight recommendations
- Hotel recommendations
- Weather information
- Budget checking
- Specialized agent handoffs
- Formatted travel responses

---

# Technologies Used

This project uses:

- Python
- OpenAI Agents SDK
- Pydantic
- Streamlit
- Python-dotenv
- Pydantic Logfire

---

# How the System Works

The project gradually develops a simple agent into a more advanced travel planning system.

```text
User
  │
  ▼
Travel Agent
  │
  ├── Weather Tool
  │
  ├── Flight Agent
  │
  ├── Hotel Agent
  │
  ├── Budget Guardrail
  │
  └── User Context
  │
  ▼
Travel Recommendation
```

The travel agent receives a request from the user and determines what information or specialized agent is required.

It can use tools, hand off tasks to other agents, check budget requirements, and use stored user preferences before generating the final response.

---

# Example Use Cases

Users can ask questions such as:

```text
Plan a 5-day trip to Tokyo with a budget of $1500.
```

```text
Suggest hotels in Dubai for my vacation.
```

```text
What will the weather be like during my trip?
```

```text
Find suitable flight and hotel options for my trip.
```

```text
Plan a budget-friendly vacation for me.
```

The agent processes the request and uses the appropriate tools or specialized agents.

---

# Development Versions

### Version 1

Basic agent configuration and execution.

### Version 2

Structured output using Pydantic.

### Version 3

Custom tool calling for weather information.

### Version 4

Multi-agent system using agent handoffs.

### Version 5

Budget guardrails and personalized user context.

### Version 6

Complete Streamlit chat interface with conversation memory.

---

# Simulated Data

This project is primarily created for learning and demonstration purposes.

Some information related to:

- Weather
- Flights
- Hotels

may use simulated or demonstration data.

For a real production travel application, these tools should be connected to real APIs.

Examples could include:

- Weather APIs
- Airline APIs
- Hotel APIs
- Maps APIs
- Travel booking APIs

---

# Security

Do not expose API keys publicly.

Never commit the following file:

```text
.env
```

Make sure `.env` is included in `.gitignore`.

Before pushing to GitHub, you can check your files using:

```bash
git status
```

---

# Running the Full Application

For the final Streamlit version:

```bash
streamlit run v6_streamlit_agent.py
```

Then open:

```text
http://localhost:8501
```

in your browser if it does not open automatically.

---

# Purpose of the Project

The purpose of this project is to learn and demonstrate agentic AI development using the OpenAI Agents SDK.

The project shows how a basic AI agent can gradually evolve into a more advanced travel assistant capable of:

- Using tools
- Returning structured outputs
- Working with multiple agents
- Applying guardrails
- Remembering user context
- Handling conversations
- Running through a web interface

---

# Future Improvements

Possible future improvements include:

- Real-time weather API integration
- Real flight search API
- Real hotel booking API
- Google Maps integration
- Destination recommendations
- Travel cost calculation
- Currency conversion
- Database-based chat history
- User authentication
- Deployment to the cloud
- Real-time itinerary generation

---

# Disclaimer

This project is intended for educational and demonstration purposes.

Travel, weather, flight, hotel, and pricing information generated by the application should not be considered real-time booking information unless connected to verified external APIs.

---

# AI Travel Agent

Built as a learning project to explore the OpenAI Agents SDK and modern agentic AI development.