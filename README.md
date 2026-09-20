# Drift AI - Autonomous Agent Fleet

This repository contains three production-grade AI agent assignments built using LangGraph, Google Gemini, and Streamlit.

## Architecture Highlights
- **Assignment 1:** A Research Agent with deterministic tool-call limits and failure recovery.
- **Assignment 2:** A strictly linear Worker/Reviewer dyad utilizing Pydantic for guaranteed structured outputs.
- **Assignment 3:** A resumable state machine powered by SQLite checkpointing.

## Quickstart
```bash
uv pip install -r requirements.txt
uv run streamlit run app.py
```

## Docker Support
Run `docker-compose up` to start the fleet.
