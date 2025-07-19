from agents import Agent, Runner
import asyncio

from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    name="Weather Assistant",
    instructions="You provide accurate and concise weather updates based on user queries in plain language."
)

async def run_agent():
    result = await Runner.run(agent, "What's the weather like today in Jakarta?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(run_agent())