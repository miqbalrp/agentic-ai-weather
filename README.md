# Agentic AI Weather

## Overview
Agentic AI Weather is a collection of Python scripts and modules designed to demonstrate a step-by-step learning on multi-agent systems using the OpenAI Agents SDK framework. This repository serves as a complementary resource to articles published by the author. The project includes examples of single-agent systems, multi-agent systems, tool usage, and handoff mechanisms, utilizing the use case of a helpful weather assistant that retrieves data from publicly accessible APIs.

### Published Articles
- [Hands-on with Agents SDK: Your First API-calling Agent](https://towardsdatascience.com/hands%e2%80%91on-with-agents-sdk-your-first-api%e2%80%91calling-agent/)

## Project Structure

- **01-single-agent.py**: Example of a single-agent system.
- **02-single-agent-app.py**: Application demonstrating a single-agent system.
- **03-tooluse-agent-app.py**: Example of an agent utilizing tools.
- **04-handoff-agent-app.py**: Demonstrates agent handoff mechanisms.

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
python 04-handoff-agent-app.py
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
