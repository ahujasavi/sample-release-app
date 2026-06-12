"""Simple inventory REST API — used as the demo app for CI/CD walkthrough."""

from flask import Flask, jsonify, request
from src.utils import calculate_reorder_point

app = Flask(__name__)

_inventory = {
    "SKU-001": {"name": "Widget A", "qty": 100, "reorder_threshold": 20},
    "SKU-002": {"name": "Gadget B", "qty": 45,  "reorder_threshold": 10},
}


@app.get("/health")
def health():
    return jsonify({"status": "ok", "version": _get_version()})


@app.get("/inventory")
def list_inventory():
    return jsonify({"items": list(_inventory.values()), "count": len(_inventory)})


@app.get("/inventory/<sku>")
def get_item(sku: str):
    item = _inventory.get(sku)
    if not item:
        return jsonify({"error": f"{sku} not found"}), 404
    reorder_point = calculate_reorder_point(item["reorder_threshold"])
    return jsonify({**item, "reorder_point": reorder_point, "needs_reorder": item["qty"] <= reorder_point})


@app.post("/inventory/<sku>/adjust")
def adjust_qty(sku: str):
    item = _inventory.get(sku)
    if not item:
        return jsonify({"error": f"{sku} not found"}), 404
    delta = request.json.get("delta", 0)
    item["qty"] = max(0, item["qty"] + delta)
    return jsonify({"sku": sku, "new_qty": item["qty"]})


def _get_version() -> str:
    try:
        with open("VERSION") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
