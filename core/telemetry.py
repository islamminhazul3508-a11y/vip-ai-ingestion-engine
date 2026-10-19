import datetime
from typing import Dict, Any
from rich import print


class TelemetryAuditor:
    """
    Layer 6: Telemetry, Audit Logs & Health Dispatcher.
    Maintains immutable execution logs and dispatches system health events.
    """

    @staticmethod
    def log_event(event_type: str, details: Dict[str, Any], status: str = "INFO"):
        """Logs audit metrics and telemetry records."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log_payload = {
            "timestamp": timestamp,
            "event": event_type,
            "status": status,
            "details": details
        }
        
        color = "green" if status == "SUCCESS" else ("yellow" if status == "WARN" else "cyan")
        print(f"[{color}][TELEMETRY - {status}][/{color}] {event_type} | Time: {timestamp}")
        return log_payload
