# Changelog

Notable changes, newest first. No release has been tagged yet
(`pyproject.toml` carries `0.1.0`); entries below are recorded as they land.

## Unreleased

- **docs**: fleet cross-repo analysis committed
  (`docs/analysis/2026-08-18-fleet-cross-repo.html`, 2026-08-18). Findings
  folded into this changelog and into the README's soft-dependencies table.
- **Nestor v0.6.0 compatibility**: fuzzy `constraints_on` (bar 0.55,
  calibrated on the dogfood corpus) now catches a re-worded prior decision
  before the Forge's own `recognize_threshold` (0.6) applies. The recognize
  band matches more reliably against Nestor v0.6.0+ with no code change on
  the Forge side. See README, Soft dependencies.
- **Promotion pipeline validated end-to-end**: homestead-health
  (safe-app-store PR #200) is the first build to traverse
  `promote_check.py`'s 9 gates from playground to promotion. Three
  promo-recon branches documented gate-by-gate due diligence before the
  attempt; the promotion record landed. First concrete evidence that the
  pipeline the Forge was designed for works as designed.
- **Readiness corpus wired store-side**: the store's `readiness_corpus.py`
  maps `promote_check` gates to production-readiness-checklist control IDs
  (10,042 controls, e.g. `witnessed` → `USEQ-E075330B`), measuring the
  measuring panel's own coverage claims. Not yet consumed directly by this
  repo — the seam is injected, never vendored, so the corpus itself stays
  with production-readiness-checklist.
