from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Choose which LLM (just this line changes!)
# llm = ChatOpenAI(model="gpt-3.5-turbo")
# llm = ChatAnthropic(model="claude-3-sonnet-20240229")
llm = ChatGoogleGenerativeAI(model="gemini-pro",api_key = "sk424789iwtrtorpepterwtrrteevcrewqwrgtgbvc2p8765")

# same code for all LLMS
response = llm.invole("Hello How r You ??")
answer = response.content

# 1. Same llm.invoke() works for all LLMs
# 2. Response format always same (.content)