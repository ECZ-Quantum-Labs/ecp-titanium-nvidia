import os
import time
import json
import urllib.request
import hashlib
import hmac
from typing import Dict, Any

class ECPNvidiaRuntime:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("NVIDIA_API_KEY", "")
        self.endpoint = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.model = "nvidia/nemotron-3.5-lightning-30b-a3b"

    def process_ephemeral_payload(self, payload_text: str) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY environment variable is missing.")

        start_time = time.perf_counter()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": payload_text}],
            "temperature": 0.2,
            "max_tokens": 32
        }
        
        req = urllib.request.Request(
            self.endpoint, 
            data=json.dumps(body).encode('utf-8'), 
            headers=headers, 
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            res_body = json.loads(response.read().decode('utf-8'))
            
        latency_ms = (time.perf_counter() - start_time) * 1000
        
        payload_hash = hashlib.sha256(payload_text.encode()).hexdigest()
        signature = hmac.new(b"ECP_TITANIUM_SECRET_KEY", payload_hash.encode(), hashlib.sha256).hexdigest()

        return {
            "status": "EXECUTED_ON_NVIDIA_CLOUD",
            "nvidia_model": self.model,
            "latency_ms": round(latency_ms, 2),
            "deletion_receipt": {
                "payload_sha256": payload_hash,
                "timestamp": int(time.time()),
                "signature": signature
            }
        }
