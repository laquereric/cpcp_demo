# cpcp_demo — the canonical CPCP package for the notes interface

`note.list` and `note.create`, defined once and executable: two CID
documents, the shape they share, a reference seam that implements them,
and conformance that holds the seam to what the CIDs declare.

The interface is the point. Everything else here exists to prove the
interface is real — a reference implementation that serves it, checks
that catch it drifting from itself, and eight client examples that show
it is not tied to one language.

Contracts it conforms to:
[coordination-protocol-contract-package](https://github.com/laquereric/coordination-protocol-contract-package).

## Layout

```text
cid/            the interface. pull-note and push-note CID documents
shapes/         note-shape.ttl, the one canonical shape both CIDs embed,
                plus SHAPES.json recording its digest
seam/           server.py, the reference implementation. In-memory,
                state evaporates with the process
conformance/    run.sh, and the two checks it runs
examples/       one directory per language, pull and push
.cpcp/          machine-readable manifests: the index and one per scope
```

Everything above used to live under `demo/`, which described how the
repo was run rather than what it is. The name says demo; the contents
are a package.

## Run it

```bash
./conformance/run.sh
```

Needs only Python 3 for the reference loop; every other language runs if
its toolchain is present and SKIPs loudly otherwise — a skip is
reported, never silent, and never counted as a pass. All green means
every present client pushed, replayed, and pulled through the reference
seam, and the seam still matches its CIDs.

Point any client at your own pod instead via `CPCP_URL`:

```bash
CPCP_URL=http://localhost:13002/_cpcp python3 examples/python/pull.py
```

## What holds it together

* `conformance/check-shapes.py` — the CIDs embed the shape so they stay
  portable on their own; this fails if either copy diverges from
  `shapes/note-shape.ttl`.
* `conformance/conform.py` — drives the seam and asserts the behaviour
  the CIDs declare: methods exist, required params are required,
  `operationId` replays, results carry the declared shape, envelopes
  carry `@context`. A failure here means the package drifted from its
  own interface.

`.cpcp/package.json` is the machine-readable index; the repo format is
documented in the contracts repo (`spec/repo-format.md`).
