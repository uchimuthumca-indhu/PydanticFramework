from dotenv import load_dotenv

from crewai import Agent, Task, Crew, LLM

load_dotenv()

llmmodel = LLM(model="gpt-4o-mini", temperature=0.7)

researcher = Agent(
    role="Researcher",
    goal="Gather information",
    backstory="Expert investigator",
    llm=llmmodel
)
print("CrewAI researcher is Ready to use")
print("Role",researcher.role)
print("Goal",researcher.goal)
print("Backstory",researcher.backstory) 
