from agents import Agent, Runner
import asyncio
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name="Weather Assistant",
    instructions="You provide accurate and concise weather updates based on user queries in plain language."
)

async def run_agent(user_input: str):
    result = await Runner.run(agent, user_input)
    return result.final_output

def main():
    st.title("Weather Assistant")
    user_input = st.text_input("Ask about the weather:")
    
    if st.button("Get Weather Update"):
        with st.spinner("Thinking..."):
            if user_input:
                agent_response = asyncio.run(run_agent(user_input))
                st.write(agent_response)
            else:
                st.write("Please enter a question about the weather.")

if __name__ == "__main__":
    main()