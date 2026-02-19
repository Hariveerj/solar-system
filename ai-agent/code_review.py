import subprocess
import requests

# Collect repo files
files = subprocess.getoutput(
    "git ls-files '*.java' '*.yaml' '*.yml' 'Jenkinsfile*'"
).splitlines()

code_data = ""

for f in files:
    try:
        with open(f) as file:
            code_data += file.read()[:800]
    except:
        pass

prompt = f"""
You are a DevOps AI reviewer.

Review this project for:

- Code issues
- Security risks
- CI/CD mistakes
- Kubernetes misconfigurations

Code:
{code_data[:4000]}
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