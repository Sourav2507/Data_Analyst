import os
import requests
import traceback
from dotenv import load_dotenv

# Load AI Pipe token from .env file
load_dotenv()
AI_PIPE_TOKEN = os.getenv("AI_PIPE_TOKEN")

if not AI_PIPE_TOKEN:
    raise RuntimeError("AI_PIPE_TOKEN is missing. Add it to your .env file.")

# Correct AI Pipe API endpoint from documentation
AI_PIPE_URL = "https://aipipe.org/openrouter/v1/chat/completions"

SYSTEM_PROMPT = """
You are a Python data analysis assistant.
Generate ONLY valid Python code that solves the given task.
Always set the final output in a variable named 'result'.
Do not use print statements, just set result.

You may use these libraries:
requests, pandas, matplotlib, seaborn, duckdb, bs4, json, base64, io, numpy, scipy, statsmodels

When converting text to numbers, ALWAYS use:
pd.to_numeric(..., errors='coerce')
This prevents errors from non-numeric values.
If numeric conversion fails, drop NaN values before calculations.

If scraping tables, always:
- Strip column names
- Handle missing or malformed rows gracefully
- Coerce numeric columns safely

If plotting, return the image as a base64 string in 'result'.
"""

def clean_code(code: str) -> str:
    """Remove markdown fences and language hints from LLM output."""
    code = code.strip()
    if code.startswith("```"):
        code = code.strip("`")
        if code.lower().startswith("python"):
            code = code[len("python"):].strip()
    return code

def run_agent(task_text):
    headers = {
        "Authorization": f"Bearer {AI_PIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4.1-nano",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task_text}
        ]
    }

    raw_code = ""
    cleaned_code = ""

    try:
        # Call AI Pipe API
        response = requests.post(AI_PIPE_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        raw_code = response.json()["choices"][0]["message"]["content"]
        cleaned_code = clean_code(raw_code)

        exec_globals = {}
        try:
            exec(cleaned_code, exec_globals)
        except SyntaxError:
            cleaned_code = clean_code(cleaned_code)
            exec(cleaned_code, exec_globals)

        result = exec_globals.get("result", None)

        return result, {"raw_code": raw_code, "cleaned_code": cleaned_code}, None

    except Exception as e:
        return None, {"raw_code": raw_code, "cleaned_code": cleaned_code}, f"{e}\n{traceback.format_exc()}"
