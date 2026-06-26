'''
Why we dont use the : memory.save_context(...)

Because ConversationChain does it automatically.
Internally it performs:

1. Load previous history
2. Add current user input
3. Send everything to LLM
4. Receive response
5. Save user + AI response into memory

Behind the scenes its doing:
---
history = memory.load_memory_variables({})

response = llm.invoke(history + user_input)

memory.save_context(
    {"input": user_input},
    {"output": response.content}
)
---
'''

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key="your_api_key_here"
)

# Create memory object
# ConversationBufferMemory stores all messages
memory = ConversationBufferMemory()

# Create conversation chain with memory
# Automatically manages conversation history
conversation = ConversationChain(
    memory= memory,
    llm = llm,
    verbose = True # shows whats happening
)

response1 = conversation.predict(
    input = 'Hi! I want to learn Python for web development'
)

print(response1)

# What LangChain did:
# 1. Saved user input to memory
# 2. Called LLM with input
# 3. Saved LLM response to memory
# 4. Memory now has: [Turn 1 user, Turn 1 AI]

response2 = conversation.predict(
    input="What framework should I use?"
)
print(response2)

# What LangChain did:
# 1. Loaded ALL previous messages from memory
# 2. Sent: [Turn 1 user, Turn 1 AI, Turn 2 user]
# 3. LLM sees context from Turn 1!
# 4. Can answer about Python web development framework
# 5. Saved Turn 2 response to memory


# VIEW FULL CONVERSATION HISTORY
print(memory.buffer)