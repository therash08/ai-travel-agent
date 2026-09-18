import requests
import json
import time

# Test script for the FastAPI Travel Agent
def test_travel_agent_api():
    """Test the FastAPI Travel Agent endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 Testing FastAPI Travel Agent API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the server first with:")
        print("   python fastapi_travel_agent.py")
        return
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    response = requests.get(f"{base_url}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 3: List agents
    print("\n3. Testing agents endpoint...")
    response = requests.get(f"{base_url}/agents")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 4: Flight query
    print("\n4. Testing flight query...")
    flight_query = {
        "query": "I need a flight from New York to Chicago tomorrow"
    }
    response = requests.post(f"{base_url}/query", json=flight_query)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['success']}")
        print(f"Response Type: {result['response_type']}")
        print(f"Message: {result['message']}")
        if result['response_type'] == 'flight':
            flight_data = result['data']
            print(f"Flight Recommendation:")
            print(f"  Airline: {flight_data['airline']}")
            print(f"  Departure: {flight_data['departure_time']}")
            print(f"  Arrival: {flight_data['arrival_time']}")
            print(f"  Price: ${flight_data['price']}")
            print(f"  Direct: {flight_data['direct_flight']}")
            print(f"  Reason: {flight_data['recommendation_reason']}")
    else:
        print(f"Error: {response.text}")
    
    # Test 5: Hotel query
    print("\n5. Testing hotel query...")
    hotel_query = {
        "query": "Find me a hotel in Paris with a pool for under $300 per night"
    }
    response = requests.post(f"{base_url}/query", json=hotel_query)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['success']}")
        print(f"Response Type: {result['response_type']}")
        print(f"Message: {result['message']}")
        if result['response_type'] == 'hotel':
            hotel_data = result['data']
            print(f"Hotel Recommendation:")
            print(f"  Name: {hotel_data['name']}")
            print(f"  Location: {hotel_data['location']}")
            print(f"  Price per night: ${hotel_data['price_per_night']}")
            print(f"  Amenities: {', '.join(hotel_data['amenities'])}")
            print(f"  Reason: {hotel_data['recommendation_reason']}")
    else:
        print(f"Error: {response.text}")
    
    # Test 6: General travel query
    print("\n6. Testing general travel query...")
    travel_query = {
        "query": "I want to plan a 5-day trip to Tokyo with a budget of $2000"
    }
    response = requests.post(f"{base_url}/query", json=travel_query)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['success']}")
        print(f"Response Type: {result['response_type']}")
        print(f"Message: {result['message']}")
        if result['response_type'] == 'travel_plan':
            plan_data = result['data']
            print(f"Travel Plan:")
            print(f"  Destination: {plan_data['destination']}")
            print(f"  Duration: {plan_data['duration_days']} days")
            print(f"  Budget: ${plan_data['budget']}")
            print(f"  Activities: {', '.join(plan_data['activities'])}")
            print(f"  Notes: {plan_data['notes']}")
    else:
        print(f"Error: {response.text}")
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_travel_agent_api()
