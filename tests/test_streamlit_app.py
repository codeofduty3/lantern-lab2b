"""Regression tests for the Streamlit frontend."""

from __future__ import annotations

from pathlib import Path

import requests
from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


class _CoverageResponse:
    status_code = 200

    @staticmethod
    def json() -> dict:
        return {
            "filings_attempted": 177,
            "filings_admitted": 88,
            "share_of_filings": 0.497,
            "filed_fv_attempted": 556_908_483_659.0,
            "filed_fv_admitted": 234_366_032_543.0,
            "share_of_dollars": 0.421,
            "filings_without_soi_rows": 5,
        }


class _FilingsResponse:
    status_code = 200

    @staticmethod
    def json() -> dict:
        return {"filings": []}


def test_streamlit_codelab_page_renders(monkeypatch):
    monkeypatch.setenv("LANTERN_API_URL", "https://api.example.test/api")

    def fake_get(url, **_kwargs):
        if url.endswith("/filings"):
            return _FilingsResponse()
        return _CoverageResponse()

    monkeypatch.setattr(
        requests,
        "get",
        fake_get,
    )

    app = AppTest.from_file(
        str(ROOT / "streamlit_app.py"),
        default_timeout=30,
    ).run()
    assert not app.exception

    app.sidebar.radio[0].set_value("Codelab").run()
    assert not app.exception
