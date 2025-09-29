import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SerpAPIWrapper

def build_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        max_output_tokens=1024,
    )

    serp = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

    tools = [
        Tool(
            name="news_search",
            func=lambda q: serp.run(q + " site:news OR site:reuters.com OR site:nytimes.com"),
            description="Search recent news for a topic. Input should be the query string.",
        )
    ]


    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )

    return agent
