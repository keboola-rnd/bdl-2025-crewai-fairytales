from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from pydantic import BaseModel
import os
from typing import List
from crewai.tools import BaseTool
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters 

@CrewBase
class FindCrew():
    """FindCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    agents_config = 'config/find_agents.yaml'
    tasks_config = 'config/find_tasks.yaml'
    
    def __init__(self):
        super().__init__()
        self.keboola_mcp_tools = None

    @agent
    def book_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['book_finder'],
            verbose=True,
            tools=self.get_keboola_mcp_tools()
        )

    @task
    def find_book_task(self) -> Task:
        class BookSummary(BaseModel):
            book_id: str
            title: str
            author_name: str
            summary: str
    
        return Task(
            config=self.tasks_config['find_book_task'],
            agent=self.book_finder(),
            output_file="out/files/book_summary.json",
            output_json=BookSummary,
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
                if tool_name.startswith('list') or tool_name.startswith('get') or tool_name.startswith('query'):
                    filtered_tools.append(tool)
            
            return filtered_tools

    @crew
    def crew(self) -> Crew:
        """Creates the FinderCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
        
    

