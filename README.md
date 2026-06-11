# AgenticAI

Azure Crest Hotel is a Flask-powered multi-agent hotel experience with rooms, dining, and billing.

## Run

```bash
pip install -r requirements.txt
python flask_app.py
```

Open http://127.0.0.1:5000 in your browser.

## LangChain and LangGraph demo

Run a standalone agent demo that shows how LangChain prompt templates and LangGraph orchestration work together:

```bash
python langchain_langgraph_demo.py
```

The demo is deterministic and does not require an API key. It walks through a planning agent, a critic agent, and a presenter agent.

## What it includes

- Booking form with room type, guest count, and stay dates
- Hotel menu with quantities and add-ons
- Live bill preview and server-side recalculation
- Multi-agent breakdown for room guidance, dining, and billing
