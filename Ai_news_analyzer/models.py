from pydantic import BaseModel
from typing import List


# user request

class NewsRequest(BaseModel):
    #   What user sends to API
    query : str


# news article
class Article(BaseModel):
    title:str
    url:str
    summary:str
    source:str

# API response
class AnalysisResponse(BaseModel):
    # What api returns to the user
    query: str
    articles:List[str]
    news_summary:str
    credibility_status: str  
