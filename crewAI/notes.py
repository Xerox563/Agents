# ---------------------------- Agent [role, verbose, llm, backstory, goal] ------------------------------------------------
'''
travel_agent = Agent(
    role="Travel Planner",
    
    goal="Create amazing travel itineraries",
    
    backstory="""
    You are an expert travel planner with 10 years experience.
    You know best destinations, flights, hotels, attractions.
    You create detailed day-by-day travel plans.
    """,
    
    llm=llm,
    
    verbose=True
)

# Why this Agent?
# - Role: Specialist in travel
# - Goal: What agent tries to achieve
# - Backstory: Context for agent (makes better decisions)
# - LLM: Which model to use
# - Verbose: Show what agent is doing
'''
# -------------------------- Tasks ----------------------------------------
# A Task defines : What to do and Who should do it . [without this : unclear responsibilties]
'''
# Task 1: Travel Agent plans trip
task1 = Task(
    description="""
    Plan a 3-day trip to Paris.
    Include:
    - Flight recommendations
    - Hotel suggestions
    - Daily itinerary
    - Attractions to visit
    """,
    
    expected_output="Detailed Paris trip plan with flights, hotels, and itinerary",
    
    agent=travel_agent
)

# Why this Task?
# - Description: Clear instructions for agent
# - Expected output: What agent should produce
# - Agent: Which agent handles this task
'''
# -------------------------------- Flow -----------------------------------
'''
Task1 created:
"Plan flights to Paris"
    ↓
Assigned to: Travel Agent
Expected output: Flight options with prices
    ↓
Travel Agent receives task
    ↓
Completes task
    ↓
Returns: Flight options

Task2 created:
"Calculate cost with budget"
    ↓
Assigned to: Budget Agent
Expected output: Cost breakdown
    ↓
Budget Agent receives task
    ↓
(Can read Task1 output from Travel Agent!)
    ↓
Completes task
    ↓
Returns: Cost breakdown

Tasks execute in sequence
Each can use previous task's output!
'''

# MAIN FLOW
'''
Overall Flow

           User
             │
             ▼
      crew.kickoff()
             │
             ▼
            Crew
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
  Task1    Task2    Task3
     │       │        │
     ▼       ▼        ▼
Travel   Budget    Food
Agent     Agent    Agent
     │       │        │
     └───────┼────────┘
             ▼
      Crew collects outputs
             │
             ▼
        Final Response
'''


#  -------------------------- MAIN FLOW --------------------------------------
'''
# ============================================
# HOW CREW WORKS (SHORT)
# ============================================

Step 1: Create Agents

Travel Agent
Budget Agent
Food Agent

↓

Agents are ready but idle.

----------------------------------------

Step 2: Create Tasks

Task 1 → Travel Agent
Task 2 → Budget Agent
Task 3 → Food Agent

↓

Each task defines:
✔ What to do
✔ Which agent should do it

----------------------------------------

Step 3: Create Crew

crew = Crew(
    agents=[...],
    tasks=[...]
)

↓

Crew acts as the manager (orchestrator).

Responsibilities:
✔ Execute tasks
✔ Coordinate agents
✔ Pass task outputs
✔ Return final result

----------------------------------------

Step 4: Start Execution

crew.kickoff()

↓

Crew starts Task 1

Travel Agent
        │
        ▼
Trip Plan

↓

Crew stores Task 1 output.

----------------------------------------

Crew starts Task 2

Task 1 Output
        │
        ▼
Budget Agent
        │
        ▼
Budget Report

↓

Crew stores Task 2 output.

----------------------------------------

Crew starts Task 3

Task 1 Output
+
Task 2 Output
        │
        ▼
Food Agent
        │
        ▼
Restaurant Suggestions

↓

Crew stores Task 3 output.

----------------------------------------

Final Step

Crew combines

✔ Trip Plan
✔ Budget Report
✔ Restaurant Suggestions

↓

Returns Final Result

============================================

Communication Flow

Travel Agent
      │
      ▼
     Crew
      │
      ▼
Budget Agent
      │
      ▼
     Crew
      │
      ▼
Food Agent

Agents never communicate directly.

The Crew passes one task's output
as the next task's input.
'''