
#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from crewai import Agent, Crew, Process, Task, LLM
from fairytale_crew.crew import FairytaleCrew
import httpx
from keboola.component import CommonInterface, UserException
import os
import json
import pandas as pd
import csv
from typing import List
from crewai.tools import BaseTool
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters 


class FairytaleState(BaseModel):
    timestamp: str = ""
    main_character: str = ""
    inspiration_book_id: int = ""
    location: str = ""
    main_problem: str = ""
    target_language: str = ""
    fairytale: str = ""
    inspiration_book_summary: str = ""
    inspiration_book_title: str = ""
    inspiration_book_author_name: str = ""

class FairytaleFlow(Flow[FairytaleState]):
    
    def __init__(self):
        super().__init__()
        self.keboola_mcp_tools = None

    @start()
    def fill_state(self):
        print("Filling state")
        df = pd.read_csv('in/tables/config.csv')
        if not df.empty:
            row = df.iloc[0]
            for key in row.index:
                if hasattr(self.state, key):
                    setattr(self.state, key, str(row[key]))
    
    @listen(fill_state)
    def find_inspiration_book(self):
        
        class BookSummary(BaseModel):
            book_id: str
            title: str
            author_name: str
            summary: str
        
        keboola_mcp_agent = Agent(
            role='Book finder',
            goal='Find a row in Keboola storage. Always make sure you are using MCP tools to find what you need.',
            backstory='You are experienced user of Keboola MCP tool. You know how to use it to find a tables and query tables in Keboola storage.',
            tools=self.get_keboola_mcp_tools(),
            LLM=LLM(model="openai/gpt-4o", temperature=0.1)
        )
        
        find_book_task = Task(
            description=
                "You have to find table \"books_authors_summaries_complete\".  and find a book with book_id: {book_id}" 
            ,
            expected_output='A JSON object with following structure: {book_id: <book_id_value>, title: <book_title>, author_name: <author_name>, summary: <book_summary>}',
            output_json=BookSummary,
            agent=keboola_mcp_agent,
            verbose=True,
            output_file="out/files/book_summary.json"
        )
        
        inspiration_crew = Crew(
            agents=[keboola_mcp_agent],
            tasks=[find_book_task],
            process=Process.sequential,
            verbose=True
        )
      
        result = inspiration_crew.kickoff(inputs={"book_id": self.state.inspiration_book_id})
        self.state.inspiration_book_summary = result["summary"]
        self.state.inspiration_book_title = result["title"]
        self.state.inspiration_book_author_name = result["author_name"]
    
    @listen(find_inspiration_book)
    def generate_fairytale(self):
        print("Generating fairytale")
    
        result = (
            FairytaleCrew()
            .crew()
            .kickoff(inputs={k: v for k, v in self.state.dict().items()})
        )

        print("Fairytale generated", result.raw)

    @listen(generate_fairytale)
    def save_fairytale(self):
        print("Saving fairytale")
        # Read the JSON file and convert to DataFrame properly
        with open('out/files/story_translated.json', 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame with proper structure
        df = pd.DataFrame([data])
        df.to_csv('out/tables/story.csv', index=False, encoding='utf-8', sep=',', quoting=csv.QUOTE_ALL)
        
        
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
        
        


def run():
    
    ci = CommonInterface()
    params = ci.configuration.parameters
    os.environ["OPENAI_API_KEY"] = params.get("#OPENAI_API_KEY")
    os.environ["KBC_STORAGE_API_URL"] = params.get("KBC_STORAGE_API_URL")
    os.environ["KBC_STORAGE_TOKEN"] = params.get("#KBC_STORAGE_TOKEN")
    os.environ["MODEL"] = params.get("MODEL")
    flow = FairytaleFlow()
    flow.kickoff()


if __name__ == "__main__":
    run()
