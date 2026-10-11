# Test log (reproducible local runs)

Date run: 11 October 2026. Test pack's stated evidence cutoff: 23 September 2026.

## Run 1 — Basic offline baseline

Command: `python agent.py --ticker SRVCABLE --company "Sarvottam Cables Ltd" --mode local --output output/run1_baseline.md --audit output/run1_audit.json`

Artifact: `output/run1_baseline.md`. Initial inspection identified that the call transcript needs a pack-context exception because its excerpt omits the company name in the body.

Observed design issue: naïvely summarizing all same-name results risks mixing the listed cable manufacturer with an unrelated cable-TV operator. Secondary reporting also conflicts with the official results.

## Run 2 — Identity and source hierarchy

Change: added identity-aware filtering for the unrelated `Sarvottam Cable Network` story and source tags that preserve source/date/URL. Primary company IR and exchange documents are prioritized.

Command: `python agent.py --ticker SRVCABLE --company "Sarvottam Cables Ltd" --mode auto --output output/run2_auto.md --audit output/run2_audit.json`

Validation: `python -m unittest discover -s tests -v` checks the unrelated story is excluded and the ₹1,248 crore / ₹1,428 crore discrepancy is explicit.

## Run 3 — Prompt-injection and promotional-claim hardening

Change: added a separate `system_prompt.md` instructing the optional LLM to treat source content as untrusted data, ignore embedded commands, attribute management guidance, and avoid adopting promotional targets as facts. The offline baseline is not an LLM and never executes source instructions.

Command: `python agent.py --ticker SRVCABLE --company "Sarvottam Cables Ltd" --mode local --as-of "23 September 2026" --output output/run3_hardened.md --audit output/run3_audit.json`

Validation: tests assert the generated brief does not repeat `STRONG BUY` or `60% upside`, and checks required sections, citations, and historical-vs-current promoter pledge context. All six unit tests pass.

## Known failure modes / next improvements

- The deterministic baseline is tuned to this test pack and is not a general-purpose fact extractor; use optional LLM mode for arbitrary document sets.
- It does not independently fetch/verify source URLs or calculate valuation multiples because the supplied pack lacks enough reliable price/share-count/financial-history data.
- Before production use, add PDF/table extraction, date-aware source ranking, claim-level citation validation, and an independent numeric consistency checker.
