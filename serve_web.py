#!/usr/bin/env python3
"""Serve the static LANTERN UI and generated codelab on hosts such as Replit."""

from __future__ import annotations

import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
WEB_ROOT = ROOT / "app" / "web"
CODELAB_ROOT = ROOT / "docs" / "lantern-case-study-2b"
DEFAULT_API = "https://lantern-lab2b.vercel.app/api"


class LanternStaticHandler(SimpleHTTPRequestHandler):
    """Serve the UI, generated codelab, and a runtime deployment config."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def translate_path(self, path: str) -> str:
        clean_path = unquote(urlsplit(path).path)
        if clean_path.startswith("/codelab/"):
            relative = clean_path.removeprefix("/codelab/") or "index.html"
            return _safe_path(CODELAB_ROOT, relative)
        return _safe_path(WEB_ROOT, clean_path.lstrip("/") or "index.html")

    def do_GET(self) -> None:
        if urlsplit(self.path).path == "/config.js":
            self._serve_config()
            return
        if urlsplit(self.path).path == "/healthz":
            self._serve_health()
            return
        if self.path == "/codelab":
            self.send_response(302)
            self.send_header("Location", "/codelab/")
            self.end_headers()
            return
        super().do_GET()

    def _serve_config(self) -> None:
        hostname = (urlsplit(f"//{self.headers.get('Host', '')}").hostname or "")
        local_default = (
            "http://127.0.0.1:8000/api"
            if hostname in {"127.0.0.1", "localhost"}
            else DEFAULT_API
        )
        api_base = os.environ.get("LANTERN_API_BASE", local_default).rstrip("/")
        docs_url = os.environ.get("LANTERN_DOCS_URL", "")
        body = {
            "apiBase": api_base,
            "docsUrl": docs_url,
            "codelabUrl": "/codelab/",
        }
        payload = (
            "window.LANTERN_CONFIG = "
            + json.dumps(body, separators=(",", ":"))
            + ";\n"
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _serve_health(self) -> None:
        payload = b'{"status":"ok","service":"lantern-static-ui"}\n'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> None:
    port = int(os.environ.get("PORT", "3000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), LanternStaticHandler)
    print(f"Serving LANTERN UI at http://0.0.0.0:{port}", flush=True)
    server.serve_forever()


def _safe_path(root: Path, relative: str) -> str:
    """Resolve a URL path without allowing traversal outside ``root``."""
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        return str(root / "__not_found__")
    return str(candidate)


if __name__ == "__main__":
    main()
