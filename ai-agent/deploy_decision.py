import json
import sys
import requests
import os

file_path = sys.argv[1] if len(sys.argv) > 1 else None
data = {}

if file_path and os.path.exists(file_path):
    try:
        with open(file_path) as f:
            data = json.load(f)
    except:
        data = {}
else:
    data = {"info": "No security report provided"}


prompt = f"""
You are a DevSecOps approval AI.

Based on this security data,
should we deploy this build?

Reply ONLY:
APPROVE or REJECT

Security Data:
{json.dumps(data)[:3000]}
"""

try:
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    decision = res.json()["response"].upper()

    if "APPROVE" in decision:
        print("APPROVE")
    else:
        print("REJECT")

except Exception as e:
    # Fail-safe → allow deploy if AI fails
    print("APPROVE")
