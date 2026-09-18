import os
import json
import asyncio
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled,Runner

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
    
# --- Models for structured outputs ---
class TravelPlan(BaseModel):
    destination: str
    duration_days: int
    budget: float
    activities: List[str] = Field(description="List of recommended activities")
    notes: str = Field(description="Additional notes or recommendations")

# --- Main Travel Agent ---

travel_agent = Agent(
    name="Travel Planner", ## Name
    instructions=""" 
    You are a comprehensive travel planning assistant that helps users plan their perfect trip.
    
    You can create personalized travel itineraries based on the user's interests and preferences.
    
    Always be helpful, informative, and enthusiastic about travel. Provide specific recommendations
    based on the user's interests and preferences.
    
    When creating travel plans, consider:
    - Local attractions and activities
    - Budget constraints
    - Travel duration
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=TravelPlan
)

# --- Main Function ---

async def main():
    # Example queries to test the system
    queries = [
        # "I'm planning a trip to Miami for 5 days with a budget of $2000. What should I do there?",
        # "I want to visit Tokyo for a week with a budget of $3000. What activities do you recommend?"
        "I want to visit Cox's Bazar for a 2 days with a budget of 10000 taka. What activities do you recommend?"
    ]
    
    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")
        
        result = await Runner.run(travel_agent, query)
        
        print("\nFINAL RESPONSE:")
        travel_plan = result.final_output
        
        
        print(json.dumps(json.loads(travel_plan.model_dump_json()), indent=2))
        
        # Format the output in a nicer way
        print(f"\n🌍 TRAVEL PLAN FOR {travel_plan.destination.upper()} 🌍")
        print(f"Duration: {travel_plan.duration_days} days")
        print(f"Budget: ${travel_plan.budget}")
        
        print("\n🎯 RECOMMENDED ACTIVITIES:")
        for i, activity in enumerate(travel_plan.activities, 1):
            print(f"  {i}. {activity}")
        
        print(f"\n📝 NOTES: {travel_plan.notes}")

if __name__ == "__main__":
    asyncio.run(main())