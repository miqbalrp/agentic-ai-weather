# Agentic AI Weather

## Overview
Agentic AI Weather is a collection of Python scripts and modules designed to demonstrate a step-by-step learning on multi-agent systems using the OpenAI Agents SDK framework. This repository serves as a complementary resource to articles published by the author. The project includes examples of single-agent systems, multi-agent systems, tool usage, and handoff mechanisms, utilizing the use case of a helpful weather assistant that retrieves data from publicly accessible APIs.

### Published Articles
- [Hands-on with Agents SDK: Your First API-calling Agent](https://towardsdatascience.com/hands%e2%80%91on-with-agents-sdk-your-first-api%e2%80%91calling-agent/)
- [Hands-On with Agents SDK: Multi-Agent Collaboration
](https://towardsdatascience.com/hands-on-with-agents-sdk-multi-agent-collaboration/)

## Project Structure

### Core Applications
- **app01_single_agent.py**: Example of a single-agent system.
- **app02_single_agent.py**: Streamlit application demonstrating a single-agent system.
- **app03_tooluse_agent.py**: Example of an agent utilizing external API tools.
- **app04_basic_handoff.py**: Demonstrates basic agent handoff mechanisms between specialists.
- **app05_customized_handoff.py**: Advanced handoff with custom callbacks and structured data.
- **app06_agents_as_tools.py**: Shows how to use agents as tools within an orchestrator pattern.
- **app07_customized_agents_as_tools.py**: Customized agents-as-tools implementation with async wrappers.

### Additional Files
- **app.py**: Main Streamlit application entry point.
- **visualize_agents.py**: Utility for visualizing agent interactions.

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/miqbalrp/agentic-ai-weather.git
   cd agentic-ai-weather
2. **Set up your environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
3. **Configure your environment variables**
   Create a .env file with:
   ```bash
   OPENAI_API_KEY=your_openai_key_here

## Usage

Run any of the Python scripts to explore the functionality. For example:

```zsh
# Run the main Streamlit app
streamlit run app.py

# Or run individual examples
python app04_basic_handoff.py
python app06_agents_as_tools.py

# Run the agent visualization tool
python visualize_agents.py
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
