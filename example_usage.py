import sys, json
from client import FintechWebhookIdempotentGuard

def main():
    print("Testing FintechWebhookIdempotentGuard...")
    guard = FintechWebhookIdempotentGuard()
    res = guard.run_benchmark_webhook_guard()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["signature_verified"] is True
    assert res["replay_blocked"] is True
    assert res["first_call_status"] == "PROCESSED_SUCCESSFULLY"
    assert res["duplicate_call_status"] == "REPLAY_CACHED_RESULT"
    print("All Fintech Webhook Idempotent Guard tests passed successfully!")

if __name__ == "__main__":
    main()
