from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class FairytaleCrew():
    """FairytaleCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self):
        super().__init__()

    @agent
    def fairytale_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['fairytale_planner'],
            verbose=True,
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
            output_file="output/fairytale_plan.txt",
            agent=self.fairytale_planner()
        )
        
    @task
    def write_fairytale(self) -> Task:
        return Task(
            config=self.tasks_config['write_fairytale'],
            output_file="output/fairytale_story.txt",
            agent=self.fairytale_writer()
        )

    @task
    def translate_fairytale(self) -> Task:
        return Task(
            config=self.tasks_config['translate_fairytale'],
            output_file="output/fairytale_story_translated.txt",
            agent=self.fairytale_translator()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FairytaleCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
