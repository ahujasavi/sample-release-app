"""Shared business logic utilities."""


def calculate_reorder_point(threshold: int, safety_factor: float = 1.5) -> int:
    """Reorder point = threshold × safety factor, rounded up."""
    return int(threshold * safety_factor)


def format_sku(raw: str) -> str:
    return raw.strip().upper().replace(" ", "-")
