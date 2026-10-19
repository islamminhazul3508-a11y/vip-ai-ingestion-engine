from core.stealth_session import StealthSessionManager
from core.extractor import PrivateAPIExtractor
from core.resilience import SelfHealingEngine
from core.normalizer import AIVectorNormalizer
from core.security import ZeroTrustSecurityManager
from core.telemetry import TelemetryAuditor
from rich import print


def run_full_stack_engine():
    print("[bold magenta]====================================================[/bold magenta]")
    print("[bold magenta]    VIP AI DATA INGESTION ENGINE - FULL RUNTIME    [/bold magenta]")
    print("[bold magenta]====================================================[/bold magenta]")

    # 1. Initialize Engines
    telemetry = TelemetryAuditor()
    security = ZeroTrustSecurityManager()
    session_engine = StealthSessionManager()
    extractor = PrivateAPIExtractor(session_manager=session_engine)
    healing_engine = SelfHealingEngine(max_retries=2, backoff_factor=1.0)
    normalizer = AIVectorNormalizer(source_name="Enterprise_Client_Alpha")

    # 2. Extract Data via Stealth + Self-Healing
    target_api_url = "https://jsonplaceholder.typicode.com/posts/4"
    telemetry.log_event("EXTRACTION_START", {"target": target_api_url})

    raw_payload = healing_engine.execute_with_healing(
        primary_func=lambda: extractor.fetch_endpoint(target_api_url),
        context_name="Live API Fetch"
    )

    # 3. Layer 4 AI Normalization
    ai_doc = normalizer.to_ai_document(raw_payload, text_fields=["title", "body"])
    telemetry.log_event("NORMALIZATION_COMPLETE", {"doc_id": ai_doc["id"]})

    # 4. Layer 5 Zero-Trust Signing & Verification
    signature = security.sign_payload(ai_doc)
    is_valid = security.verify_payload(ai_doc, signature)
    ai_doc["signature"] = signature

    telemetry.log_event("SECURITY_INTEGRITY_CHECK", {"verified": is_valid, "sig": signature[:12] + "..."}, status="SUCCESS")

    print("\n[bold green][FINAL OUTPUT] Enterprise Ready Ingestion Stream:[/bold green]")
    print(ai_doc)


if __name__ == "__main__":
    run_full_stack_engine()
