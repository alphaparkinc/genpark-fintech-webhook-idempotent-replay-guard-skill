import sys, json
from client import FintechWebhookIdempotentGuard

def main():
    guard = FintechWebhookIdempotentGuard()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(guard.run_benchmark_webhook_guard(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "verify_hmac_signature", "description": "Verify HMAC-SHA256 signature with sliding timestamp window."},
                        {"name": "process_idempotent_webhook", "description": "Process webhook with atomic idempotency locking."},
                        {"name": "run_benchmark_webhook_guard", "description": "Run webhook security benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "verify_hmac_signature":
                    out = guard.verify_hmac_signature(args.get("raw_payload", ""), args.get("signature_header", ""), args.get("secret_key", ""), args.get("current_time"))
                elif tname == "process_idempotent_webhook":
                    out = guard.process_idempotent_webhook(args.get("idempotency_key", ""), args.get("payload_dict", {}))
                elif tname == "run_benchmark_webhook_guard":
                    out = guard.run_benchmark_webhook_guard()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
