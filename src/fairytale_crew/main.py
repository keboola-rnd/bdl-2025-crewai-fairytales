
#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from fairytale_crew.crew import FairytaleCrew
import httpx
from keboola.component import CommonInterface, UserException
import os
import pandas as pd
import csv


class FairytaleState(BaseModel):
    timestamp: str = ""
    character_name: str = ""
    character_type: str = ""
    personality_traits: str = ""
    location: str = ""
    atmosphere: str = ""
    main_problem: str = ""
    antagonist: str = ""
    helper_mentor: str = ""
    story_length: str = ""
    tone: str = ""
    target_language: str = ""
    art_style: str = ""
    story_plan: str = ""
    fairytale: str = ""


class FairytaleFlow(Flow[FairytaleState]):

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
    def generate_fairytale(self):
        print("Generating fairytale")
    
        result = (
            FairytaleCrew()
            .crew()
            .kickoff(inputs={k: v for k, v in self.state.dict().items()})
        )

        print("Fairytale generated", result.raw)
        self.state.fairytale = result.raw

    @listen(generate_fairytale)
    def save_fairytale(self):
        print("Saving fairytale")
        os.makedirs("out/tables", exist_ok=True)
        df = pd.read_csv('in/tables/config.csv')
        df.insert(0, 'fairytale', self.state.fairytale)
        df.to_csv('out/tables/story.csv', index=False, encoding='utf-8', sep=',', quoting=csv.QUOTE_ALL)
        


def run():
    
    ci = CommonInterface()
    params = ci.configuration.parameters
    os.environ["OPENAI_API_KEY"] = params.get("#OPENAI_API_KEY")
    flow = FairytaleFlow()
    flow.kickoff()


if __name__ == "__main__":
    run()
