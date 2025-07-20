# Multi-Agent-Business-Plan-Generator

This project is a business plan generator powered by a multi-agent system using artificial intelligence. It retrieves information based on a user's request about a company or industry, then automatically generates a tailored business plan using the collected data.

## 🎯 Project Goal
To automate the creation of business plans using a coordinated multi-agent system, leveraging NLP techniques, agent orchestration, and API integration.

## 🏆 Context
This project was developed as part of the Talan SummerCamp 2025.

## ⚙️ Technologies Used
🐍 Python
🕸️ Streamlit (user interface)
🤖 LangChain (agent orchestration)
🌐 RapidAPI (real-time-web-search)
📚 LLMs for text generation
📦 dotenv for API key management

## 🧠 Multi-Agent Architecture
The system includes:

An implicit orchestrator agent managed by LangGraph, coordinating the workflow between agents using a state graph (StateGraph).

Specialized agents:

   - An agent for retrieving company information

   - An agent for generating the business plan
