# For OpenAI
from openai import OpenAI
openai_client = OpenAI(api_key="...")
openai_response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
openai_answer = openai_response.choices[0].message.content

# For Claude (different API)
import anthropic
claude_client = anthropic.Anthropic(api_key="...")
claude_response = claude_client.messages.create(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": "Hello"}]
)
claude_answer = claude_response.content[0].text

# For Gemini (yet another different API)
import google.generativeai as genai
genai.configure(api_key="...")
gemini_model = genai.GenerativeModel("gemini-pro")
gemini_response = gemini_model.generate_content("Hello")
gemini_answer = gemini_response.text

# Problem: Different code for each!
# Hard to switch between LLMs
# Lot of duplicate logic