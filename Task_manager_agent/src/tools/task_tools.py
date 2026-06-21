from datetime import datetime
from src.database.tasks import tasks_db

# ============================================
# TOOL 1: Get All Tasks
# ============================================

def get_all_tasks():
    """
    Returns all pending tasks
    
    Why: Agent needs to know what tasks exist first
    """
    
    # Get only pending tasks (not done ones)
    pending = [t for t in tasks_db if t["status"] == "pending"]
    
    # Format nicely
    result = "📋 All Pending Tasks:\n"
    for task in pending:
        result += f"  • {task['name']} ({task['hours']} hours)\n"
    
    return result

# ============================================
# TOOL 2: Check Deadlines
# ============================================

def check_deadlines():
    """
    Shows tasks organized by deadline
    
    Why: Agent needs to know which are urgent
    """
    
    today = datetime.strptime("2024-01-15", "%Y-%m-%d")
    
    # Organize by deadline
    today_tasks = []
    tomorrow_tasks = []
    this_week_tasks = []
    no_deadline_tasks = []
    
    for task in tasks_db:
        if task["status"] == "pending":
            if task["deadline"] is None:
                no_deadline_tasks.append(task)
            else:
                due_date = datetime.strptime(task["deadline"], "%Y-%m-%d")
                days_away = (due_date - today).days
                
                if days_away == 0:
                    today_tasks.append(task)
                elif days_away == 1:
                    tomorrow_tasks.append(task)
                elif days_away <= 7:
                    this_week_tasks.append(task)
    
    # Format result
    result = "📅 Deadlines Breakdown:\n"
    
    if today_tasks:
        result += f"\n⚠️ TODAY:\n"
        for t in today_tasks:
            result += f"  • {t['name']}\n"
    
    if tomorrow_tasks:
        result += f"\n🔴 TOMORROW:\n"
        for t in tomorrow_tasks:
            result += f"  • {t['name']}\n"
    
    if this_week_tasks:
        result += f"\n💛 THIS WEEK:\n"
        for t in this_week_tasks:
            result += f"  • {t['name']}\n"
    
    if no_deadline_tasks:
        result += f"\n⭕ NO DEADLINE:\n"
        for t in no_deadline_tasks:
            result += f"  • {t['name']}\n"
    
    return result

# ============================================
# TOOL 3: Prioritize Tasks
# ============================================

def prioritize_tasks():
    """
    Ranks tasks by urgency and importance
    
    Why: Agent needs to know what's most important
    """
    
    today = datetime.strptime("2024-01-15", "%Y-%m-%d")
    
    # Calculate priority score for each task
    scored_tasks = []
    
    for task in tasks_db:
        if task["status"] == "pending":
            score = 0
            
            # Urgent if deadline soon
            if task["deadline"]:
                due_date = datetime.strptime(task["deadline"], "%Y-%m-%d")
                days_away = (due_date - today).days
                
                if days_away <= 0:
                    score += 10  # Due now
                elif days_away == 1:
                    score += 8   # Due soon
                elif days_away <= 7:
                    score += 5   # This week
                else:
                    score += 1   # Later
            else:
                score += 0  # No deadline = low priority
            
            scored_tasks.append({
                "task": task,
                "score": score
            })
    
    # Sort by score (highest first)
    scored_tasks.sort(key=lambda x: x["score"], reverse=True)
    
    # Format result
    result = "🎯 Prioritized Tasks:\n\n"
    
    for i, item in enumerate(scored_tasks, 1):
        task = item["task"]
        score = item["score"]
        
        # Add priority level emoji
        if score >= 8:
            priority = "🔴 URGENT"
        elif score >= 5:
            priority = "🟡 SOON"
        else:
            priority = "🟢 LATER"
        
        result += f"{i}. {task['name']} - {priority}\n"
    
    return result

# ============================================
# TOOL 4: Schedule Task
# ============================================

def schedule_task(task_name):
    """
    Suggests when to do a specific task
    
    Why: Agent needs to create a plan
    """
    
    # Find the task
    task = None
    for t in tasks_db:
        if t["name"].lower() == task_name.lower():
            task = t
            break
    
    if not task:
        return f"❌ Task '{task_name}' not found"
    
    # Suggest schedule based on deadline and hours
    today = datetime.strptime("2024-01-15", "%Y-%m-%d")
    
    if task["deadline"] is None:
        suggested_time = "Whenever you have time"
    else:
        due_date = datetime.strptime(task["deadline"], "%Y-%m-%d")
        days_away = (due_date - today).days
        
        if days_away <= 0:
            suggested_time = "TODAY (URGENT!)"
        elif days_away == 1:
            suggested_time = "Tomorrow morning"
        else:
            suggested_time = f"Within {days_away} days"
    
    result = f"⏰ Schedule for '{task['name']}':\n"
    result += f"  When: {suggested_time}\n"
    result += f"  Duration: {task['hours']} hours\n"
    
    return result

# ============================================
# TOOL 5: Mark Task Complete
# ============================================

def mark_complete(task_name):
    """
    Marks a task as done
    
    Why: Agent needs to update status
    """
    
    # Find and update task
    for task in tasks_db:
        if task["name"].lower() == task_name.lower():
            task["status"] = "done"
            return f"✅ Marked '{task_name}' as complete!"
    
    return f"❌ Task '{task_name}' not found"
