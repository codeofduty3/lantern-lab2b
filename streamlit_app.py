"""LANTERN Explorer: Streamlit UI for the Vercel-hosted read-only API.

Run locally:

    LANTERN_API_URL=http://127.0.0.1:8000/api streamlit run streamlit_app.py

Streamlit Community Cloud uses the same app. Set ``LANTERN_API_URL`` to the
deployed API in the app secrets.
"""

from __future__ import annotations

import os
from typing import Any

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components


DEFAULT_API = os.environ.get(
    "LANTERN_API_URL", "https://lantern-lab2b.vercel.app/api"
).rstrip("/")
TIMEOUT = float(os.environ.get("LANTERN_API_TIMEOUT", "30"))
CODELAB_URL = "https://lantern-cs2b-codelab.vercel.app"

st.set_page_config(
    page_title="LANTERN Explorer",
    page_icon="🏮",
    layout="wide",
)


class ApiError(RuntimeError):
    """A readable error returned by the LANTERN API."""


def api_base() -> str:
    try:
        secret = st.secrets.get("LANTERN_API_URL", "")
    except Exception:
        secret = ""
    return (
        st.session_state.get("api_url")
        or secret
        or DEFAULT_API
    ).rstrip("/")


@st.cache_data(ttl=300, show_spinner=False)
def get_json(url: str) -> Any:
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise ApiError(f"Could not reach the API: {exc}") from exc
    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        if isinstance(detail, dict):
            detail = detail.get("message") or str(detail)
        raise ApiError(f"{response.status_code}: {detail}")
    return response.json()


def api(path: str) -> Any:
    return get_json(f"{api_base()}{path}")


def money(value: float | None, compact: bool = False) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    if compact:
        for divisor, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
            if abs(value) >= divisor:
                return f"${value / divisor:,.1f}{suffix}"
    return f"${value:,.0f}"


def percent(value: float | None, signed: bool = False) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    text = f"{value:.1%}"
    return f"+{text}" if signed and value > 0 else text


def coverage_page() -> None:
    coverage = api("/coverage")
    filings = api("/filings")["filings"]

    st.title("See the holdings behind the number")
    st.write(
        "Project LANTERN reconciles BDC schedules of investments to each "
        "fund's reported fair value. Every admitted holding remains traceable "
        "to its filing, source rows, and cleaning decision."
    )
    st.warning(
        f"Coverage is not 100%: {coverage['filings_admitted']:,} of "
        f"{coverage['filings_attempted']:,} filings "
        f"({percent(coverage['share_of_filings'])}) and "
        f"{money(coverage['filed_fv_admitted'], True)} of "
        f"{money(coverage['filed_fv_attempted'], True)} filed fair value "
        f"({percent(coverage['share_of_dollars'])}) are represented."
    )

    columns = st.columns(4)
    columns[0].metric(
        "Filings admitted",
        f"{coverage['filings_admitted']:,}",
        percent(coverage["share_of_filings"]),
    )
    columns[1].metric(
        "Filings attempted",
        f"{coverage['filings_attempted']:,}",
        f"{coverage['filings_attempted'] - coverage['filings_admitted']} excluded",
        delta_color="off",
    )
    columns[2].metric(
        "Filed FV admitted",
        money(coverage["filed_fv_admitted"], True),
        percent(coverage["share_of_dollars"]),
    )
    columns[3].metric(
        "No SOI rows",
        f"{coverage['filings_without_soi_rows']:,}",
        "reported separately",
        delta_color="off",
    )

    st.subheader("Largest admitted schedules")
    admitted = sorted(
        (item for item in filings if item["admitted"]),
        key=lambda item: item["filed_fv"] or 0,
        reverse=True,
    )[:10]
    table = pd.DataFrame(
        {
            "BDC": [item["name"] for item in admitted],
            "Accession": [item["adsh"] for item in admitted],
            "Holdings FV": [money(item["holdings_fv"]) for item in admitted],
            "Filed FV": [money(item["filed_fv"]) for item in admitted],
            "Gap": [percent(item["gap_pct"], signed=True) for item in admitted],
            "SEC filing": [item["edgar_url"] for item in admitted],
        }
    )
    st.dataframe(
        table,
        hide_index=True,
        width="stretch",
        column_config={
            "SEC filing": st.column_config.LinkColumn(
                "SEC filing", display_text="Open filing"
            )
        },
    )


