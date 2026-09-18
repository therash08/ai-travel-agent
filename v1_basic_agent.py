import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled,Runner

# https://claude.ai/public/artifacts/21ada6a7-d6f8-4160-b3e1-8d33088a5f93

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME") 

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set BASE_URL, API_KEY, and MODEL_NAME."
    )
    

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)
    

agent = Agent(
    name="Assistant",  
    instructions="You are a helpful assistant", # Prompt -> Task 
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)
)

def main():
    result = Runner.run_sync(agent, "Write a joke about recursion in programming.")
    print(result.final_output)

if __name__ == "__main__":
    main()