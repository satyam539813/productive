from dotenv import load_dotenv
load_dotenv()

import os, requests

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY", "")

def get_ai_insight(prompt: str, max_tokens: int = 150):
    """Generate insight via free OpenRouter API"""
    if not OPENROUTER_KEY:
        return "⚠️ Missing OpenRouter key."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "http://localhost:8000",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a productivity expert. Provide concise, specific, and actionable advice based on the user's metrics. Avoid generic platitudes."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens
    }

    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                          headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            content = data["choices"][0]["message"]["content"].strip()
            # Clean up Mistral tokens
            content = content.replace("<s>", "").replace("[B_INST]", "").replace("[/B_INST]", "").strip()
            return content
        else:
            return f"⚠️ API Error {r.status_code}: {r.text[:120]}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
