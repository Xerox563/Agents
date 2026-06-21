from openai import OpenAI
from src.config.settings import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL, MAX_ITERATIONS
from src.agent.llm_utils import openrouter_completion_with_retry
from src.tools.task_tools import (
    get_all_tasks, 
    check_deadlines, 
    prioritize_tasks, 
    schedule_task, 
    mark_complete
)

# Initialize client for OpenRouter
client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# ============================================
# AGENT BRAIN: Thinking & Decision Making
# ============================================

def agent_think_and_decide(user_request: str):
    """
    Agent reads user request and decides what to do
    
    Why: This is the "brain" - makes decisions
    """
    
    # Step 1: Create prompt for LLM
    tools_available = """
    Available tools:
    1. get_all_tasks() - Get all pending tasks
    2. check_deadlines() - Show tasks by deadline
    3. prioritize_tasks() - Rank tasks by urgency
    4. schedule_task(task_name) - Suggest schedule for task
    5. mark_complete(task_name) - Mark task as done
    """
    
    prompt = f"""
    User request: {user_request}
    
    {tools_available}
    
    Think about what tools you need to use.
    What should you do first? What next?
    
    Format your response as:
    THOUGHT: [What do I need to do?]
    ACTION: [Which tool to use?]
    
    Examples:
    - For "organize my tasks": use get_all_tasks, then check_deadlines, then prioritize_tasks
    - For "I finished a task": use mark_complete, then get_all_tasks
    - For "what are deadlines": use check_deadlines
    """
    
    # Step 2: Send to LLM and get decision
    try:
        response = openrouter_completion_with_retry(
            client=client,
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            extra_headers={
                "HTTP-Referer": "https://github.com/your-repo", # Optional, for OpenRouter rankings
                "X-Title": "Task Manager Agent", # Optional, for OpenRouter rankings
            }
        )
        decision = response.choices[0].message.content
    except Exception as e:
        return [], f"Error connecting to OpenRouter: {str(e)}"
    
    # Step 3: Print what agent decided
    print("\n🧠 AGENT THINKING:")
    print(decision)
    
    # Step 4: Extract tools from decision
    tools_to_use = []
    
    if "get_all_tasks" in decision:
        tools_to_use.append("get_all_tasks")
    if "check_deadlines" in decision:
        tools_to_use.append("check_deadlines")
    if "prioritize_tasks" in decision:
        tools_to_use.append("prioritize_tasks")
    if "schedule_task" in decision:
        tools_to_use.append("schedule_task")
    if "mark_complete" in decision:
        tools_to_use.append("mark_complete")
    
    return tools_to_use, decision


# ============================================
# EXECUTE TOOLS (Agent takes action)
# ============================================

def execute_tools(tools_list: list, user_request: str):
    """
    Execute the tools agent decided to use
    """
    
    results = []
    
    print("\n⚙️ EXECUTING TOOLS:")
    
    for tool in tools_list:
        print(f"\n  Running: {tool}...")
        
        if tool == "get_all_tasks":
            result = get_all_tasks()
            results.append(result)
        
        elif tool == "check_deadlines":
            result = check_deadlines()
            results.append(result)
        
        elif tool == "prioritize_tasks":
            result = prioritize_tasks()
            results.append(result)
        
        elif tool == "schedule_task":
            # Try to extract task name from user request
            # Simple approach: just schedule first urgent task
            result = schedule_task("Reply to emails")
            results.append(result)
        
        elif tool == "mark_complete":
            # Extract task name from request
            if "finished" in user_request.lower():
                # Very simple extraction logic for demo purposes
                task_name = "Buy groceries"  # Default
                result = mark_complete(task_name)
            else:
                result = "No task to mark complete"
            results.append(result)
    
    return results


# ============================================
# COMBINE RESULTS INTO ANSWER
# ============================================

def format_agent_answer(results: list):
    """
    Combine all tool results into final answer
    """
    
    answer = "\n" + "="*50
    answer += "\n🤖 AGENT'S ORGANIZED ANSWER\n"
    answer += "="*50 + "\n"
    
    for i, result in enumerate(results, 1):
        answer += f"\n{result}\n"
    
    answer += "\n" + "="*50
    answer += "\n💡 RECOMMENDATIONS:\n"
    answer += "="*50
    answer += "\n• Start with the URGENT tasks first\n"
    answer += "• Check deadlines daily\n"
    answer += "• Mark tasks as you complete them\n"
    
    return answer

# ============================================
# AGENT MAIN LOOP
# ============================================

def agent_loop(user_request: str, max_iterations: int = MAX_ITERATIONS):
    """
    Main agent loop
    """
    
    print(f"\n{'='*50}")
    print(f"👤 USER: {user_request}")
    print(f"{'='*50}")
    
    iteration = 0
    all_results = []
    
    while iteration < max_iterations:
        iteration += 1
        
        print(f"\n🔄 ITERATION {iteration}:")
        
        # Step 1: Agent thinks and decides
        print("\n  1️⃣ Agent thinking...")
        tools_to_use, thinking = agent_think_and_decide(user_request)
        
        if not tools_to_use and "Error" in thinking:
             print(f"     ❌ {thinking}")
             break

        # Step 2: Execute the tools
        print("\n  2️⃣ Executing tools...")
        results = execute_tools(tools_to_use, user_request)
        all_results.extend(results)
        
        # Step 3: Check if done
        print("\n  3️⃣ Checking if done...")
        
        if results and len(results) > 0:
            print("     ✅ Got results! Task complete.")
            break
        else:
            print("     ⏳ Need more information...")
    
    # Format and return final answer
    print(f"\n{'='*50}")
    print("FINAL ANSWER FROM AGENT")
    print(f"{'='*50}")
    
    final_answer = format_agent_answer(all_results)
    print(final_answer)
    
    return final_answer
