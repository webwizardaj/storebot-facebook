
import hmac
import json
import logging
import os
from http.server import BaseHTTPRequestHandler

from auto_publish import main


class handler(BaseHTTPRequestHandler):

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # Health check only; does not publish anything.
        self.send_json(200, {
            "status": "ok",
            "message": "StoreBot publishing API is online."
        })

    def do_POST(self):
        expected_secret = os.getenv("PUBLISH_SECRET", "")
        supplied_secret = self.headers.get("Authorization", "")

        if (
            not expected_secret
            or not hmac.compare_digest(
                supplied_secret,
                f"Bearer {expected_secret}"
            )
        ):
            self.send_json(401, {"error": "Unauthorized"})
            return

        try:
            result = main()

            self.send_json(200, {
                "success": True,
                "message": "Publishing workflow completed.",
                "result": result
            })

        except Exception:
            # Log the traceback for debugging without exposing it to callers.
            logging.exception("StoreBot publishing workflow failed")

            self.send_json(500, {
                "success": False,
                "error": "Publishing failed. Check Vercel function logs."
            })


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
