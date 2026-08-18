"""forge/paths.py — the one path resolver. All Forge state hangs off home().

Mirrors homestead.keep.paths: this is the ONLY module permitted to resolve a
home directory, and `Path.home()` is the only spelling it may use — the store's
vault-leak linter can SEE `Path.home() / ...` but a bare `~`/`expanduser` string
disappears from its report (homestead's I-20), and a write the tooling cannot see
is exactly the leak that discipline exists to prevent. No fixed-location default:
`FORGE_HOME` exists for tests and for an operator who deliberately moves the root,
not as a convenience override (homestead's I-19).
"""
from __future__ import annotations

import os
from pathlib import Path

__all__ = ["home"]

_ROOT_ENV = "FORGE_HOME"
_ROOT_NAME = ".forge"


def home() -> Path:
    """The Forge root. `$FORGE_HOME`, else `<home>/.forge` — the shared home the
    checkpoint memory, calibration ledger, soil store and schedules all hang off,
    the way homestead-law and homestead-ledger share `~/.homestead`."""
    override = os.environ.get(_ROOT_ENV)
    if override:
        return Path(override)
    return Path.home() / _ROOT_NAME
