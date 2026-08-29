import os

clean_benchmark_code = """import os
import time
import json
import urllib.request
import hashlib

def run_nvidia_live_benchmark():
    # Read API key strictly from environment variables (No hardcoded keys)
    api_key = os.environ.get("NVIDIA_API_KEY", "")
    if not api_key:
        print("[X] ERROR: NVIDIA_API_KEY environment variable is not set.")
        print("[!] Set it using: set NVIDIA_API_KEY=your_key_here")
        return

    endpoint = "https://integrate.api.nvidia.com/v1/chat/completions"
    model = "deepseek-ai/deepseek-v4-f"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    prompts = ["ECP_TEST_PAYLOAD_ALPHA", "ECP_TEST_PAYLOAD_BETA"]

    print("==================================================")
    print("  ECP TITANIUM - NVIDIA CLOUD LIVE BENCHMARK      ")
    print("==================================================")
    print(f"Target Model : {model}")
    print("--------------------------------------------------")

    for idx, payload in enumerate(prompts, start=1):
        body = {
            "model": model,
            "messages": [{"role": "user", "content": payload}],
            "max_tokens": 16
        }
        start = time.perf_counter()
        req = urllib.request.Request(endpoint, data=json.dumps(body).encode('utf-8'), headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req) as resp:
                latency = (time.perf_counter() - start) * 1000
                print(f"Pass {idx} | Latency: {latency:.2f} ms")
        except Exception as e:
            print(f"[X] Pass {idx} Failed: {e}")

if __name__ == "__main__":
    run_nvidia_live_benchmark()
"""

with open("benchmarks/run_benchmark.py", "w", encoding="utf-8") as f:
    f.write(clean_benchmark_code)

if os.path.exists("setup_benchmark.py"):
    os.remove("setup_benchmark.py")

print("[+] Cleaned API keys from codebase.")