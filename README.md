# cpcp_demo — the notes interface, with callers in eight languages

`note.list` and `note.create`: two CID documents, the shape they share, a
reference seam that implements them, and conformance that holds the seam to what
the CIDs declare.

**The name is accurate.** [The format](https://github.com/laquereric/coordination-protocol-contract-package/blob/main/spec/repo-format.md)
asks for *one* example caller per CID, in any language. This repo carries one
per language because demonstrating is its job — that is a choice, not the bar.
A conforming package needs a CID and a caller that runs.

```text
cid/            the interface: pull-note and push-note
shapes/         note-shape.ttl, embedded in both CIDs; SHAPES.json holds its digest
seam/           server.py, the reference implementation
conformance/    run.sh and the two checks it runs
examples/       one directory per language, pull and push
.cpcp/          the index, and one manifest per scope served
```

## Run it

```bash
./conformance/run.sh
```

Python 3 runs the reference loop; every other language runs if its toolchain is
present and SKIPs loudly otherwise — a skip is reported, never silent, never a
pass. Green means every present caller pushed, replayed and pulled through the
seam, and the seam still matches its CIDs.

Point a caller at your own pod instead:

```bash
CPCP_URL=http://localhost:13002/_cpcp python3 examples/python/pull.py
```

## What holds it together

* `conformance/check-shapes.py` — the CIDs embed the shape so they travel alone;
  this fails if either copy diverges from `shapes/note-shape.ttl`.
* `conformance/conform.py` — drives the seam and asserts what the CIDs declare:
  methods exist, required params are required, `operationId` replays, results
  carry the shape, envelopes carry `@context`.

Contract: [coordination-protocol-contract-package](https://github.com/laquereric/coordination-protocol-contract-package).
`.cpcp/package.json` is the machine-readable index.
