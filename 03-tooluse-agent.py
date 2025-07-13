from agents import Agent, Runner, function_tool
import asyncio
import requests

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

@function_tool
def get_current_weather(latitude: float, longitude: float) -> dict:
    print("[debug] get_current_weather called")
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation,weathercode,windspeed_10m,winddirection_10m",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    return response.json()

current_weather_agent = Agent(
    name="Current Weather Agent",
    instructions="""
    You are a weather assistant agent.
    Given current weather data (including temperature, humidity, wind speed/direction, precipitation, and weather codes), provide:
    1. A clear and concise explanation of the current weather conditions.
    2. Practical suggestions or precautions for outdoor activities, travel, health, or clothing based on the data.
    3. If any severe weather is detected (e.g., heavy rain, thunderstorms, extreme heat), highlight necessary safety measures.

    Format your response in two sections:
    Weather Summary:
    - Briefly describe the weather in plain language.

    Suggestions:
    - Offer actionable advice relevant to the weather conditions.
    """,
    tools=[get_current_weather],
    tool_use_behavior="run_llm_again"
)

def main():
    st.title("Weather Assistant")
    user_input = st.text_input("Ask about the weather:")
    
    if st.button("Get Weather Update"):
        with st.spinner("Thinking..."):
            if user_input:
                result = asyncio.run(Runner.run(current_weather_agent, user_input))
                st.write(result.final_output)
            else:
                st.write("Please enter a question about the weather.")

if __name__ == "__main__":
    main()