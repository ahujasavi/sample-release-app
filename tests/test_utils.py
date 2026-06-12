from src.utils import calculate_reorder_point, format_sku


def test_reorder_point_default_safety():
    assert calculate_reorder_point(20) == 30


def test_reorder_point_custom_safety():
    assert calculate_reorder_point(10, safety_factor=2.0) == 20


def test_format_sku_normalises():
    assert format_sku("  sku 001  ") == "SKU-001"
