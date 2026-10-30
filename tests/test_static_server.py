"""Tests for the separately deployable static UI and codelab server."""

from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

import requests

from serve_web import CODELAB_ROOT, LanternStaticHandler


ROOT = Path(__file__).resolve().parents[1]


def test_static_site_serves_ui_config_codelab_and_health(monkeypatch):
    monkeypatch.setenv("LANTERN_API_BASE", "https://api.example.test/api")
    server = ThreadingHTTPServer(("127.0.0.1", 0), LanternStaticHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        assert "Project LANTERN" in requests.get(base + "/", timeout=10).text
        assert requests.get(base + "/healthz", timeout=10).json()["status"] == "ok"
        config = requests.get(base + "/config.js", timeout=10)
        assert config.status_code == 200
        assert "https://api.example.test/api" in config.text
        codelab = requests.get(base + "/codelab/", timeout=10)
        assert codelab.status_code == 200
        assert "lantern-case-study-2b" in codelab.text
        assert "Part 5" in codelab.text
        assert requests.get(base + "/codelab/%2e%2e/README.md", timeout=10).status_code == 404
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_generated_codelab_metadata_matches_source():
    metadata = json.loads((CODELAB_ROOT / "codelab.json").read_text())
    source = (ROOT / "docs" / "codelab.md").read_text()
    assert metadata["id"] == "lantern-case-study-2b"
    assert "Part 0" in source and "Part 5" in source
