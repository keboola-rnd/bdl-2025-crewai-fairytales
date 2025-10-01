
#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from crewai import Agent, Crew, Process, Task, LLM
from fairytale_crew.crew import FairytaleCrew
from fairytale_crew.find_crew import FindCrew
import httpx
from keboola.component import CommonInterface, UserException
import os
import json
import pandas as pd
import csv



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
        
        result = (
            FindCrew()
            .crew()
            .kickoff(inputs={"book_id": self.state.inspiration_book_id})
        )
      
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
