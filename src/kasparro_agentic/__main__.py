from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, render_template, request

from kasparro_agentic.orchestration import run_agent_workflow

# Resolve project root: .../project/src/kasparro_agentic/__main__.py -> parents[2] is project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = PROJECT_ROOT / "static"

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path="/static",
)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/generate")
def api_generate():
    data = request.get_json(silent=True) or {}
    product_name = str(data.get("productName", "")).strip()
    if not product_name:
        return jsonify({"error": "productName is required"}), 400

    result = run_agent_workflow(product_name)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
