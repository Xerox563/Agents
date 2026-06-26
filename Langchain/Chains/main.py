'''
Without Chains (Manual):
- Format prompt
- send to llm
- parse responses
- save to db

# Normal flow - lots of code

With Chains (LangChain):
Step 1 | Step 2 | Step 3 | Step 4
Data flows automatically between steps
LangChain handles everything
'''

# How it works behind the scenes
'''
Input
  ↓
[Prompt Template] → fills template with input
  ↓
[LLM] → sends to LLM, gets response
  ↓
[Output Parser] → parses LLM response
  ↓
[Database] → saves result
  ↓
Output

LangChain: prompt | llm | parser | database
           Data flows left to right automatically
'''

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key="your_api_key_here"
)

# Create prompt template
prompt_template = PromptTemplate.from_template(
    "Explain {topic} in simple terms for {audience}"
)

# Create chain: template | llm | parser
# | = pipe operator (data flows left to right)
chain = prompt_template | llm | StrOutputParser()

# Why StrOutputParser?
# LLM returns complex object, Parser extracts just the text

# Use chain
result = chain.invoke({
    "topic": "Python",
    "audience": "beginner"
})

print("Chain Result:")
print(result)
print()
