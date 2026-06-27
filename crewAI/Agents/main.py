# CREWAI: CREW (ORCHESTRATION) 
# Crew passes the previous task's output to the next task as context , In this way direct communication does not happens between agents , it happens using middleware as the crew
import os
from crewai import Agent, Task, Crew
from crewai.llm import LLM
from dotenv import load_dotenv

# SETUP
load_dotenv()

llm = LLM(
    model=os.getenv("AI_MODEL_NAME"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# DEFINE AGENTS

travel_agent = Agent(
    role="Travel Planner",
    goal="Create amazing travel itineraries",
    backstory="Expert travel planner with 10 years experience",
    llm=llm,
    verbose=True
)

budget_agent = Agent(
    role="Budget Manager",
    goal="Manage travel budget and find cost-effective options",
    backstory="Budget expert who finds best deals",
    llm=llm,
    verbose=True
)

food_agent = Agent(
    role="Food & Restaurant Expert",
    goal="Suggest best restaurants and local cuisine",
    backstory="Food critic who knows best restaurants",
    llm=llm,
    verbose=True
)

# DEFINE TASKS

task1 = Task(
    description="""
    Plan a 3-day trip to Paris.
    Include:
    - Flight recommendations
    - Hotel suggestions
    - Daily itinerary
    - Attractions to visit
    """,
    expected_output="Detailed Paris trip plan",
    agent=travel_agent
)

task2 = Task(
    description="""
    Analyze the trip plan and calculate:
    - Total flight cost
    - Total hotel cost
    - Recommended daily budget
    - Ways to save money
    
    Budget limit: $2000
    """,
    expected_output="Cost breakdown with savings",
    agent=budget_agent
)

task3 = Task(
    description="""
    For the Paris trip:
    - Suggest best restaurants
    - Recommend local cuisine
    - Keep within budget from Task 2
    - Suggest 1 restaurant per day
    """,
    expected_output="Restaurant recommendations",
    agent=food_agent
)

# CREATE CREW (The Orchestrator)

crew = Crew(
    agents=[travel_agent, budget_agent, food_agent],
    # List all agents
    
    tasks=[task1, task2, task3],
    # List all tasks in order
    
    verbose=True
    # Show what crew is doing
)

# Why Crew?
# - Manages all agents
# - Executes all tasks
# - Passes results between tasks
# - Combines final output
# - YOU don't have to manage anything!


# EXECUTE CREW

print("= STARTING CREW =\n")

# kickoff() = Run all tasks automatically!
result = crew.kickoff()

# What happens:
# 1. Crew starts Task1 with Travel Agent
#    → Travel agent plans Paris trip
#    → Result saved
#
# 2. Crew starts Task2 with Budget Agent
#    → Budget agent reads Task1 result
#    → Calculates costs
#    → Result saved
#
# 3. Crew starts Task3 with Food Agent
#    → Food agent reads Task1 + Task2 results
#    → Suggests restaurants
#    → Result saved
#
# 4. Crew combines all results
#    → Returns complete trip plan!

print("\n= CREW RESULT =\n")
print(result)

# 
# REAL WORLD FLOW
# 

# Without Crew (Manual):
# 1. You: "Travel agent, plan trip"
# 2. Travel agent: Returns plan
# 3. You: "Budget agent, calculate cost"
# 4. You: Show budget agent the plan
# 5. Budget agent: Returns cost
# 6. You: "Food agent, suggest restaurants"
# 7. You: Show food agent budget and plan
# 8. Food agent: Returns restaurants
# 9. You: Combine all 3 results
# 10. You: Show user final plan

# Lots of manual work!

# With Crew (Automatic):
# 1. You: crew.kickoff()
# 2. Crew: Runs Task1, Task2, Task3 automatically
# 3. Crew: Passes results between tasks
# 4. Crew: Combines everything
# 5. You: Get final result!

# Much simpler!

# 
# KEY BENEFIT
# 
# Without Crew:
# - Manually run each task
# - Manually pass results
# - Manually combine results
# - Error-prone, tedious

# With Crew:
# - Define agents and tasks
# - crew.kickoff() handles everything
# - Automatic coordination
# - Clean, organized, professional