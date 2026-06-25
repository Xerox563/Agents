'''
Without Abstraction (Manual):
You write code for OpenAI
You write different code for Claude
You write different code for Gemini

Problem: Write same logic 3 times!

With Abstraction (LangChain):
Write code ONCE
Use ANY LLM
Just change 1 line

LangChain handles different LLMs behind the scenes
'''

# Without Langchain
'''
Your code:
  ↓
If OpenAI:
  - Format as OpenAI expects
  - Call OpenAI API
  - Parse OpenAI response
  
If Claude:
  - Format as Claude expects
  - Call Claude API
  - Parse Claude response
  
If Gemini:
  - Format as Gemini expects
  - Call Gemini API
  - Parse Gemini response

Problem: 3 different flows!
'''

# With Langchain
'''
Your code:
  ↓
LLM Abstraction Layer:
  - Detect which LLM
  - Format according to that LLM
  - Call correct API
  - Parse response
  - Return standardized format
  ↓
Your code gets same format
Regardless of which LLM

Simple!
'''