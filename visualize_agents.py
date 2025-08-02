# Before running this script, ensure you need to have the following installed:
# - graphviz 
# - pip install "openai-agents[viz]"

# Check documentation for more details: https://openai.github.io/openai-agents-python/visualization/

from agents.extensions.visualization import draw_graph
from app01_single_agent import *
from app03_tooluse_agent import *
from app04_basic_handoff import *
from app06_agents_as_tools import *

agents = [
    weather_specialist_agent,
    triage_agent,
    orchestrator_agent
]

dir = "assets/graphs/"

if __name__ == "__main__":
    for agent in agents:
        filename = f"{dir}{agent.name}_graph"
        draw_graph(agent, filename)
        print(f"Graph for {agent.name} saved to {filename}")
    
    print("All agent graphs have been generated.")

