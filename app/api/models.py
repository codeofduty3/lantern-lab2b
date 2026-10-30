"""Response schemas for the LANTERN API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HealthResponse(APIModel):
    status: Literal["ok"] = Field(description="Service health.")
    release: Literal["2026q3"] = Field(description="SEC data release.")
    read_only: Literal[True] = Field(description="The API exposes no write endpoints.")


class CoverageResponse(APIModel):
    filings_attempted: int = Field(description="Filings that contain schedule-of-investments rows.")
    filings_admitted: int = Field(description="Filings within the reconciliation tolerance.")
    share_of_filings: float = Field(description="Admitted share of attempted filings.")
    filed_fv_attempted: float = Field(description="Reported fair value across attempted filings.")
    filed_fv_admitted: float = Field(description="Reported fair value across admitted filings.")
    share_of_dollars: float = Field(description="Admitted share of attempted filed dollars.")
    filings_without_soi_rows: int = Field(description="SEC filings with no schedule rows.")


class Filing(APIModel):
    adsh: str
    cik: str
    name: str
    form: str
    period: str
    n_holdings: int
    holdings_fv: float | None
    missing_fv: int
    filed_fv: float | None
    gap_pct: float | None
    admitted: bool
    triage_category: str | None
    edgar_url: str


class FilingsResponse(APIModel):
    filings: list[Filing]


class Holding(APIModel):
    identifier: str
    investment_type: str | None = None
    industry: str | None = None
    affiliation: str | None = None
    principal: float | None = None
    cost: float | None = None
    fair_value: float | None = None
    interest_rate: float | None = None
    spread: float | None = None
    pik_rate: float | None = None
    maturity: str | None = None
    pct_net_assets: float | None = None
    source_rows: str = Field(description="Semicolon-separated zero-based SOI source rows.")
    n_rows: int
    n_conflicts: int
    identifier_source: str | None = None
    fair_value_source: str | None = None
    security_class: str | None = None
    affiliation_category: str | None = None
    has_unfunded_commitment: bool
    shares: float | None = None
    unfunded_commitment: float | None = None


class HoldingsResponse(APIModel):
    adsh: str
    holdings_fv: float
    holdings: list[Holding]


class TriageItem(APIModel):
    adsh: str
    name: str
    form: str
    period: str
    holdings_fv: float | None
    filed_fv: float | None
    gap_pct: float | None
    triage_category: str
    evidence: str
    example: str
    fix: str
    edgar_url: str


class TriageResponse(APIModel):
    triage: list[TriageItem]


class CleaningRule(APIModel):
    rule: str
    artifact: str
    motivation: str
    example_adsh: str
    example_soi_row: int | str
    rows_affected: int
    coverage_before: float | None
    coverage_after: float | None


class CleaningRulesResponse(APIModel):
    rules: list[CleaningRule]


class ErrorDetail(APIModel):
    code: str
    message: str
    hint: str | None = None


class ErrorResponse(APIModel):
    detail: ErrorDetail
