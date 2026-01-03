from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from kasparro_agentic.orchestration.dag import run_workflow

# --- PATHS (repo structure) ---
# src/app.py
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "kasparro_agentic" / "templates"
STATIC_DIR = BASE_DIR.parent / "static"

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
    """
    Backend endpoint (LangGraph pipeline).
    Note: Your UI can run purely client-side (Puter JS) and may never call this.
    This endpoint is kept stable for demos/tests and ALWAYS returns JSON.
    """
    try:
        data = request.get_json(silent=True) or {}
        product_name = (data.get("productName") or "").strip()
        if not product_name:
            return jsonify({"error": "productName is required"}), 400

        result = run_workflow(product_name)

        # Always JSON-safe
        return jsonify(
            {
                "productName": result.get("productName", product_name),
                "questions": result.get("questions", []),
                "answer": result.get("answer", ""),
                "mode": result.get("mode", os.getenv("KASPARRO_LLM_MODE", "mock")),
                "error": result.get("error"),
            }
        )
    except Exception as e:  # noqa: BLE001
        # Never return HTML (prevents "Unexpected token <" in frontend)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # load_dotenv=False prevents rare startup hangs on some Windows setups
    app.run(host="127.0.0.1", port=5000, debug=True, load_dotenv=False)
