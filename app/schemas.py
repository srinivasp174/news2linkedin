from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class GeneratePostRequest(BaseModel):
    topic: str

class GeneratePostResponse(BaseModel):
    topic: str
    news_sources: List[HttpUrl]
    linkedin_post: str
    image_suggestion: Optional[str] = None
