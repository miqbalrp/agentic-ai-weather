from agents import (
    Agent, 
    Runner, 
    function_tool, 
    
    GuardrailFunctionOutput, 
    input_guardrail, 
    InputGuardrailTripwireTriggered,
    output_guardrail,
    OutputGuardrailTripwireTriggered
    )
import asyncio
import requests
import streamlit as st
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Define output model for the guardrail agent to classify if input is off-topic
class TopicClassificationOutput(BaseModel):
    is_off_topic: bool = Field(
        description="True if the input is off-topic (not related to weather/air quality and not a greeting), False otherwise"
    )
    reasoning: str = Field(
        description="Brief explanation of why the input was classified as on-topic or off-topic"
    )

# Create the guardrail agent to determine if input is off-topic
topic_classification_agent = Agent(
    name="Topic Classification Agent",
    instructions=(
        "You are a topic classifier for a weather and air quality application. "
        "Your task is to determine if a user's question is on-topic. "
        "Allowed topics include: "
        "1. Weather-related: current weather, weather forecast, temperature, precipitation, wind, humidity, etc. "
        "2. Air quality-related: air pollution, AQI, PM2.5, ozone, air conditions, etc. "
        "3. Location-based inquiries about weather or air conditions "
        "4. Polite greetings and conversational starters (e.g., 'hello', 'hi', 'good morning') "
        "5. Questions that combine greetings with weather/air quality topics "
        "Mark as OFF-TOPIC only if the query is clearly unrelated to weather/air quality AND not a simple greeting. "
        "Examples of off-topic: math problems, cooking recipes, sports scores, technical support, jokes (unless weather-related). "
        "Examples of on-topic: 'Hello, what's the weather?', 'Hi there', 'Good morning, how's the air quality?', 'What's the temperature?' "
        "The final output MUST be a JSON object conforming to the TopicClassificationOutput model."
    ),
    output_type=TopicClassificationOutput,
    model="gpt-4o-mini" # Use a fast and cost-effective model
)

# Create the input guardrail function
@input_guardrail
async def off_topic_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    """
    Classifies user input to ensure it is on-topic for a weather and air quality app.
    """

    result = await Runner.run(topic_classification_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output.reasoning,
        tripwire_triggered=result.final_output.is_off_topic
    )

# Define function tools and specialized agents for weather and air qualities
@function_tool
def get_current_weather(latitude: float, longitude: float) -> dict:
    """Fetch current weather data for the given latitude and longitude."""
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation,weathercode,windspeed_10m,winddirection_10m",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    return response.json()

weather_specialist_agent = Agent(
    name="Weather Specialist Agent",
    instructions="""
    You are a weather specialist agent.
    Your task is to analyze current weather data, including temperature, humidity, wind speed and direction, precipitation, and weather codes.

    For each query, provide:
    1. A clear, concise summary of the current weather conditions in plain language.
    2. Practical, actionable suggestions or precautions for outdoor activities, travel, health, or clothing, tailored to the weather data.
    3. If severe weather is detected (e.g., heavy rain, thunderstorms, extreme heat), clearly highlight recommended safety measures.

    Structure your response in two sections:
    Weather Summary:
    - Summarize the weather conditions in simple terms.

    Suggestions:
    - List relevant advice or precautions based on the weather.
    """,
    tools=[get_current_weather],
    tool_use_behavior="run_llm_again"
)

@function_tool
def get_current_air_quality(latitude: float, longitude: float) -> dict:
    """Fetch current air quality data for the given latitude and longitude."""

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "european_aqi,us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    return response.json()

air_quality_specialist_agent = Agent(
    name="Air Quality Specialist Agent",
    instructions="""
    You are an air quality specialist agent.
    Your role is to interpret current air quality data and communicate it clearly to users.

    For each query, provide:
    1. A concise summary of the air quality conditions in plain language, including key pollutants and their levels.
    2. Practical, actionable advice or precautions for outdoor activities, travel, and health, tailored to the air quality data.
    3. If poor or hazardous air quality is detected (e.g., high pollution, allergens), clearly highlight recommended safety measures.

    Structure your response in two sections:
    Air Quality Summary:
    - Summarize the air quality conditions in simple terms.

    Suggestions:
    - List relevant advice or precautions based on the air quality.
    """,
    tools=[get_current_air_quality],
    tool_use_behavior="run_llm_again"
)

# Define the main orchestrator agent with guardrails
orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions="""
    You are an orchestrator agent.
    Your task is to manage the interaction between the Weather Specialist Agent and the Air Quality Specialist Agent.
    You will receive a query from the user and will decide which agent to invoke based on the content of the query.
    If both weather and air quality information is requested, you will invoke both agents and combine their responses into one clear answer.
    """,
    tools=[
        weather_specialist_agent.as_tool(
            tool_name="get_weather_update",
            tool_description="Get current weather information and suggestion including temperature, humidity, wind speed and direction, precipitation, and weather codes."
        ),
        air_quality_specialist_agent.as_tool(
            tool_name="get_air_quality_update",
            tool_description="Get current air quality information and suggestion including pollutants and their levels."
        )
    ],
    tool_use_behavior="run_llm_again",
    input_guardrails=[off_topic_guardrail]
)

# Define the run_agent function
async def run_agent(user_input: str):
    result = await Runner.run(orchestrator_agent, user_input)
    return result.final_output

# Define the main function of the Streamlit app
def main():
    st.title("Weather and Air Quality Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about weather or air quality..."):
        # Show user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get and show assistant response
        with st.chat_message("assistant"):
            try:
                response = asyncio.run(run_agent(prompt))
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except InputGuardrailTripwireTriggered:
                error_msg = "I can only help with weather and air quality questions. Please try something else!"
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except Exception as e:
                error_msg = f"Sorry, something went wrong: {str(e)}"
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
