# Reference project notes

## Availability

The Case Study 2B brief contains the placeholder
`<ABSOLUTE PATH OR REPO URL TO THE REFERENCE PROJECT>` rather than a readable
path or URL. No reference project was searched for elsewhere on disk. This
document therefore records the unavailable-reference decision instead of
claiming unobserved backend, frontend or Replit conventions.

## Conventions used here

- Backend: FastAPI with an explicit `app` entry point in
  `app/api/main.py`, a separate Pydantic response-model module, and a
  JSON-only data loader.
- OpenAPI: `/docs` includes a title, summary, description, contact, version and
  task-oriented tags. Every public endpoint has a summary and a docstring.
- Errors: errors use a stable `{"detail": {"code", "message", "hint"}}`
  envelope. Missing generated exports return 503; an unknown filing or absent
  holdings document returns 404.
- Frontend: static HTML, CSS and browser JavaScript. The API base defaults to
  the same origin in production and `http://127.0.0.1:8000` when the static
  server runs locally on port 8001. CORS allows those two local origins.
- Health: `/health` checks that exported coverage can be read and returns
  `status=ok` plus the read-only/release metadata.

## Task precedence

The brief's application constraints take precedence over unknown reference
patterns: the API does not import pandas or pyarrow, all routes are GET-only,
and no old-project endpoints or data models were carried forward.
