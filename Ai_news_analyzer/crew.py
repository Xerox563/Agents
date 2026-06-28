
# CREWAI: Agents and Tasks

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from tools import search_news_with_llm, summarize_news_with_llm, check_credibility_with_llm
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="deepseek/deepseek-chat-v3.1"
    api_key = os.getenv("OPENROUTER_API_KEY"),
)


# AGENT 1: NEWS COLLECTOR
news_collector = Agent(
    role="News Collector",
    goal="Find latest AI news",
    backstory="Expert news researcher in AI/ML field",
    llm=llm,
    verbose=True
)


# AGENT 2: SUMMARIZER
news_summarizer = Agent(
    role="News Summarizer",
    goal="Create clear concise summaries",
    backstory="Expert at identifying key insights",
    llm=llm,
    verbose=True
)


# AGENT 3: FACT CHECKER
news_verifier = Agent(
    role="Fact Checker",
    goal="Verify news credibility",
    backstory="Expert at assessing source reliability",
    llm=llm,
    verbose=True
)


# TASK 1: COLLECT NEWS
collect_task = Task(
    description="Search for AI news about: {query}",
    expected_output="List of 5 news articles with title, url, summary, source",
    agent=news_collector
)


# TASK 2: SUMMARIZE
summarize_task = Task(
    description="Create overall summary of the news articles",
    expected_output="2-3 sentence summary of main AI news trends",
    agent=news_summarizer
)


# TASK 3: VERIFY CREDIBILITY
verify_task = Task(
    description="Check credibility of news sources and claims",
    expected_output="Credibility assessment: Highly Reliable / Mixed / Needs Verification",
    agent=news_verifier
)


# CREATE CREW
news_crew = Crew(
    agents=[news_collector, news_summarizer, news_verifier],
    tasks=[collect_task, summarize_task, verify_task],
    verbose=True
)

def analyze_with_crew_agents(query: str):
    # running the actual crew ai agents
    result = news_crew.kickoff(
        inputs= {"query": query}
    )
    return result


# EXECUTE FUNCTION
def analyze_news(query: str) -> dict:
    """
    Run crew analysis on news query
    
    Returns: dict with articles, summary, credibility
    """
    
    print(f"🔄 Analyzing: {query}")
    
    # Get articles
    articles = search_news_with_llm(query)
    
    # Summarize
    summary = summarize_news_with_llm(articles)
    
    # Check credibility
    credibility = check_credibility_with_llm(articles)
    
    return {
        "articles": articles,
        "summary": summary,
        "credibility": credibility
    }