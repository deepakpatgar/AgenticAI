# AgenticAI

Flask page that runs a tiny multi-agent meal planner.

## Run

```bash
pip install -r requirements.txt
python flask_app.py
```

Open http://127.0.0.1:5000 in your browser.

## How it works

The idea agent generates options, the critic agent picks the easiest one, and the summarizer agent renders the final recommendation.
