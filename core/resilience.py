import time
from typing import Callable, Any, List, Optional
from rich import print


class SelfHealingEngine:
    """
    Layer 3: Self-Healing & Fallback Engine.
    Handles network failures, rate-limits, and reroutes traffic automatically.
    """

    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.5):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def execute_with_healing(
        self,
        primary_func: Callable[[], Any],
        fallback_func: Optional[Callable[[], Any]] = None,
        context_name: str = "Pipeline Operation"
    ) -> Any:
        """Executes operation with exponential backoff and automatic failover."""
        for attempt in range(1, self.max_retries + 1):
            try:
                return primary_func()
            except Exception as exc:
                print(f"[bold yellow][!] {context_name} - Attempt {attempt}/{self.max_retries} failed: {exc}[/bold yellow]")
                if attempt < self.max_retries:
                    sleep_time = self.backoff_factor ** attempt
                    time.sleep(sleep_time)
                else:
                    print("[bold red][CRITICAL] Primary route failed. Triggering Self-Healing Fallback...[/bold red]")
                    if fallback_func:
                        return fallback_func()
                    raise RuntimeError(f"All retries and fallbacks exhausted for {context_name}")
