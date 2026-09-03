@markdownai v1.0

<!-- Copied from the session plan of 2026-09-02 (Vishwakarma seat). The living decisions are drafts in ~/.forge/nestor; this is the build plan. -->

# The Forge engine build — plan

## Context

The Forge (`forge-play/Forge`, import name `forge`) is the engine that refuses a confident wrong answer: a three-band checkpoint loop (`forge/checkpoint.py:run_checkpoint`) over a maker's sealed decisions, and a measuring panel (`forge/measure_panel.py`) over a build. Every design doc names the same missing piece: **decision extraction**. `Decision` is an explicit input today (`forge/checkpoint.py:173`: "Nothing in this module infers a Decision from anything"), so the router has nothing to route, and the calibration ledger has never been called outside its own tests (code-graph warrant in `~/.forge/nestor`).

Operator direction, 2026-09-02 (drafts in the project Nestor, unsealed):
- One engine, living here. Willow gains the dependency; apps built here run only on it. The Forge never imports willow-mcp.
- Same extraction pattern as Kart and Jeles: zero-runtime-dep package on PyPI, pinned `>=x,<1.0.0`.
- PyPI trusted publisher pending for **`forge-play`** / repo `forge-play/Forge` / `release.yml` / environment `pypi`. Repo is still `rudi193-cmd/Forge`; pyproject still says `the-forge`, setuptools, literal version.
- Every fleet release now cuts with the willow-ci GitHub App; publishing is OIDC. Jeles's workflows are the template; Kart's `tests/test_release_wiring.py` is the rule file.

Scoping answers: whole ladder, phased so each bite ships alone; deterministic extraction first with a seam for model-proposed candidates; vendored modules go home after the first release; design docs move into the Forge first.

Two facts found during planning that change the shape:
- **The host is already repointed, but not pinned.** `safe-app-store-public/stores/_forge_extracted/README.md` records the store-side copies archived 2026-08-18, and the store's only live consumer (`stores/readiness_corpus.py`'s `assess`) imports `forge.measure_panel` lazily. The install line in `stores/requirements.txt` (`forge @ git+…Forge@master`) is a deliberate comment so the stdlib-only default stays clean; the real pin lands with Phase 5 once `forge-play` is on PyPI. `promotion.json`'s `host_repointed: false` is stale, not blocked.
- **The host's `Plan` has no fork in it.** `apps/the-forge/src/the_forge/plan.py:72` is `app_name + entries[file_write…]`; `stub_builder.hello_world_command` emits two file writes and no choice. A decision can't be extracted from a shape that can't express one. The extraction seam is a new entry kind, not a parser over prose.

Goal: **ground truth that arrives on its own.** A maker's sentence becomes a small thing; every decision along the way is asked once or not asked because it was already answered; the engine finds out whether its confidence was earned.

