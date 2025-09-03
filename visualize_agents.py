# Before running this script, ensure you need to have the following installed:
# - graphviz 
# - pip install "openai-agents[viz]"

# Check documentation for more details: https://openai.github.io/openai-agents-python/visualization/

from agents.extensions.visualization import draw_graph
import app01_single_agent
import app03_tooluse_agent
import app04_basic_handoff
import app06_agents_as_tools 
import app08_guardrails 

agents = [
    app03_tooluse_agent.weather_specialist_agent,
    app04_basic_handoff.triage_agent,
    app06_agents_as_tools.orchestrator_agent,
    app08_guardrails.orchestrator_agent
]

dir = "assets/graphs/"

if __name__ == "__main__":
    for agent in agents:
        filename = f"{dir}{agent.name}_graph"
        draw_graph(agent, filename)
        print(f"Graph for {agent.name} saved to {filename}")
    
    print("All agent graphs have been generated.")

