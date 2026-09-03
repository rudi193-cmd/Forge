# The Forge — design docs

Moved here 2026-09-02. The Forge's design was written while the engine lived
inside `safe-app-store` and its shape was worked out at Willow's desk in the
Grove; the docs stayed where they were written. `the-forge-shape.md` says of
itself: "it may want to move into `forge-play/Forge` once the shape settles."
The operator said move them. Each file is byte-identical to its origin at the
commit date shown; a pointer stays behind at each origin.

| File | Origin | Last changed there | What it is |
|---|---|---|---|
| `the-forge-shape.md` | `willow-memory/willows-grove/docs/design/` | 2026-09-01 | Captured working conversation (2026-08-30): what the Forge is, the keyword→major scan, per-project Nestor, Nestor-first, the PR deposit. Sixteen "Decisions taken" at the end. |
| `the-forge.md` | `safe-app-store-public/docs/design/` | 2026-08-11 | The founding design: D1–D13, the bite ladder for the learning layer, what landed 2026-08-11. |
| `the-forge-reuse-map.md` | same | 2026-08-11 | What the fleet already had (willow-mcp, Jeles, Nestor) and what the Forge wires rather than builds. |
| `the-forge-human-loop.md` | same | 2026-08-11 | D-HL-1..6: human_required queue + attestations adopted under checkpoint. |
| `the-forge-fsrs.md` | same | 2026-08-11 | D-FSRS-1..4: spaced resurfacing of seals; soft dependency. |
| `the-forge-measure.md` | same | 2026-08-11 | The measuring panel: convergence is the alarm; coverage reported honestly; decision extraction named as next. |
| `the-forge-promotion.md` | same | 2026-08-11 | Grounded extraction/promotion plan; the `host_repointed` gate. |
| `the-forge-readiness.md` | same | 2026-08-16 | D-R1..7: the panel measured against the production-readiness corpus; no mechanical Pass. |
| `the-forge-landscape.md` | same | 2026-08-11 | Where the Forge sits among the fleet's components. |
| `the-forge-review-2026-07-31.md` | same | 2026-07-31 | External review of the v1 design; P0/P1/P2 open items. |
| `the-forge-engine-build.md` | this repo | 2026-09-02 | The build plan for the engine: six phases, each a PR that ships alone. |

Decisions taken since these were written are not in these files. They are
drafts in the engine's per-project Nestor (`~/.forge/nestor`, see
`the-forge-engine-build.md`), waiting for a human seal. Documents are cited,
never sealed.
