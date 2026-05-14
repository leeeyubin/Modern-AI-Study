Sync docs/API.md with the live OpenAPI spec.

1. Fetch the running app's OpenAPI spec: `curl -s http://127.0.0.1:8000/openapi.json`
   - If the server isn't running, start it in the background first: `PYTHONPATH=. uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 &` then wait a moment and retry.
2. Read the current `docs/API.md` (if it exists).
3. Compare every route (method + path), request body schema, response schema, and status code in the spec against what's documented.
4. For each discrepancy (added route, removed route, changed schema, wrong status code), note what changed.
5. Rewrite `docs/API.md` to reflect the current spec exactly. Format:
   - One section per router tag
   - Each endpoint: method + path as a heading, then request body fields and response fields as bullet lists with types, then possible status codes
6. Report a summary of what changed (added, removed, updated).
