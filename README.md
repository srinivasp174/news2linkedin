# Demanual AI - LinkedIn Post Generator

> AI-powered service that generates LinkedIn-style posts from recent news using Google Gemini API and LangChain.

---

## Table of Contents

- [Demanual AI - LinkedIn Post Generator](#demanual-ai---linkedin-post-generator)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [Setup Instructions](#setup-instructions)
  - [API Usage](#api-usage)
    - [Endpoint](#endpoint)
    - [Request Body](#request-body)
    - [Response](#response)
  - [Deployment](#deployment)

---

## Project Overview

This project demonstrates a complete AI workflow for generating professional social media content:

1. Fetches the most recent news on a given topic using a web-accessible LangChain agent.
2. Summarizes and structures the information into a **LinkedIn-style post**.
3. Optionally suggests hashtags and a professional image.

The FastAPI backend exposes a clean `/generate-post` endpoint, making it easy to integrate into other applications or workflows.

---

## Features

* Fetches **recent news articles** on a topic via SerpAPI.
* Generates **LinkedIn-ready posts** using Google Gemini API (via `langchain-google-genai`).
* Structured output: **Hook sentence → Bullet points → Call to action**.
* Optional **image suggestion** and **hashtags** for professional posts.
* Fully **containerized and deployable** on serverless platforms like Vercel.

---

## Tech Stack

* **Backend:** FastAPI 0.118
* **AI:** Google Gemini API via `langchain-google-genai` 2.1.12
* **Search:** SerpAPI
* **Deployment:** Vercel (serverless)
* **Python:** 3.12
* **Environment Variables:** `.env` using `python-dotenv`

---

## Setup Instructions

1. Clone the repo:

```bash
git clone https://github.com/your-username/demanual-ai-postgen.git
cd demanual-ai-postgen
```

2. Create a virtual environment and activate it:

```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:

```
SERPAPI_API_KEY=your_serpapi_key
GOOGLE_API_KEY=your_google_gemini_key
```

5. Run locally:

```bash
uvicorn app.main:app --reload --port 8000
```

6. Open Swagger docs at:

```
http://127.0.0.1:8000/docs
```

---

## API Usage

### Endpoint

```
POST /generate-post
```

### Request Body

```json
{
  "topic": "Artificial Intelligence"
}
```

### Response

```json
{
  "topic": "Artificial Intelligence",
  "news_sources": [
    "https://www.reuters.com/ai-news-article",
    "https://www.nytimes.com/ai-trends"
  ],
  "linkedin_post": "AI is transforming industries... [generated content]",
  "image_suggestion": "Royalty-free image of Artificial Intelligence, professional context"
}
```

---

## Deployment

* Deployed on **Vercel** as a serverless FastAPI function.
* Swagger docs available at `/docs` endpoint of your deployment URL.
* Environment variables managed securely via Vercel settings.

**Example deployed URL:**

```
https://demanual-ai-postgen.vercel.app/docs
```