def filing_detail(filing: dict) -> None:
    st.header(filing["name"])
    st.caption(
        f"{filing['form']} · {filing['period']} · `{filing['adsh']}`"
    )
    st.markdown(f"[Open the SEC filing]({filing['edgar_url']})")

    metrics = st.columns(4)
    metrics[0].metric("Holdings", f"{filing['n_holdings']:,}")
    metrics[1].metric("Holdings FV", money(filing["holdings_fv"], True))
    metrics[2].metric("Filed FV", money(filing["filed_fv"], True))
    metrics[3].metric("Gap", percent(filing["gap_pct"], signed=True))

    if not filing["admitted"]:
        triage = next(
            (
                item
                for item in api("/triage")["triage"]
                if item["adsh"] == filing["adsh"]
            ),
            None,
        )
        st.error(
            "This filing was attempted but remains outside the panel. "
            "It was not forced into scope."
        )
        if triage:
            st.markdown(f"**Category:** `{triage['triage_category']}`")
            st.markdown(f"**Evidence:** {triage['evidence']}")
            st.markdown(f"**Example:** `{triage['example']}`")
            st.markdown(f"**Why it remains excluded:** {triage['fix']}")
        return

    document = api(f"/filings/{filing['adsh']}/holdings")
    search = st.text_input(
        "Filter holdings",
        placeholder="Borrower, investment type, industry, or source row",
    )
    rows = document["holdings"]
    if search:
        needle = search.casefold()
        rows = [
            row
            for row in rows
            if needle
            in " ".join(
                str(row.get(field) or "")
                for field in (
                    "identifier",
                    "investment_type",
                    "industry",
                    "security_class",
                    "affiliation_category",
                    "source_rows",
                )
            ).casefold()
        ]

    table = pd.DataFrame(
        {
            "Holding": [row["identifier"] for row in rows],
            "Type": [row.get("investment_type") or "n/a" for row in rows],
            "Security": [row.get("security_class") or "other" for row in rows],
            "Fair value": [money(row.get("fair_value")) for row in rows],
            "Cost": [money(row.get("cost")) for row in rows],
            "Principal": [money(row.get("principal")) for row in rows],
            "SOI rows": [row.get("source_rows") for row in rows],
        }
    )
    st.caption(f"{len(rows):,} holdings shown")
    st.dataframe(table, hide_index=True, width="stretch", height=520)


def filings_page() -> None:
    filings = api("/filings")["filings"]
    st.title("Attempted filings")
    st.write(
        "Every filing with SOI rows remains visible, whether or not it falls "
        "inside the panel's reconciliation tolerance."
    )

    left, middle, right = st.columns([2, 1, 2])
    query = left.text_input("Search name, accession, or category")
    state = middle.selectbox("Status", ["All", "Admitted", "Excluded"])
    categories = sorted(
        {item["triage_category"] for item in filings if not item["admitted"]}
    )
    category = right.selectbox("Exclusion category", ["All", *categories])
    admitted_filter = {"All": None, "Admitted": True, "Excluded": False}[state]
    needle = query.casefold().strip()
    visible = [
        item
        for item in filings
        if (admitted_filter is None or item["admitted"] == admitted_filter)
        and (category == "All" or item["triage_category"] == category)
        and (
            not needle
            or needle
            in f"{item['name']} {item['adsh']} {item['triage_category'] or ''}".casefold()
        )
    ]
    table = pd.DataFrame(
        {
            "BDC": [item["name"] for item in visible],
            "Accession": [item["adsh"] for item in visible],
            "Holdings FV": [money(item["holdings_fv"]) for item in visible],
            "Filed FV": [money(item["filed_fv"]) for item in visible],
            "Gap": [percent(item["gap_pct"], signed=True) for item in visible],
            "Status": ["Admitted" if item["admitted"] else "Excluded" for item in visible],
            "Category": [item["triage_category"] or "—" for item in visible],
        }
    )
    st.caption(f"{len(visible):,} of {len(filings):,} attempted filings")
    st.dataframe(table, hide_index=True, width="stretch", height=420)

    if not visible:
        return
    labels = {f"{item['name']} · {item['adsh']}": item for item in visible}
    choice = st.selectbox("Inspect filing", list(labels))
    filing_detail(labels[choice])


