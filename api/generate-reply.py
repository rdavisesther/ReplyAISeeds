from http.server import BaseHTTPRequestHandler
import json
import os
import google.generativeai as genai


class handler(BaseHTTPRequestHandler):

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        self._send_json(200, {"ok": True})

    def do_POST(self):
        try:
            api_key = os.environ.get("GEMINI_API_KEY")

            if not api_key:
                self._send_json(500, {
                    "error": "GEMINI_API_KEY is missing in Vercel Environment Variables"
                })
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            data = json.loads(body.decode("utf-8"))
            prompt = data.get("prompt", "").strip()

            if not prompt:
                self._send_json(400, {
                    "error": "Prompt is required"
                })
                return

            genai.configure(api_key=api_key)

            model = genai.GenerativeModel("gemini-1.5-flash")

            response = model.generate_content(prompt)

            reply = response.text.strip() if response.text else ""

            if not reply:
                self._send_json(500, {
                    "error": "Empty response from Gemini"
                })
                return

            self._send_json(200, {
                "reply": reply
            })

        except Exception as e:
            self._send_json(500, {
                "error": str(e)
            })
