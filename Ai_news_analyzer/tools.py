from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import json
load_dotenv()


llm = ChatOpenAI(
    model="deepseek/deepseek-chat-v3.1"
    api_key = os.getenv("OPENROUTER_API_KEY"),
)


# SEARCH NEWS 
def search_news_with_llm(query: str) -> list:
    """
    Use LLM to generate realistic news articles
    
    Why: Simulate real news search without external API
         LLM creates realistic news data
    """
    
    prompt = f"""
    Generate 5 realistic AI news articles about: {query}
    
    For each article provide:
    - Title (realistic headline)
    - URL (realistic URL)
    - Summary (2-3 sentences)
    - Source (like OpenAI, Google, TechCrunch, etc)
    
    Format as JSON list:
    [
        {{"title": "...", "url": "...", "summary": "...", "source": "..."}},
        ...
    ]
    
    Return ONLY the JSON, no other text.
    """
    
    response = llm.invoke(prompt)
    
    try:
        articles = json.loads(response.content)
        return articles
    except:
        # Fallback if JSON parsing fails
        return [
            {
                "title": "OpenAI Releases New Model",
                "url": "https://openai.com",
                "summary": "Latest AI breakthrough",
                "source": "OpenAI"
            }
        ]

# SUMMARIZE NEWS 
def summarize_news_with_llm(articles: list) -> str:
    """
    Use LLM to create overall summary
    
    Why: Condense all articles into key insights
         Uses LLM's understanding, not just text extraction
    """
    
    articles_text = "\n".join([
        f"- {a['title']}: {a['summary']}"
        for a in articles
    ])
    
    prompt = f"""
    Summarize these AI news articles in 2-3 sentences:
    
    {articles_text}
    
    Focus on: Main trends, key developments, overall importance
    """
    
    response = llm.invoke(prompt)
    return response.content

# CHECK CREDIBILITY 
def check_credibility_with_llm(articles: list) -> str:
    """
    Use LLM to assess news credibility
    
    Why: LLM evaluates source reputation and claim validity
         More intelligent than simple rules
    """
    
    articles_text = "\n".join([
        f"- {a['source']}: {a['title']}"
        for a in articles
    ])
    
    prompt = f"""
    Rate the credibility of these AI news sources and claims:
    
    {articles_text}
    
    Consider:
    - Source reputation 
    - Claim plausibility
    - Common misinformation patterns
    
    Return: "Highly Reliable", "Mixed", or "Needs Verification"
    """
    
    response = llm.invoke(prompt)
    return response.content.strip()

