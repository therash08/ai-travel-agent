import os
import json
import asyncio
from typing import List, Optional
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

class FlightRecommendation(BaseModel):
    airline: str
    departure_time: str
    arrival_time: str
    price: float
    direct_flight: bool
    recommendation_reason: str

class HotelRecommendation(BaseModel):
    name: str
    location: str
    price_per_night: float
    amenities: List[str]
    recommendation_reason: str

class TravelPlan(BaseModel):
    destination: str
    duration_days: int
    budget: float
    activities: List[str] = Field(description="List of recommended activities")
    notes: str = Field(description="Additional notes or recommendations")

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


@function_tool
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for flights between two cities on a specific date."""
    flight_options = [
        {
            "airline": "SkyWays",
            "departure_time": "08:00",
            "arrival_time": "10:30",
            "price": 350.00,
            "direct": True
        },
        {
            "airline": "OceanAir",
            "departure_time": "12:45",
            "arrival_time": "15:15",
            "price": 275.50,
            "direct": True
        },
        {
            "airline": "MountainJet",
            "departure_time": "16:30",
            "arrival_time": "21:45",
            "price": 225.75,
            "direct": False
        }
    ]
    
    return json.dumps(flight_options)

@function_tool
def search_hotels(city: str, check_in: str, check_out: str, max_price: Optional[float] = None) -> str:
    """Search for hotels in a city for specific dates within a price range."""
    hotel_options = [
        {
            "name": "City Center Hotel",
            "location": "Downtown",
            "price_per_night": 199.99,
            "amenities": ["WiFi", "Pool", "Gym", "Restaurant"]
        },
        {
            "name": "Riverside Inn",
            "location": "Riverside District",
            "price_per_night": 149.50,
            "amenities": ["WiFi", "Free Breakfast", "Parking"]
        },
        {
            "name": "Luxury Palace",
            "location": "Historic District",
            "price_per_night": 349.99,
            "amenities": ["WiFi", "Pool", "Spa", "Fine Dining", "Concierge"]
        }
    ]

    if max_price is not None:
        filtered_hotels = [hotel for hotel in hotel_options if hotel["price_per_night"] <= max_price]
    else:
        filtered_hotels = hotel_options

    return json.dumps(filtered_hotels)


flight_agent = Agent(
    name="Flight Specialist",
    handoff_description="Specialist agent for finding and recommending flights",
    instructions="""
    You are a flight specialist who helps users find the best flights for their trips.
    
    Use the search_flights tool to find flight options, and then provide personalized recommendations
    based on the user's preferences (price, time, direct vs. connecting).
    
    Always explain the reasoning behind your recommendations.
    
    Format your response in a clear, organized way with flight details and prices.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[search_flights]
)

hotel_agent = Agent(
    name="Hotel Specialist",
    handoff_description="Specialist agent for finding and recommending hotels and accommodations",
    instructions="""
    You are a hotel specialist who helps users find the best accommodations for their trips.
    
    Use the search_hotels tool to find hotel options, and then provide personalized recommendations
    based on the user's preferences (location, price, amenities).
    
    Always explain the reasoning behind your recommendations.
    
    Format your response in a clear, organized way with hotel details, amenities, and prices.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[search_hotels]
)

travel_agent = Agent(
    name="Travel Planner",
    instructions="""
    You are a comprehensive travel planning assistant that helps users plan their perfect trip.
    
    You can:
    1. Provide weather information for destinations
    2. Create personalized travel itineraries
    3. Hand off to specialists for flights and hotels when needed
    
    Always be helpful, informative, and enthusiastic about travel. Provide specific recommendations
    based on the user's interests and preferences.
    
    When creating travel plans, consider:
    - The weather at the destination
    - Local attractions and activities
    - Budget constraints
    - Travel duration
    
    If the user asks specifically about flights or hotels, hand off to the appropriate specialist agent.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[get_weather_forecast],
    handoffs=[flight_agent, hotel_agent]
)

FORMATTER_SETTINGS = ModelSettings(max_tokens=4096)

flight_formatter = Agent(
    name="Flight Formatter",
    instructions="Extract a FlightRecommendation (airline, departure_time, arrival_time, price, direct_flight, recommendation_reason) from the text.",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=FlightRecommendation,
    model_settings=FORMATTER_SETTINGS,
)

hotel_formatter = Agent(
    name="Hotel Formatter",
    instructions="Extract a HotelRecommendation (name, location, price_per_night, amenities, recommendation_reason) from the text.",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=HotelRecommendation,
    model_settings=FORMATTER_SETTINGS,
)

travel_formatter = Agent(
    name="Travel Plan Formatter",
    instructions="Extract a TravelPlan (destination, duration_days, budget, activities, notes) from the text.",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=TravelPlan,
    model_settings=FORMATTER_SETTINGS,
)

FORMATTERS = {
    "Flight Specialist": flight_formatter,
    "Hotel Specialist": hotel_formatter,
    "Travel Planner": travel_formatter,
}


async def main():
    queries = [
       "I need a flight from New York to Chicago tomorrow",
    ]

    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")

        result = await Runner.run(travel_agent, query)
        handled_by = result.last_agent.name
        print(f"\nHANDLED BY: {handled_by}")

        structured = await Runner.run(FORMATTERS[handled_by], result.final_output)
        output = structured.final_output

        if isinstance(output, FlightRecommendation):
            print("\n✈️ FLIGHT RECOMMENDATION ✈️")
            print(f"Airline: {output.airline}")
            print(f"Departure: {output.departure_time}")
            print(f"Arrival: {output.arrival_time}")
            print(f"Price: ${output.price}")
            print(f"Direct Flight: {'Yes' if output.direct_flight else 'No'}")
            print(f"\nWhy this flight: {output.recommendation_reason}")

        elif isinstance(output, HotelRecommendation):
            print("\n🏨 HOTEL RECOMMENDATION 🏨")
            print(f"Name: {output.name}")
            print(f"Location: {output.location}")
            print(f"Price per night: ${output.price_per_night}")

            print("\nAmenities:")
            for i, amenity in enumerate(output.amenities, 1):
                print(f"  {i}. {amenity}")

            print(f"\nWhy this hotel: {output.recommendation_reason}")

        elif isinstance(output, TravelPlan):
            print(f"\n🌍 TRAVEL PLAN FOR {output.destination.upper()} 🌍")
            print(f"Duration: {output.duration_days} days")
            print(f"Budget: ${output.budget}")

            print("\n🎯 RECOMMENDED ACTIVITIES:")
            for i, activity in enumerate(output.activities, 1):
                print(f"  {i}. {activity}")

            print(f"\n📝 NOTES: {output.notes}")

if __name__ == "__main__":
    asyncio.run(main())
