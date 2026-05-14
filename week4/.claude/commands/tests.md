Run the full test suite and fix any failures.

1. Run: `PYTHONPATH=. pytest -q backend/tests 2>&1`
2. If all tests pass, report the count and stop.
3. If there are failures, for each one:
   - Quote the exact error message and traceback
   - Identify the root cause (wrong assertion, missing route, schema mismatch, etc.)
   - Suggest a concrete fix with the specific file and line to change
   - If the fix is straightforward and clearly correct, apply it, then re-run only the affected test file to confirm it passes
4. After fixing, re-run the full suite once more and report the final result.
