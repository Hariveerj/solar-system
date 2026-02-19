import json
import sys
import requests

file_path = sys.argv[1]

data = json.load(open(file_path))

prompt = f"""
Analyze this Trivy security scan.

Provide:

1. Overall risk
2. Critical CVEs
3. Fix suggestions

{json.dumps(data)[:4000]}
"""

res = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }
)

print(res.json()["response"])
