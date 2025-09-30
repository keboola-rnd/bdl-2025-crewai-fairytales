from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai.tools import BaseTool
from crewai_tools import MCPServerAdapter

@CrewBase
class FairytaleCrew():
    """FairytaleCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self):
        super().__init__()
        self.keboola_mcp_tools = None

    @agent
    def fairytale_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['fairytale_planner'],
            verbose=True,
            tools=self.get_keboola_mcp_tools(),
        )

    @agent
    def fairytale_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['fairytale_writer'],
            verbose=True,
        )

    @agent
    def fairytale_translator(self) -> Agent:
        return Agent(
            config=self.agents_config['fairytale_translator'],
            verbose=True,
        )

    @task
    def plan_fairytale(self) -> Task:
        return Task(
            config=self.tasks_config['plan_fairytale'],
            agent=self.fairytale_planner()
        )
        
    @task
    def write_fairytale(self) -> Task:
        return Task(
            config=self.tasks_config['write_fairytale'],
            agent=self.fairytale_writer()
        )

    @task
    def translate_fairytale(self) -> Task:
        return Task(
            config=self.tasks_config['translate_fairytale'],
            output_file="out/tables/story_translated.csv",
            agent=self.fairytale_translator()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FairytaleCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            llm=LLM(model="gpt-4o-mini", temperature=0.7)
        )
        
    
    def get_keboola_mcp_tools(self, include_write_tools: bool = False) -> List[BaseTool]:
        if self.keboola_mcp_tools is None:
            params = StdioServerParameters(
                command="uvx",
                args=[
                                'keboola_mcp_server',
                                '--transport', 'stdio',
                                '--log-level', 'INFO',
                                '--api-url', os.getenv('KBC_STORAGE_API_URL')
                            ],
                env={"UV_PYTHON": "3.12", **os.environ},
            )
            mcp_server_adapter = MCPServerAdapter(params)
            self.keboola_mcp_tools = mcp_server_adapter.tools
        
        if include_write_tools:
            return self.keboola_mcp_tools
        else:
        # Filter tools by name starting with "list" or "get"
            filtered_tools = []
            for tool in self.keboola_mcp_tools:
                tool_name = getattr(tool, 'name', '')
                if tool_name.startswith('list') or tool_name.startswith('get'):
                    filtered_tools.append(tool)
            
            return filtered_tools
        
