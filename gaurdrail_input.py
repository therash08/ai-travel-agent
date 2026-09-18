import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME") 

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("Please set BASE_URL, API_KEY, and MODEL_NAME.")

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

# Define output schema
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

# Guardrail agent
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

# Guardrail function
@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )

# Main agent
agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

# Main async function
async def main():
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail didn't trip - this is unexpected")
    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

# Run it
if __name__ == "__main__":
    asyncio.run(main())
