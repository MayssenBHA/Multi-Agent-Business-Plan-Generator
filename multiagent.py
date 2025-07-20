import os
import time
import requests
from bs4 import BeautifulSoup
from typing import TypedDict, Optional

import google.generativeai as genai
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Utiliser la bonne variable d'environnement pour la clé Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
RAPID_API_KEY = os.getenv("RAPIDAPI_KEY")

# Configurer la clé API Gemini
genai.configure(api_key=GOOGLE_API_KEY)

def agent_a(state):
    company_query = state.get("user_input")

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
You are an intelligent agent that turns a user’s input into a precise Google search query.
Assume the input is a **company or industry name**, not a technical concept.
Just return one clear search query — don't explain.

User input: {company_query}
"""
    search_query = model.generate_content(prompt).text.strip()
    print("🤖 GEMINI SEARCH QUERY:", search_query)

    # Recherche Google via RapidAPI
    url = "https://real-time-web-search.p.rapidapi.com/search-advanced"
    querystring = {
        "q": search_query,
        "gl": "us",
        "hl": "en",
        "autocorrect": "true",
        "num": "10",
        "page": "1"
    }
    headers = {
        "x-rapidapi-host": "real-time-web-search.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY
    }
    res = requests.get(url, headers=headers, params=querystring)
    print("🔍 RapidAPI status code:", res.status_code)
    results = res.json() if res.status_code == 200 else {"data": []}
    links = [item['url'] for item in results.get('data', [])]
    print("🔗 Links fetched:", links)

    # Crawl des pages web
    headers_browser = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    web_content = ""
    for url in links:
        try:
            resp = requests.get(url, headers=headers_browser, timeout=10)
            if "text/html" not in resp.headers.get('Content-Type', ''):
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            web_content += soup.get_text(separator=" ", strip=True)
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
        time.sleep(1.5)

    print("📄 Web Content Preview:\n", web_content[:1000])

    cert_prompt = f"""
From the following company webpage content, give me a Market Research (event, clients) of the company in a detailed text.

Content:
{web_content}
"""
    print("📊 Prompt to Gemini for Market Research:\n", cert_prompt[:1000])

    cert_model = genai.GenerativeModel("gemini-1.5-flash")
    certs = cert_model.generate_content(cert_prompt).text

    state["company_info"] = certs
    return state


def agent_b(state):
    company_info = state.get("company_info")

    prompt = f"""
You are a business strategist. Based on the following market research of a given company, propose a strategic business plan that can beat and outperform them.

Market research info (text):
{company_info}

Output format:
- Summary
- Strategic Opportunities
- Potential Partners
- Suggested Services or Products
- Risks and Recommendations
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(prompt)

    state["business_plan"] = result.text
    return state


# Définition de l'état partagé
class AgentState(TypedDict):
    user_input: str
    company_info: Optional[str]
    business_plan: Optional[str]


# Construction du graphe d'agents
graph = StateGraph(AgentState)

graph.add_node("AgentA", agent_a)
graph.add_node("AgentB", agent_b)

graph.set_entry_point("AgentA")
graph.add_edge("AgentA", "AgentB")
graph.add_edge("AgentB", END)

app = graph.compile()
