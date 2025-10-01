# 🚀 FairytaleCrew

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green?logo=python)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Powered-orange)](https://crewai.com)
[![Keboola](https://img.shields.io/badge/Keboola-Integrated-purple)](https://keboola.com)
[![MCP](https://img.shields.io/badge/MCP-Enabled-green)](https://modelcontextprotocol.io)

A sophisticated multi-agent AI system built with CrewAI that creates engaging fairytales with Keboola integration. The crew consists of specialized agents that find inspiration from existing books, plan captivating fairytale stories, write them, and translate them to different languages using MCP (Model Context Protocol) tools for seamless data integration.

## 🛠️ Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.10+ (for local development)
- Keboola account with storage access
- OpenAI API key

### Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Keboola Configuration
KBC_STORAGE_API_URL=your_keboola_storage_api_url
KBC_STORAGE_TOKEN=your_keboola_storage_token

# Model Configuration
MODEL=openai/gpt-4o
```

### Input Configuration

Create a `config.csv` file in the `in/tables/` directory with the following structure:

```csv
main_character,location,main_problem,target_language,inspiration_book_id
Alice,Enchanted Forest,Find the lost magic crystal,Spanish,12345
```

## 🚀 Running the Project

### Using Docker (Recommended)

Launch your crew of AI agents:

```bash
docker-compose run crew
```

This command initializes the FairytaleCrew using Docker, assembling the agents and assigning them tasks as defined in your configuration.

### Local Development

For local development, you can run the crew directly:

```bash
# Install dependencies
pip install -e .

# Run the crew
python -m fairytale_crew.main
```

## 📊 What the Crew Does

The FairytaleCrew consists of four specialized AI agents working in a sophisticated flow:

### 🔍 Book Finder Agent
- Uses Keboola MCP tools to query the `books_authors_summaries_complete` table
- Finds inspiration books based on the provided `inspiration_book_id`
- Retrieves book metadata including title, author, and summary

### 📝 Fairytale Planner Agent
- Creates engaging story plans with all the elements of a fairytale
- Uses inspiration from the found book to enhance the story structure
- Plans the narrative arc, character development, and magical elements

### ✍️ Fairytale Writer Agent
- Writes captivating fairytale stories based on the detailed plans
- Creates stories that are maximum 3 paragraphs long
- Ensures the story follows fairytale conventions and includes magical elements

### 🌍 Fairytale Translator Agent
- Translates the completed fairytale to the target language
- Maintains the story's essence while adapting it culturally
- Outputs the translated story in markdown format

### 🔄 Workflow Process
The crew follows a sequential process using CrewAI Flow:
1. **State Initialization**: Loads configuration from `config.csv`
2. **Book Discovery**: Finds inspiration book in Keboola storage
3. **Story Planning**: Creates detailed fairytale plan
4. **Story Writing**: Writes the complete fairytale
5. **Translation**: Translates to target language
6. **Output Generation**: Saves results in multiple formats

## 📁 Output

All fairytale results are saved to the `out/tables/` folder:

- `out/tables/book_summary.json` - Inspiration book metadata (title, author, summary)
- `out/tables/story_translated.json` - Complete fairytale with plan and story
- `out/tables/story_translated.csv` - CSV version of the translated story
- `out/tables/story.csv` - Final processed story output

The system automatically creates the necessary output directories and files during execution.

## 📁 Project Structure

```
crewai-mcp/
├── src/fairytale_crew/
│   ├── config/
│   │   ├── agents.yaml    # Agent definitions and configurations
│   │   └── tasks.yaml     # Task configurations and descriptions
│   ├── tools/
│   │   └── custom_tool.py # Custom tools and utilities
│   ├── crew.py           # Main crew logic and agent definitions
│   └── main.py           # Entry point with flow orchestration
├── in/tables/            # Input data
│   └── config.csv        # Configuration parameters
├── out/tables/           # Output results
│   ├── book_summary.json # Inspiration book metadata
│   ├── story_translated.json # Complete fairytale with plan
│   ├── story_translated.csv  # CSV version of story
│   └── story.csv         # Final processed output
├── data/                 # Data configuration
│   └── config.json       # Keboola component configuration
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Docker image definition
├── pyproject.toml       # Python project configuration
├── .env                 # Environment variables (create this)
└── README.md            # This file
```

## 🔧 Technical Details

### Dependencies

- **CrewAI**: Multi-agent AI framework for orchestration
- **CrewAI Tools**: MCP integration for external tool connectivity
- **Keboola Component**: Integration with Keboola data platform
- **Pandas**: Data manipulation and processing
- **Pydantic**: Data validation and serialization
- **HTTPX**: HTTP client for API interactions

### MCP Integration

The project uses Model Context Protocol (MCP) to integrate with Keboola storage:

- **Read Operations**: Query books and authors data
- **Data Processing**: Transform and structure data for AI agents
- **Output Management**: Save results in multiple formats

### Flow Architecture

The system uses CrewAI Flow for state management and sequential execution:

```python
@start() -> fill_state() -> find_inspiration_book() -> generate_fairytale() -> save_fairytale()
```

Each step maintains state and passes data to the next phase, ensuring continuity throughout the process.

## 🚨 Troubleshooting

### Common Issues

1. **Missing Environment Variables**: Ensure all required environment variables are set in `.env`
2. **Keboola Connection**: Verify your Keboola credentials and API URL
3. **Book ID Not Found**: Check that the `inspiration_book_id` exists in your Keboola storage
4. **Output Directory**: The system creates output directories automatically

### Debug Mode

Run with verbose logging to see detailed agent interactions:

```bash
docker-compose run crew
```

The system will output detailed logs showing each agent's work and decision-making process.

## 🤝 Contributing

Feel free to contribute to this project by:

1. Submitting issues for bugs or feature requests
2. Creating pull requests with improvements
3. Adding new agent capabilities or tools
4. Improving documentation

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

---

**Happy Fairytale Creation! 🧚‍♀️✨**
