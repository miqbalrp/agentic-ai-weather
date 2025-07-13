from agents import Agent, Runner
import asyncio

from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    name="Weather Assistant",
    instructions="You provide weather updates and forecasts."
)

async def main():
    result = await Runner.run(agent, "What's the weather like today in Jakarta?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
