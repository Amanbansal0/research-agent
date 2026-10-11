# ResearchForge — Evidence-First Equity Research Agent

A small, auditable research agent that turns an NSE ticker plus a folder of scraped Markdown documents into a concise retail-investor brief. Built for the fictional Sarvottam Cables Ltd (NSE: SRVCABLE) assignment.

## Why this design

- **Source-grounded:** every important claim carries `[S#]` citations mapped to source metadata.
- **Conflict-aware:** does not quietly reconcile inconsistent figures; it flags the company's ₹1,248 crore revenue against a secondary article's ₹1,428 crore.
- **Identity-aware:** excludes a similarly named local cable-TV operator from the equity analysis.
- **Prompt-injection-resistant:** source text is treated as evidence, never instructions. The promotional blog's embedded instruction is ignored.
- **Runs without an API key:** deterministic local mode works offline. Optional OpenAI mode gives richer synthesis.
- **Auditable:** each run writes `output/run_audit.json`, listing documents used/excluded and the execution mode.

## Requirements

- Python 3.10+ (core mode uses only the standard library)
- Optional: OpenAI API key and `pip install -r requirements.txt`

## Quick start (Windows PowerShell)

```powershell
cd C:\research-agent
# If you downloaded this project ZIP, extract it here first.
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python agent.py --ticker SRVCABLE --company "Sarvottam Cables Ltd" --mode local
```

The brief is written to `output\SRVCABLE_brief.md` and the audit to `output\run_audit.json`.

### Optional LLM mode

Set the key only in your terminal/session; do not commit it to Git:

```powershell
$env:OPENAI_API_KEY = "YOUR_KEY_HERE"
$env:OPENAI_MODEL = "gpt-4.1-mini"
python agent.py --ticker SRVCABLE --company "Sarvottam Cables Ltd" --mode openai
```

`auto` mode selects OpenAI only if `OPENAI_API_KEY` exists; otherwise it uses local mode. The LLM mode sends the selected source documents to the chosen API. Check the provider's current pricing and data terms before use.

## Input format

Put `.md` documents in `research_pack/`. Each document should ideally start with YAML-like metadata:

```yaml
---
source: Publisher / filing name
url: https://example.com/document
published: 2026-09-23
type: official filing
---
```

The parser also works without metadata, but source traceability will be weaker. Supply the as-of date explicitly when it differs from the default:

```powershell
python agent.py --ticker ABC --company "Example Ltd" --pack .\research_pack --as-of "11 October 2026" --output .\output\ABC.md
```

## Architecture

1. **Ingest:** parse document metadata and assign stable per-run source IDs.
2. **Resolve identity:** match ticker/company and exclude obvious same-name false positives.
3. **Synthesize:** use a deterministic offline baseline or an optional LLM following `system_prompt.md`.
4. **Audit:** save the selected source list, exclusions, mode, and output path.

## Model choice

The default is offline deterministic mode, so the assignment is reproducible and costs nothing. Optional `gpt-4.1-mini` is a cost-conscious synthesis choice for interpreting conflicting prose, but the code does not require it. Source hierarchy, citations, identity filtering, and prompt-injection handling are enforced in the system prompt and local pipeline.

## Tests and known limitations

Run `python -m unittest discover -s tests -v`. The test suite checks source metadata parsing, exclusion of unrelated same-name content, citation presence, conflict surfacing, and resistance to an embedded instruction in a promotional source.

The baseline is intentionally transparent, not a substitute for professional investment research. It is tailored to the supplied pack's known facts and filenames; generalizing to arbitrary tickers works best in LLM mode and may require tuning. It does not independently verify external URLs or market prices, and it should never be interpreted as a buy/sell recommendation.

## Submission checklist

- [x] `system_prompt.md` separate from code
- [x] One-page SRVCABLE brief generated into `output/SRVCABLE_brief.md`
- [x] Run audit and test log
- [ ] Push repository to GitHub (user action)
- [ ] Record 2–3 minute walkthrough (user action)
- [ ] Paste the generated brief into the submission form (user action)
