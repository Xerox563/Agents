from src.agent.brain import agent_loop

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """
    Main function - entry point of program
    
    Why: Organized starting point
    """
    
    print("\n🤖 TASK MANAGER AGENT")
    print("Starting...")
    
    # Test Case 1: Organize tasks
    print("\n" + "#"*50)
    print("# TEST 1: Organize Tasks")
    print("#"*50)
    
    agent_loop("Help me organize my tasks")
    
    # Test Case 2: Check what's urgent
    print("\n\n" + "#"*50)
    print("# TEST 2: What's Urgent?")
    print("#"*50)
    
    agent_loop("What do I need to do today? What's urgent?")
    
    # Test Case 3: Mark task complete
    print("\n\n" + "#"*50)
    print("# TEST 3: Mark Task Complete")
    print("#"*50)
    
    agent_loop("I finished buying groceries")


# ============================================
# RUN PROGRAM
# ============================================

if __name__ == "__main__":
    main()
