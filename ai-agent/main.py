import sys
import subprocess

def run_script(script, args=None):
    cmd = ["python3", script]
    if args:
        cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout.strip())

def usage():
    print("""
Usage:
python3 main.py <mode> [file]

Modes:
  code        → AI Code Review
  security    → AI Security Review (needs trivy json file)
  deploy      → AI Deployment Approval (needs trivy json file)
  k8s         → AI Kubernetes Review
""")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "code":
        run_script("ai-agent/code_review.py")

    elif mode == "security":
        if len(sys.argv) < 3:
            print("Provide trivy JSON file")
            sys.exit(1)
        run_script("ai-agent/security_review.py", [sys.argv[2]])

    elif mode == "deploy":
        if len(sys.argv) < 3:
            print("Provide trivy JSON file")
            sys.exit(1)
        run_script("ai-agent/deploy_decision.py", [sys.argv[2]])

    elif mode == "k8s":
        run_script("ai-agent/k8s_review.py")

    else:
        usage()