'''
# WHAT IS TOOL INTEGRATION?

A Tool is simply a Python function that the LLM can use
to perform tasks it cannot do by itself.

Examples:
- Calculator
- Weather API
- Database Query
- Search Engine
- File Reader

Instead of the LLM guessing,
it calls the appropriate tool to get the real answer.
'''

# Tools to write the Tool Integration
'''
1. @tool 
- Converts a normal Python function into a LangChain Tool.
Now the LLM knows:
- Tool name → calculator
- Parameters → a, b
- Description → "Add two numbers."

2. llm_with_tools = llm.bind_tools([calculator])
- registers the tool with the llm , so that llm knows this the toolw hich it can request during quering .


3. llm_with_tools.invoke(...)

The LLM automatically decides
whether to call the tool or answer directly.
'''

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key="skolhkjbhyf89re-v9e=b9e-r0g3hrfjvdfkvkfd"
)

# Defining tool
@tool
def get_weather(city:str) -> str:
    weather = {
        "Paris": "18°C, Sunny",
        "London": "15°C, Rainy",
        "Tokyo": "22°C, Clear"
    }

    return weather.get(city,"City not Found !!")

@tool
def calculate_distance(city1: str, city2: str):
    """Calculate distance."""
    return "344 km"

# Bind Tool to LLM
llm_with_tools = llm.bind_tools([get_weather,calculate_distance])

# Use the tools [Ask question]
response = llm_with_tools.invoke(
    "What's the weather in Paris?"
)

print(response)

'''
Working:
What happens?

User
 │
 ▼
LLM
 │
 ▼
Detects weather information is needed
 │
 ▼
Calls get_weather("Paris")
 │
 ▼
Returns "18°C, Sunny"
 │
 ▼
LLM generates final response
'''