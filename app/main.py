from fastapi import FastAPI, HTTPException
from .schemas import GeneratePostRequest, GeneratePostResponse
from .agent import build_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import re
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Demanual AI - LinkedIn Post Generator",
    description="Generate LinkedIn-style posts from recent news using Google Gemini + LangChain",
    version="0.2.0",
)

# Initialize the news search agent once
agent = build_agent()

# Initialize Gemini LLM for post generation
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_output_tokens=1024,
)


@app.post("/generate-post", response_model=GeneratePostResponse)
async def generate_post(req: GeneratePostRequest):
    topic = req.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="topic is required")

    search_prompt = (
        f"Find the most recent (last 7 days) reputable news about: '{topic}'. "
        "Return article titles and URLs."
    )
    try:
        raw_search = agent.run(f"news_search: {search_prompt}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

    # Extract URLs from agent output
    urls = re.findall(r"https?://\S+", raw_search)
    news_sources = list(dict.fromkeys([u.rstrip(".,)") for u in urls]))[:5]

    summary_prompt = (
        f"Create a LinkedIn-style post about '{topic}' using the following recent news sources:"
        f"{news_sources}"+
        """Guidelines:
        - Tone: professional, insightful, and engaging; suitable for a LinkedIn audience.
        - Structure:
            1. Hook sentence to capture attention.
            2. 2-3 bullet points summarizing key insights, trends, or actionable takeaways.
            3. Call to action encouraging discussion, feedback, or engagement.
        - Keep the post concise and readable, but do not strictly limit the length; focus on clarity and flow.
        - Include 2-3 relevant hashtags at the end.
        - Optionally, suggest a professional, royalty-free image related to the topic.

        Ensure the post feels human-written, informative, and encourages interaction from readers."""

    )
    try:
        linkedin_post = llm.predict(summary_prompt)  # Direct LLM call avoids ReAct parsing errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Post generation failed: {e}")

    return GeneratePostResponse(
        topic=topic,
        news_sources=news_sources,
        linkedin_post=linkedin_post.strip(),
        image_suggestion=f"Royalty-free image of {topic}, professional context",
    )


# Only needed for Vercel deployment
from mangum import Mangum

handler = Mangum(app)
