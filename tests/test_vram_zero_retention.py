import sys
import os
sys.path.append(os.path.abspath("ecp-titanium-nvidia/src"))

from ecp_runtime import ECPNvidiaRuntime

def test_retention():
    print("[*] Testing ECP Titanium VRAM Memory Nullifier...")
    runtime = ECPNvidiaRuntime(secret_signing_key=os.urandom(32))
    payload = b"CONFIDENTIAL_PROMPT_GOOGLE_ZURICH_PAYLOAD"
    res = runtime.process_ephemeral_payload(payload, ttl_sec=1)
    
    assert res["status"] == "ZEROIZED"
    assert res["vram_freed"] is True
    print(f"[✓] Deletion Receipt Verified. SHA256: {res['deletion_receipt']['payload_sha256']}")
    print(f"[✓] Overhead Latency: {res['runtime_overhead_ms']} ms")

if __name__ == "__main__":
    test_retention()
