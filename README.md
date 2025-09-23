# 🚀 FairytaleCrew

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green?logo=python)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Powered-orange)](https://crewai.com)

A magical multi-agent AI system built with CrewAI that creates engaging fairytales. The crew consists of specialized agents that plan and write captivating fairytale stories with rich characters, plots, and magical elements.

## 🛠️ Setup

### Environment Configuration

Copy the environment template and configure your variables:

```bash
cp .env.dist .env
```

Edit the `.env` file and fill in the appropriate values for all required variables. Examples are provided in the `.env.dist` file.

## 🚀 Running the Project

Launch your crew of AI agents:

```bash
docker-compose run crew
```

This command initializes the FairytaleCrew using Docker, assembling the agents and assigning them tasks as defined in your configuration.

## 📊 What the Crew Does

The FairytaleCrew consists of two specialized AI agents:

- **Fairytale Planner**: Creates engaging story plans with all the elements of a fairytale
- **Fairytale Writer**: Writes captivating fairytale stories based on the plans

The crew works together to create magical and engaging fairytale stories with rich characters, plots, and magical elements.

## 📁 Output

All fairytale results are saved to the `output/` folder:

- `output/fairytale_plan.json` - Fairytale story plan and structure
- `output/fairytale_story.txt` - Complete fairytale story

Make sure the `output/` directory exists before running the crew.

## 📁 Project Structure

```
crewai-mcp/
├── src/fairytale_crew/
│   ├── config/
│   │   ├── agents.yaml    # Agent definitions
│   │   └── tasks.yaml     # Task configurations
│   ├── crew.py           # Main crew logic
│   └── main.py           # Entry point
├── output/               # Fairytale results
│   ├── fairytale_plan.json  # Fairytale plan
│   └── fairytale_story.txt  # Complete fairytale
├── docker-compose.yml    # Docker configuration
├── .env.dist            # Environment template
└── README.md            # This file
```

## 🤝 Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

---

**Happy Fairytale Creation! 🧚‍♀️✨**
