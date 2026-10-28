
import hmac
import logging
import os

from flask import Flask, jsonify, request
from auto_publish import main

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.get("/")
def health():
    return jsonify({
        "status": "ok",
        "message": "StoreBot publishing API is online."
    })


@app.post("/publish")
def publish():
    expected_secret = os.getenv("PUBLISH_SECRET", "")
    supplied_secret = request.headers.get("Authorization", "")

    if not expected_secret or not hmac.compare_digest(
        supplied_secret, f"Bearer {expected_secret}"
    ):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        result = main()
        return jsonify({
            "success": True,
            "message": "Publishing workflow completed.",
            "result": result
        }), 200

    except Exception:
        logging.exception("StoreBot publishing failed")
        return jsonify({
            "success": False,
            "error": "Publishing failed. Check Render logs."
        }), 500
