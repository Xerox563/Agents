'''
Without Templates (Manual):
prompt1 = f"User: {name}, Task: study, Hours: {hours}"
prompt2 = f"User: {name}, Task: work, Hours: {hours}"
prompt3 = f"User: {name}, Task: exercise, Hours: {hours}"

Problem: Write {name} and {hours} every time!

With Templates (LangChain):
template = "User: {name}, Task: {task}, Hours: {hours}"
prompt = PromptTemplate.from_template(template)

Then reuse:
prompt.format(name="Ali", task="study", hours=2)
prompt.format(name="Ali", task="work", hours=8)
prompt.format(name="Ali", task="exercise", hours=1)

Same template, different values!
'''

# How It Works
'''
Template created:
"User: {name}, Task: {task}, Hours: {hours}"
         ↓
Variables identified:
{name}, {task}, {hours}
         ↓
format() called:
name="Ali", task="study", hours=2
         ↓
Template filled:
"User: Ali, Task: study, Hours: 2"
         ↓
Sent to LLM     
'''

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key="your_api_key_here"
)

# create a reusable template
template_simple = "Explain {topic} to {name} in simple terms"
prompt_simple = PromptTemplate.from_template(template_simple)

# use template with different values
prompt1 = prompt_simple.format(topic="Ali",name="Python")

print("Template 1 filled:")
print(prompt1)

template_complex = """
You are a helpful study assistant.
Student: {student_name}
Subject: {subject}
Level: {level}
Time available: {hours} hours

Create a study plan for this student.
"""

prompt_complex = PromptTemplate(
    input_variables=["student_name", "subject", "level", "hours"],
    template = template_complex
)
filled_prompt = prompt_complex.format(
    student_name="Ali",
    subject="Python",
    level="beginner",
    hours=10
)

print("Complex template filled:")
print(filled_prompt)


# METHOD 3: Use Template with LLM

# Create template
template = "Question: {question}\nAnswer in one sentence:"
prompt_template = PromptTemplate.from_template(template)

def ask_question(question : str):

    # Fill template with actual question
    filled_template = prompt_template.format(question=question)

    # send to llm
    response = llm.envoke(filled_prompt)

    # return answer
    return response.content

answer1 = ask_question("What is Python?")
print("Question 1: What is Python?")
print(f"Answer: {answer1}\n")
