#!/usr/bin/env python3
"""Fail if either CID's embedded shape diverges from the canonical file.

Audit F4: the CIDs stay self-contained (standalone portability), and this
check -- run by conformance/run.sh -- fails loudly on silent drift instead.
Usage:  python3 conformance/check-shapes.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

# ROOT, NOT HERE. The contract used to sit beside this script in demo/; it now
# lives in cid/ and shapes/ at the top of the package, so a checker anchored on
# its own directory would look inside conformance/ and find nothing.
ROOT = Path(__file__).resolve().parent.parent
CID_DIR = ROOT / "cid"
SHAPE_DIR = ROOT / "shapes"
CANONICAL = SHAPE_DIR / "note-shape.ttl"
CANONICAL_REL = "shapes/note-shape.ttl"


def normalized(text):
    """Compare shape graphs, not comment bytes: drop full-line comments."""
    out = [line.rstrip() for line in text.splitlines()
           if line.strip() and not line.strip().startswith("#")]
    return "\n".join(out).strip() + "\n"


def main():
    canonical = normalized(CANONICAL.read_text(encoding="utf-8"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    ok = True
    for name in ("pull-note.cid.json", "push-note.cid.json"):
        cid = json.loads((CID_DIR / name).read_text(encoding="utf-8"))
        embedded = normalized(cid.get("shapes") or "")
        match = embedded == canonical
        print("%s shapes-identical=%s sha256=%s" % (name, match, digest[:16]))
        ok = ok and match
    record = {"canonical": CANONICAL_REL, "version": 1, "sha256": digest}
    (SHAPE_DIR / "SHAPES.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("wrote shapes/SHAPES.json")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
