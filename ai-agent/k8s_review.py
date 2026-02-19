import glob
import requests

yamls = glob.glob("k8/**/*.yaml", recursive=True)

data = ""

for y in yamls:
    data += open(y).read()[:800]

prompt = f"""
Review these Kubernetes manifests.

Check for:

- Security risks
- NodePort exposure
- Missing resource limits
- Best practices

{data[:4000]}
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