def excluded_page() -> None:
    triage = api("/triage")["triage"]
    st.title("Excluded filings and evidence")
    st.write(
        "Coverage gaps stay explicit. Each excluded filing has a category, "
        "reconciliation evidence, an example, and a reason or remaining fix."
    )
    category = st.selectbox(
        "Category", ["All", *sorted({item["triage_category"] for item in triage})]
    )
    query = st.text_input("Search excluded filings")
    visible = [
        item
        for item in triage
        if (category == "All" or item["triage_category"] == category)
        and (
            not query
            or query.casefold()
            in f"{item['name']} {item['adsh']} {item['evidence']}".casefold()
        )
    ]
    table = pd.DataFrame(
        {
            "BDC": [item["name"] for item in visible],
            "Accession": [item["adsh"] for item in visible],
            "Gap": [percent(item["gap_pct"], signed=True) for item in visible],
            "Category": [item["triage_category"] for item in visible],
        }
    )
    st.dataframe(table, hide_index=True, width="stretch", height=320)
    if not visible:
        return
    labels = {f"{item['name']} · {item['adsh']}": item for item in visible}
    item = labels[st.selectbox("Open triage evidence", list(labels))]
    st.subheader(item["name"])
    st.markdown(f"**Gap:** {percent(item['gap_pct'], signed=True)}")
    st.markdown(f"**Category:** `{item['triage_category']}`")
    st.markdown(f"**Evidence:** {item['evidence']}")
    st.markdown(f"**Example:** `{item['example']}`")
    st.markdown(f"**Fix or reason:** {item['fix']}")
    st.markdown(f"[Open the SEC filing]({item['edgar_url']})")


def method_page() -> None:
    rules = api("/cleaning-rules")["rules"]
    st.title("Method")
    st.write(
        "Transformations and structural rules run in the order shown below. "
        "Coverage is calculated after a rule is chosen; it is not used to tune "
        "the rule."
    )
    for index, rule in enumerate(rules, start=1):
        with st.expander(
            f"{index}. {rule['rule']} · {rule['rows_affected']:,} rows",
            expanded=index <= 2,
        ):
            st.markdown(f"**Motivation:** {rule['motivation']}")
            st.markdown(f"**Artifact:** {rule['artifact']}")
            st.markdown(
                f"**Example:** `{rule['example_adsh']}` / "
                f"SOI row `{rule['example_soi_row']}`"
            )
            st.markdown(
                "**Logged coverage:** "
                f"{percent(rule['coverage_before'])} → "
                f"{percent(rule['coverage_after'])}"
            )


def codelab_page() -> None:
    st.title("Project LANTERN codelab")
    st.write(
        "Follow the public, step-by-step tutorial from SEC ZIP files through "
        "the panel, reconciliation, verification, DVC, and serving layers."
    )
    st.link_button("Open the codelab", CODELAB_URL, width="stretch")
    components.iframe(CODELAB_URL, height=900, scrolling=True)


def main() -> None:
    st.sidebar.title("🏮 LANTERN Explorer")
    st.session_state.setdefault("api_url", DEFAULT_API)
    st.sidebar.text_input("API base URL", key="api_url")

    try:
        coverage = api("/coverage")
    except ApiError as exc:
        st.error(str(exc))
        st.stop()

    st.sidebar.success(
        f"2026 Q3 · {coverage['filings_attempted']:,} attempted filings"
    )
    st.sidebar.caption(
        f"{coverage['filings_admitted']:,} admitted · "
        f"{percent(coverage['share_of_dollars'])} of filed dollars"
    )
    page = st.sidebar.radio(
        "Explore",
        ["Coverage", "Filings", "Excluded", "Method", "Codelab"],
    )
    st.sidebar.divider()
    api_root = api_base().removesuffix("/api")
    st.sidebar.markdown(
        f"[API documentation]({api_root}/docs)  \n"
        f"[Codelab]({CODELAB_URL})"
    )
    st.sidebar.caption(
        "Coverage is not 100%. This app is read-only and does not perform "
        "cross-BDC borrower matching."
    )

    {
        "Coverage": coverage_page,
        "Filings": filings_page,
        "Excluded": excluded_page,
        "Method": method_page,
        "Codelab": codelab_page,
    }[page]()


if __name__ == "__main__":
    main()
