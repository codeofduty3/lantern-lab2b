"""LANTERN's read-only FastAPI application."""

from __future__ import annotations

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import data_store
from .models import (
    CleaningRulesResponse,
    CoverageResponse,
    ErrorResponse,
    Filing,
    FilingsResponse,
    HealthResponse,
    HoldingsResponse,
    TriageResponse,
)


DESCRIPTION = """
Explore the 2026 Q3 BDC schedule-of-investments release used by Project LANTERN.

Every endpoint is read-only. Coverage is measured in both filings and reported
fair value; it is not 100%. Use the filing endpoints to trace a holding back to
its source SOI rows and the SEC filing.
""".strip()

app = FastAPI(
    title="Project LANTERN API",
    summary="Trace BDC holdings to filings, totals and cleaning decisions.",
    description=DESCRIPTION,
    version="1.0.0",
    contact={
        "name": "Project LANTERN",
        "url": "https://www.sec.gov/data-research/sec-markets-data/bdc-data-sets",
    },
    openapi_tags=[
        {"name": "System", "description": "Service health."},
        {"name": "Coverage", "description": "How much of the release is represented."},
        {"name": "Filings", "description": "Attempted filings and their holdings."},
        {"name": "Triage", "description": "Filings excluded from the panel and why."},
        {"name": "Method", "description": "Ordered cleaning transformations and rules."},
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8001",
        "http://localhost:8001",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def _router(prefix: str = "", include_in_schema: bool = True) -> APIRouter:
    router = APIRouter(prefix=prefix)

    @router.get(
        "/health",
        response_model=HealthResponse,
        tags=["System"],
        summary="Check that the service can read its exported data",
        include_in_schema=include_in_schema,
    )
    def health() -> dict:
        """Return a small readiness response without recomputing any numbers."""
        data_store.coverage()
        return {"status": "ok", "release": "2026q3", "read_only": True}

    @router.get(
        "/coverage",
        response_model=CoverageResponse,
        tags=["Coverage"],
        summary="View filing and dollar coverage",
        include_in_schema=include_in_schema,
        responses={503: {"model": ErrorResponse}},
    )
    def get_coverage() -> dict:
        """Show the copied release coverage from `reports/coverage.json`.

        `share_of_filings` and `share_of_dollars` are kept beside the raw counts
        and dollar totals so a portfolio reader can judge the scope of every
        number in the app.
        """
        return data_store.coverage()

    @router.get(
        "/filings",
        response_model=FilingsResponse,
        tags=["Filings"],
        summary="List every attempted filing",
        include_in_schema=include_in_schema,
    )
    def get_filings() -> dict:
        """Return admitted and excluded filings with copied reconciliation values.

        `holdings_fv` is the panel side of the check, `filed_fv` is the BDC's
        reported total, and `gap_pct` is the relative difference between them.
        """
        return data_store.filings_document()

    return router


def _filing_router(prefix: str = "", include_in_schema: bool = True) -> APIRouter:
    router = APIRouter(prefix=prefix)

    @router.get(
        "/filings/{adsh}",
        response_model=Filing,
        tags=["Filings"],
        summary="View one attempted filing",
        include_in_schema=include_in_schema,
        responses={404: {"model": ErrorResponse}},
    )
    def get_filing(adsh: str) -> dict:
        """Return one filing's coverage row and a direct SEC filing link."""
        item = data_store.filing(adsh)
        if item is None:
            raise _not_found("Filing", adsh)
        return item

    @router.get(
        "/filings/{adsh}/holdings",
        response_model=HoldingsResponse,
        tags=["Filings"],
        summary="View a filing's holdings and source rows",
        include_in_schema=include_in_schema,
        responses={404: {"model": ErrorResponse}},
    )
    def get_holdings(adsh: str) -> dict:
        """Return admitted holdings and each holding's original SOI row numbers.

        The response total is copied from coverage. It is not calculated by
        the API; the app test verifies that it equals the panel total.
        """
        document = data_store.holdings_document(adsh)
        if document is None:
            filing = data_store.filing(adsh)
            if filing is None:
                raise _not_found("Filing", adsh)
            raise _not_found(
                "Holdings",
                adsh,
                hint="This filing was attempted but was not admitted to the panel.",
            )
        return document

    @router.get(
        "/triage",
        response_model=TriageResponse,
        tags=["Triage"],
        summary="List excluded filings with evidence",
        include_in_schema=include_in_schema,
    )
    def get_triage() -> dict:
        """Return each excluded filing's category, gap, evidence and example.

        Exclusions remain explicit rather than being forced into the panel.
        """
        return data_store.triage_document()

    @router.get(
        "/cleaning-rules",
        response_model=CleaningRulesResponse,
        tags=["Method"],
        summary="View the ordered cleaning method",
        include_in_schema=include_in_schema,
    )
    def get_cleaning_rules() -> dict:
        """Return the cleaning log's artifact, motivation, example and row count."""
        return data_store.cleaning_rules_document()

    return router


def _not_found(kind: str, value: str, hint: str | None = None) -> Exception:
    from fastapi import HTTPException

    return HTTPException(
        status_code=404,
        detail={"code": "not_found", "message": f"{kind} {value} was not found.", "hint": hint},
    )


app.include_router(_router())
app.include_router(_filing_router())
# Vercel preserves the /api prefix when it invokes the ASGI app.
app.include_router(_router(prefix="/api", include_in_schema=False))
app.include_router(_filing_router(prefix="/api", include_in_schema=False))


@app.exception_handler(FileNotFoundError)
async def missing_export(_: Request, exc: FileNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "detail": {
                "code": "data_not_exported",
                "message": "The app data has not been generated.",
                "hint": str(exc),
            }
        },
    )