Rules of the house (apply to every phase):
- Paper before code: each phase opens by proposing its decisions as drafts in the project Nestor (`~/.forge/nestor`, `DecisionMemory.propose`) with a construction warrant where a tool can check the claim; the operator seals. Nothing here seals.
- Structure first (Vishwakarma seat): name the boundary, then the parts. No `task_submit` from this seat; Kart-side runs are the operator's.
- Every phase is one PR that leaves the suite green and adds its own tests in the existing style (`tests/conftest.py` isolates Nestor's ledger; `ScriptedResponder` in `tests/test_checkpoint.py:57`; `_fsrs_blocked` in `tests/test_checkpoint_schedule.py`).

---

## Phase 0 — Paper: docs move in, decisions on the record

**Why first:** the shape doc says it may want to move here; the operator said move it. The plan itself should be findable from the repo.

- Copy into `docs/design/`: `willows-grove/docs/design/the-forge-shape.md` and the nine `safe-app-store-public/docs/design/the-forge*.md`. Add `docs/design/README.md` listing them with their origin path and date. Leave a one-paragraph pointer file at each origin (follow-up PRs in those two repos; note in this PR's description).
- Add `docs/design/the-forge-engine-build.md`: this plan, trimmed to the phases and the invariants.
- Propose Nestor drafts for the two new facts above (host repointed; Plan has no fork) with construction warrants: `grep -c archived stores/_forge_extracted/README.md`, and a grep showing `plan.py` has no `fork` kind.
- No code. Verification: `pytest -q` unchanged; `docs/design/README.md` lists 11 files.

## Phase 1 — Package and release chain (the Kart/Jeles road)

**Boundary:** the Forge becomes a fleet package Willow can pin. Operator acts are listed separately; nothing in this PR depends on them to be green.

Repo changes:
- `pyproject.toml`: `name = "forge-play"`, `requires = ["hatchling", "hatch-vcs"]`, `build-backend = "hatchling.build"`, `dynamic = ["version"]`, `[tool.hatch.version] source = "vcs"`, packages `forge*` unchanged (import name stays `forge`). Keep `test` and `trust` extras; add `pyyaml` to `test` (the release-wiring tests read the workflows). Copy Jeles's `[tool.hatch.version]` comment block verbatim; it names the v0.0.8 scar.
- `.github/workflows/release.yml`, `release-please.yml`, `tests.yml`, `pr-title.yml`, `dependabot-automerge.yml`: port from `hornbook-knowledge/Jeles/.github/workflows/`, package name swapped (`forge_play-` in the sdist assertion; `jeles` → `forge-play`). Keep the App-token step (`vars.WILLOW_CI_APP_ID` / `secrets.WILLOW_CI_PRIVATE_KEY`). `tests.yml` runs 3.11–3.13 with `pip install -e '.[test]' nestor-meaning`; name the jobs so branch protection has a check to require.
- `release-please-config.json` + `.release-please-manifest.json`: from Jeles; `package-name: forge-play`, `include-component-in-tag: false`, `bump-minor-pre-major: false`, manifest `"."` = `"0.0.0"` so the first `feat:` proposes 0.1.0 (the literal 0.1.0 in pyproject was never released).
- `tools/changelog_dedup.py` if `release-please.yml` calls it (Kart's does; port it with the workflow it belongs to). `CHANGELOG.md` keeps its hand-written history; release-please prepends.
- `tests/test_release_wiring.py`: port from `kartikeya/tests/test_release_wiring.py` (15 rules). Adapt the version-single-source rule to hatch-vcs + no literal in pyproject; drop Kart-specific exclusions only where the comment says why.
- `tests/test_no_reach_back.py`: AST-scan `forge/`, `demo/`, `tools/` for any import of `willow_mcp`; fail on one. This is the no-cycle invariant from the dependency decision.
- `tests/test_vendor_sync.py` stays as is until Phase 5.

Operator acts (recorded in the PR description, not code): rename is done on PyPI; transfer repo to `forge-play/Forge`; install willow-ci App on the org with the var/secret at org level; create `pypi` environment; enable auto-merge; require the `tests` check on master.

Verification: `pytest -q` green with the new tests; `python -m build` in a clean venv produces `forge_play-0.0.1.devN` (untagged) and the tag-match assertion is exercised by the test; after transfer, a `v0.1.0` cut by release-please reaches PyPI and `pip install forge-play` imports `forge`.

## Phase 2 — The four open issues

One PR, four commits, each `fix:` (they cut a patch release, which is right).

- **#6** `forge/checkpoint_schedule.py:174-204` `grade()` docstring: state the wire is live via `checkpoint_calibration.resurface`, `engagement=None` is the deliberate degraded path, point at `tests/test_checkpoint_calibration.py` §6.
- **#7** `forge/measure_panel.py:165` `_iter_files`: prune a named set (`.git`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `__pycache__`, `.venv`, `node_modules`, `.tox`, `dist`, `build`, `*.egg-info`) as a module constant with a docstring saying why each is a tool cache, not an artifact. Test: a tree with two tiny sources and a 400 KB `.mypy_cache/x.db` yields no convergent finding and routes nothing.
- **#9** `forge/instrument_callgraph.py`: call the CLI with `--args-file` (a temp JSON; the raw-JSON form is deprecated), parse `structuredContent.rows` (fallback: the `content[0].text` JSON). Zero rows on a non-empty tree is **not** "found nothing": if the payload parses but yields no rows where `query_graph` reported `total > 0`, raise `InstrumentUnavailable("could not read the output")` so the panel says COULD NOT RUN, never clean. Test: `tests/test_instrument_callgraph.py::test_drives_the_real_tool_and_flags_dead_code` goes green; add a unit test that a compact-JSON payload with a dead function is flagged, and that a payload the parser can't read raises.
- **#8** promotion: flip `promotion.json` `host_repointed: true` with a `notes` line citing the store README (2026-08-18). Add `tools/promotion_trust.py`: `enroll` (author side, uses `forge.trust.enroll`) writes the provisional custody; `ratify` (verifier side, `forge.trust.ratify`) is run by the operator with their key; the CLI prints the `trust` block to paste. Test with the existing `tests/test_trust.py` fixtures (`test_enroll_ratify_witnessed_end_to_end`). The ratify itself is the operator's act; the PR ships the tool and the flipped flag. Store-side follow-up: `python stores/promote_check.py <forge checkout> --record`.

Verification: `pytest -q` → 0 failed with the fleet keyring unset and `codebase-memory-mcp` on PATH; `python -m forge.measure_panel measure ./forge` prints no `.mypy_cache` findings; issue-#9 repro tree flags `never_called_anywhere`.

## Phase 3 — Nestor first, and the keyword → major table

**Boundary:** the entry. "The Forge cannot start a build that never asked. Not discouraged — unable." This phase gives the demo's beat 1 its missing artifact and puts the first real decision through the router.

- `forge/majors.py` + `forge/majors.tsv` (the flat file: `keyword<TAB>major<TAB>reason`, one row per pair; `site → web`, `app → web`, `app → mobile`, `app → desktop`, `cli → cli`, `api → service`, `bot → agent`, …). `scan(text: str, *, path: str = "", anchor: str = "") -> list[Hit]` where `Hit = (source, target, reason, path, anchor)` — word-boundary, case-insensitive, deterministic, no model. Two callers by construction: the Forge ignores `path`/`anchor`; the corpus lane (willow side) needs them. `majors_for(hits) -> dict[major, set[keyword]]`.
- `forge/paths.py`: `project_nestor(project_id) -> Path` = `home()/projects/<project_id>/nestor/keep/nestor.db`, ledger beside it. Same charset rule as `builder_id`. Move the store stood up today from `~/.forge/nestor` to `~/.forge/projects/forge-engine/nestor` (operator or the PR's migration note; `env.sh` updated).
- `forge/entry.py`: `open_bite(sentence, *, project_id, builder_id, responder, root) -> Entry`. Order, and each step records which tier answered:
  1. **Nestor** — ask the project store (`nestor.answer.resolve` over `SqliteStore(project_nestor(project_id))`, domain `decision`). If Nestor is not importable, **refuse** with `EntryError` (no soft degrade here, unlike `run_checkpoint`; this is the §11 rule as code). A sealed hit short-circuits: the bite already has an answer.
  2. **The box** — a `BoxLookup` protocol (`lookup(hits) -> list[Candidate]`), default implementation returns `[]` honestly and says so. The real box (the corpus under `~/github`) is willow-side; the seam is here.
  3. **Remote** — not built; `Entry.tiers` records `remote: not_attempted`.
  Then `scan(sentence)`; if `majors_for` has more than one major, build `Decision(decision_type="major", surface=f"'{sentence}' could be {majors}; which?", options=[Option(m, reason) …])` and run it through `run_checkpoint`. One major → no decision, recorded as `major: <m> (unambiguous)`.
- `Entry` dataclass: `sentence, hits, major, tiers, decision_outcome | None`. JSON-serialisable for the demo.
- CLI: `python -m forge.entry "<sentence>" --project X --builder Y` (dev shape like the other modules).
- Tests: table loads and every row has three fields; the shape doc's sentence yields `site→web` and `app→{web,mobile,desktop}`; ambiguity becomes a `Decision` with three options and routes socratic on a fresh store, then `auto` on the second run (the whole point); Nestor absent → `EntryError`; `BoxLookup` default is empty and labelled.

Verification: `python -m forge.entry "I got sum kol sites for app to spin" --project demo --builder rosalind` asks once, seals, and on the second run confirms without asking. Demo beat 1's friction line (`the keyword → major table does not exist`) is removed in Phase 6.

## Phase 4 — Decision extraction (deterministic over the Plan), and the calibration wire

**Boundary:** the engine cannot import the host's `the_forge.plan`, and must not. It defines the *decision-bearing* plan shape itself; the host's plan is a strict subset (file writes only) that extracts to nothing, honestly.

- `forge/plan_shape.py`: `Fork` entry — `{"kind": "fork", "decision_type": str, "surface": str, "options": [{"label", "tradeoff"}…], "recommended": str | None, "confidence": float | None, "resolves": [entry-index…]}`; `PlanDoc = {"app_name", "entries": [file_write | fork]}`. `validate(plan_dict) -> PlanDoc` with the same charset rule as the host (`decision_type` via `checkpoint_memory._check_decision_type`). This is the seam for "model proposes": a model-written plan carries forks; nothing else it writes reaches the router.
- `forge/decision_extract.py`: `extract(plan: PlanDoc, *, entry: Entry | None) -> Extraction(decisions, refused)`. Rules, in order, all model-free:
  - R1 the entry's major ambiguity (if `Entry.decision_outcome` is None and majors > 1) — already a `Decision`, pass through.
  - R2 every well-formed `fork` → `Decision(decision_type, surface, options, recommended)`; a fork with <2 options or a bad `decision_type` is **refused with a reason**, never silently dropped.
  - R3 two `file_write` entries with the same `dest_path` → a `Decision(decision_type="conflicting-write:<path>", options=[each content's first line…])`.
  A plan with no forks and no conflicts extracts to `[]` and the report says `nothing_to_decide=True` (the host's stub plan lands here today; that's the honest state, not a failure).
- `forge/build_loop.py`: `resolve(plan, *, builder_id, responder, root, extraction) -> Resolved(plan, outcomes)` — runs each `Decision` through `run_checkpoint` in plan order, replaces the fork with the chosen option's `resolves` entries, refuses to return a plan that still holds a fork. The model never touches the router: extraction is rule-based; bands come from memory.
- **Calibration wire** (the reason the engine exists): for each fork with `recommended` and `confidence`, before the checkpoint call `calibration_ledger.record_prediction(builder_id, claim=f"{decision_type}: maker picks {recommended}", confidence, kind="fork")`; after it, `resolve_prediction(…, outcome=(chosen == recommended))`. A fork without a confidence records nothing (no fabricated 0.5). `overconfidence_signal` already routes through `human_loop`; leave it.
- Tests: extraction from the host's stub plan → empty + `nothing_to_decide`; a fork plan yields one `Decision` per fork in order; malformed fork refused with reason; conflicting writes → R3 decision; `resolve` seals and substitutes; second run of the same plan hits `auto`; prediction recorded and resolved true/false against `ScriptedResponder`'s pick; `scorecard` shows one resolved row. Code-graph warrant on the project Nestor draft "next piece" gets its expected digest updated by the PR (the ledger will now have a non-test caller).

Host-side follow-up (app store PR, not this repo): `stub_builder` emits one `fork` from `forge.majors.scan` of a `--sentence`, and `forge_build.build_and_cross` calls `forge.build_loop.resolve` before `seam.cross`. The seam refuses an unresolved fork.

Verification: `pytest -q`; `python -m forge.build_loop demo/fixtures/fork_plan.json --builder rosalind` asks once, prints the resolved plan and a scorecard with one resolved prediction; the code-graph query for outside callers of `calibration_ledger` now lists `forge/build_loop.py`.

## Phase 5 — Vendoring goes home (after the first release)

- willow-mcp PR (operator-driven): pin `forge-play>=0.1.0,<1.0.0`; replace `src/willow_mcp/{human_loop,friction_floor,model_egress}.py` with imports from `forge`; add the contract test the fleet-versioning doc asks for.
- Forge PR: remove the vendor-note headers from the three modules, delete `tools/vendor_sync_check.py` and `tests/test_vendor_sync.py`, keep `tests/test_no_reach_back.py`. Propose a `supersedes` edge in the project Nestor from the new dependency draft to the vendoring draft.

Verification: `pip install forge-play willow-mcp` in one venv; willow-mcp's suite green; `python -c "import willow_mcp.human_loop as h, forge.human_loop as f; assert h is f"`.

## Phase 6 — The demo runs the loop it describes

- `demo/the_first_bite.py`: beat 1 calls `forge.majors.scan` and `forge.entry.open_bite` (friction line removed when the table exists); beat 3's "every warrant is an attestation" stays as a friction (that's Nestor-side); beat 11 calls `calibration_ledger.scorecard` and shows the fork prediction resolved (friction line removed). `--json` output gains `tiers` from `Entry`.
- `tests/test_demo.py`: run `demo/the_first_bite.py --json --pace fast` in a temp `FORGE_HOME`; assert beats 1 and 11 report no `friction`, and the friction log is otherwise unchanged in shape.
- Update `README.md` quick start (`pip install forge-play`) and the soft-dependencies table (Nestor is *required at the entry*, soft everywhere else — say so).

Verification: `python demo/the_first_bite.py --json` on a fresh `FORGE_HOME` shows MISSING only for the willow-side beats (6: the net lease; 7/8: Kart and promote_check on the box).

---

## Files touched (by phase)

- P0: `docs/design/*` (11 copied + README + plan)
- P1: `pyproject.toml`, `.github/workflows/*.yml` (5), `release-please-config.json`, `.release-please-manifest.json`, `tools/changelog_dedup.py`, `tests/test_release_wiring.py`, `tests/test_no_reach_back.py`
- P2: `forge/checkpoint_schedule.py`, `forge/measure_panel.py`, `forge/instrument_callgraph.py`, `promotion.json`, `tools/promotion_trust.py`, tests for each
- P3: `forge/majors.py`, `forge/majors.tsv`, `forge/paths.py`, `forge/entry.py`, `tests/test_majors.py`, `tests/test_entry.py`
- P4: `forge/plan_shape.py`, `forge/decision_extract.py`, `forge/build_loop.py`, `demo/fixtures/fork_plan.json`, `tests/test_decision_extract.py`, `tests/test_build_loop.py`
- P5: three vendored modules' headers, `tools/vendor_sync_check.py` (delete), `tests/test_vendor_sync.py` (delete)
- P6: `demo/the_first_bite.py`, `tests/test_demo.py`, `README.md`

Reused, not rebuilt: `run_checkpoint` / `Decision` / `Option` / `Responder` (`forge/checkpoint.py`), `open_checkpoint_memory` + `_check_decision_type` (`forge/checkpoint_memory.py`), `record_prediction` / `resolve_prediction` / `scorecard` / `overconfidence_signal` (`forge/calibration_ledger.py`), `route` + `InstrumentUnavailable` (`forge/measure_panel.py`), `enroll` / `ratify` / `witnessed` (`forge/trust.py`), Jeles's workflows, Kart's release tests, Nestor's `answer.resolve` / `SqliteStore` / `DecisionMemory.propose`.

## Order and what ships alone

P0 → P1 → P2 can land in any order after P0 (P1 and P2 are independent; P2's #8 flag flip waits on nothing). P3 before P4 (P4 consumes `Entry`). P5 after the first PyPI release. P6 last. Each phase closes with a `session_handoff_write` naming its `next_bite`.

## End-to-end verification

1. Fresh venv: `pip install -e '.[test]' nestor-meaning pyyaml`; `env -u NESTOR_KEYRING -u NESTOR_REQUIRE_SEAL_KEY pytest -q` → 0 failed (fsrs and codebase-memory-mcp present, or their tests skip honestly).
2. `python demo/the_first_bite.py --json` on `FORGE_HOME=$(mktemp -d)`: beats 1, 3-5, 9-11 run; friction only where the box, not the engine, is missing.
3. `~/.forge/nestor/warrant_check.py` (env sourced): every construction warrant holds or is deliberately re-digested by the PR that changed the fact.
4. After transfer + tag: `pip install forge-play==0.1.0 && python -c "import forge, forge.entry, forge.build_loop"`.
