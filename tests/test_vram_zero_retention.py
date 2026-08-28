import sys
import os
sys.path.append(os.path.abspath("ecp-titanium-nvidia/src"))

from ecp_runtime import ECPNvidiaRuntime

def test_nvidia_cloud_execution():
    print("[*] Connecting to NVIDIA Cloud Infrastructure (Nemotron-3.5)...")
    runtime = ECPNvidiaRuntime()
    payload = "CONFIDENTIAL_PROMPT_ECP_PROTOTYPE_PING"
    
    result = runtime.process_ephemeral_payload(payload)
    
    print(f"[+] Executed successfully on model: {result['nvidia_model']}")
    print(f"[+] Real Cloud Round-Trip Latency: {result['latency_ms']} ms")
    print(f"[+] Deletion Receipt Signed: {result['deletion_receipt']['payload_sha256']}")

if __name__ == "__main__":
    test_nvidia_cloud_execution()
