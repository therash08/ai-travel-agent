import os
import asyncio
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled, ModelSettings,Runner

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

class TravelPlan(BaseModel):
    destination: str
    duration_days: int
    budget: float
    activities: List[str] = Field(description="List of recommended activities")
    notes: str = Field(description="Additional notes or recommendations")

@function_tool
def get_predicted_travel_cost(city: str , activity: list[str]):
    """Get the predicted travel cost for a city and activity."""
    travel_cost = {
        "New York": 1000,
        "Los Angeles": 1500,
        "Chicago": 1200,
    }
    return f"The predicted travel cost for {city} and {activity} is {travel_cost.get(city, 1000)}."

@function_tool
def get_weather_forecast(city: str, date: str) -> str:
    """Get the weather forecast for a city on a specific date."""
    weather_data = {
        "New York": {"sunny": 0.3, "rainy": 0.4, "cloudy": 0.3},
        "Los Angeles": {"sunny": 0.8, "rainy": 0.1, "cloudy": 0.1},
        "Chicago": {"sunny": 0.4, "rainy": 0.3, "cloudy": 0.3},
        "Miami": {"sunny": 0.7, "rainy": 0.2, "cloudy": 0.1},
        "London": {"sunny": 0.2, "rainy": 0.5, "cloudy": 0.3},
        "Paris": {"sunny": 0.4, "rainy": 0.3, "cloudy": 0.3},
        "Tokyo": {"sunny": 0.5, "rainy": 0.3, "cloudy": 0.2},
    }
    
    if city in weather_data:
        conditions = weather_data[city]
        highest_prob = max(conditions, key=conditions.get)
        temp_range = {
            "New York": "15-25°C",
            "Los Angeles": "20-30°C",
            "Chicago": "10-20°C",
            "Miami": "25-35°C",
            "London": "10-18°C",
            "Paris": "12-22°C",
            "Tokyo": "15-25°C",
        }
        return f"The weather in {city} on {date} is forecasted to be {highest_prob} with temperatures around {temp_range.get(city, '15-25°C')}."
    else:
        return f"Weather forecast for {city} is not available."


travel_agent = Agent(
    name="Travel Planner",
    instructions="""
    You are a comprehensive travel planning assistant that helps users plan their perfect trip.
    
    You can create personalized travel itineraries based on the user's interests and preferences.
    
    Always be helpful, informative, and enthusiastic about travel. Provide specific recommendations
    based on the user's interests and preferences.
    You can 2 tools to help you with your task:
    
    1. get_weather_forecast to get the weather forecast for a city
    2. get_predicted_travel_cost to get the predicted travel cost for a city and activity
    
    When creating travel plans, consider:
    - The weather at the destination
    - Local attractions and activities
    - Budget constraints
    - Travel duration
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[get_weather_forecast, get_predicted_travel_cost]
    # No output_type: combining `tools` with strict `output_type` in one
    # request breaks on Groq/vLLM/Gemini. Structured output runs as a
    # separate pass below instead.
)

structured_output_agent = Agent(
    name="Structured Output Formatter",
    instructions="Extract a TravelPlan (destination, duration_days, budget, activities, notes) from the text.",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=TravelPlan,
    model_settings=ModelSettings(max_tokens=4096),
)


async def main():
    queries = [
        "I'm planning a trip to Miami for 5 days with a budget of $2000. What should I do there and what is the weather going to look like?",
    ]

    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")

        result = await Runner.run(travel_agent, query)
        structured = await Runner.run(structured_output_agent, result.final_output)
        travel_plan = structured.final_output

        print(f"\n🌍 TRAVEL PLAN FOR {travel_plan.destination.upper()} 🌍")
        print(f"Duration: {travel_plan.duration_days} days")
        print(f"Budget: ${travel_plan.budget}")

        print("\n🎯 RECOMMENDED ACTIVITIES:")
        for i, activity in enumerate(travel_plan.activities, 1):
            print(f"  {i}. {activity}")

        print(f"\n📝 NOTES: {travel_plan.notes}")

if __name__ == "__main__":
    asyncio.run(main())