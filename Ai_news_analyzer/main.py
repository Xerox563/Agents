from fastapi import FastAPI
from models import NewsRequest, Article,AnalysisResponse
from crew import analyze_news, analyze_with_crew_agents

# starting the app
app = FastAPI(
    title="AI News Analyzer",
    description="Multi-agent news analysis system"
)

# ENDPOINTS
@app.get("/health")
async def health_check():
    """Check API status"""
    return {"status": "✅ Running"}

@app.post("/analyze")
async def analyze_news_endpoint(request: NewsRequest) -> AnalysisResponse:
    """
    Analyze AI news
    
    Uses LLM for everything:
    - Search news
    - Summarize
    - Check credibility
    """
    print(f"📡 Request: {request.query}")
    
    result = analyze_news(request.query)
    
    articles = [Article(**a) for a in result["articles"]]
    return AnalysisResponse(
        query=request.query,
        articles=articles,
        news_summary=result["summary"],
        credibility_status=result["credibility"]
    )

@app.post("/analyze_with_crew_agents")
def analyze_with_crew_agentts(request: NewsRequest):
   result =  analyze_with_crew_agents(request.query) # Runs crew
   return result

# Run server
if __name__ == "__name__":
    import uvicorn
    uvicorn(app,host="0.0.0.0",port=8000)
