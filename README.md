# The Forge

**The engine that refuses a confident wrong answer.** *Per ignem, probatur — proven through fire.*

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Runtime deps](https://img.shields.io/badge/runtime%20deps-none-lightgrey)](pyproject.toml)

The Forge is the **model side** of a SAFE-native app-building system — not a
model that emits answers, but the harness that refuses to let a confident wrong
one stand. It is the base engine every builder pins, and it needs **no live
model** to run: it works on decisions and build directories, the way a linter
works on source.

It refuses in two places:

| | Layer | What it refuses |
|---|-------|-----------------|
| ⚖ | **The checkpoint loop** | a confident wrong **decision** — a three-band interaction (auto / recognize / socratic) over a memory of the maker's sealed decisions, with an engagement gate that scores rubber-stamping and a governance layer that records the maker's non-forgeable sign-off. *Authorship is not authority.* |
| 🔍 | **The measuring panel** | a confident wrong **artifact** — measuring instruments run across a build; **convergence** (≥2 instruments naming one artifact) is the alarm, and the panel reports its own coverage honestly, so a class nothing measured is named unseen, never sound. |

Five measurement classes: size, hygiene, call-graph (dead code), execution
(parse-in-a-sandbox — *run it, don't read it*), and calibration (the model's own
confidence mirror). Plus **declared-not-ambient model routing**: local by
default, cloud only when the maker's signed manifest asks for it.

## The home

All Forge state — the decision memory, the calibration ledger, the governance
queue, the FSRS schedules — hangs off a single root: **`~/.forge`** (override
`FORGE_HOME`). One home, resolved in one place (`forge/paths.py`), the way the
Homestead face shares `~/.homestead`.

## Soft dependencies

The engine degrades around every heavy dependency rather than requiring it — the
pure math and governance run on the standard library alone:

| Absent | The engine still runs, but… |
|--------|------------------------------|
| **Nestor** (the decision seal) | full-Socratic every time — no recognition, no reseal |
| **fsrs** (spaced resurfacing) | fixed-interval fallback |
| **kartikeya** (the sandbox) | the `execution` instrument declares an honest coverage gap instead of parsing unsandboxed |
| **codebase-memory-mcp** | `call-graph` is named uncovered |

## Quick start

```bash
pip install -e '.[test]'
pytest
```

The suite is green with the soft dependencies present; individual tests skip or
fall back when theirs is absent.

## License

Apache-2.0. See `LICENSE` and `NOTICE`.
