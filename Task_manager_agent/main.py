from openai import OpenAI
from config import OPENAI_API_KEY, MODEL, TODAY, MAX_ITERATIONS

# Initialize client
client = OpenAI(api_key=OPENAI_API_KEY)

# We'll add code here in next steps

if __name__ == "__main__":
    print("Task Manager Agent - Ready to build!")