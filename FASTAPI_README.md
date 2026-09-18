# FastAPI Travel Agent Server

This FastAPI server wraps the v4_handoffs travel agent system, providing a REST API interface for travel planning queries.

## Features

- **Multi-Agent System**: Uses specialized agents for flights, hotels, and general travel planning
- **REST API**: Clean HTTP endpoints for easy integration
- **Structured Responses**: JSON responses with typed data models
- **CORS Support**: Cross-origin requests enabled for web applications
- **Health Monitoring**: Built-in health check endpoint

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env` file:
```
BASE_URL=your_openai_compatible_api_url
API_KEY=your_api_key
MODEL_NAME=your_model_name
```

## Running the Server

### Option 1: Direct Python execution
```bash
python fastapi_travel_agent.py
```

### Option 2: Using uvicorn
```bash
uvicorn fastapi_travel_agent:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
- **GET** `/`
- Returns API information and available endpoints

### 2. Health Check
- **GET** `/health`
- Returns server health status

### 3. Process Travel Query
- **POST** `/query`
- **Body**: `{"query": "your travel question"}`
- **Response**: Structured travel recommendation

### 4. List Agents
- **GET** `/agents`
- Returns information about available agents

## Example Usage

### Using curl:

```bash
# Health check
curl http://localhost:8000/health

# Flight query
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "I need a flight from New York to Chicago tomorrow"}'

# Hotel query
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Find me a hotel in Paris with a pool for under $300 per night"}'

# General travel planning
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "I want to plan a 5-day trip to Tokyo with a budget of $2000"}'
```

### Using Python requests:

```python
import requests

# Flight query
response = requests.post(
    "http://localhost:8000/query",
    json={"query": "I need a flight from New York to Chicago tomorrow"}
)
result = response.json()
print(result)
```

## Response Types

The API returns different response types based on the query:

### Flight Recommendation
```json
{
  "success": true,
  "response_type": "flight",
  "data": {
    "airline": "SkyWays",
    "departure_time": "08:00",
    "arrival_time": "10:30",
    "price": 350.00,
    "direct_flight": true,
    "recommendation_reason": "Best value for money with convenient timing"
  },
  "message": "Flight recommendation generated successfully"
}
```

### Hotel Recommendation
```json
{
  "success": true,
  "response_type": "hotel",
  "data": {
    "name": "City Center Hotel",
    "location": "Downtown",
    "price_per_night": 199.99,
    "amenities": ["WiFi", "Pool", "Gym", "Restaurant"],
    "recommendation_reason": "Great location with excellent amenities"
  },
  "message": "Hotel recommendation generated successfully"
}
```

### Travel Plan
```json
{
  "success": true,
  "response_type": "travel_plan",
  "data": {
    "destination": "Tokyo",
    "duration_days": 5,
    "budget": 2000.0,
    "activities": ["Visit Senso-ji Temple", "Explore Harajuku", "Try authentic ramen"],
    "notes": "Consider getting a JR Pass for transportation"
  },
  "message": "Travel plan generated successfully"
}
```

## Testing

Run the test script to verify the API is working:

```bash
python test_fastapi_agent.py
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Error Handling

The API includes proper error handling:
- Invalid requests return appropriate HTTP status codes
- Detailed error messages for debugging
- Graceful handling of agent failures

## Architecture

The FastAPI server wraps the existing v4_handoffs multi-agent system:

1. **Travel Planner Agent**: Main coordinator, handles general queries and weather
2. **Flight Specialist Agent**: Handles flight searches and recommendations
3. **Hotel Specialist Agent**: Handles hotel searches and recommendations

The system automatically routes queries to the appropriate specialist agents based on the content of the user's question.
