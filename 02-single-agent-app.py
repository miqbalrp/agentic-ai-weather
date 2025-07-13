from agents import Agent, Runner
import asyncio

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

agent = Agent(
    name="Weather Assistant",
    instructions="You provide weather updates and forecasts."
)

def main():
    st.title("Weather Assistant")
    user_input = st.text_input("Ask about the weather:")
    
    if st.button("Get Weather Update"):
        with st.spinner("Thinking..."):
            if user_input:
                result = asyncio.run(Runner.run(agent, user_input))
                st.write(result.final_output)
            else:
                st.write("Please enter a question about the weather.")

if __name__ == "__main__":
    main()