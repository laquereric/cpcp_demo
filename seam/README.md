# The reference seam

`server.py` implements the notes interface so the CIDs in `../cid/` are
runnable rather than only readable. Stdlib only — no framework, no
database, no credentials.

* `note.list` — read notes by reference. Reading costs nothing and
  promises nothing.
* `note.create` — write a typed, closed-shape Effect named by an
  `operationId`. Repeats return the first receipt.
* Routes: `POST /_cpcp/rpc`, `GET /_cpcp/cid.json`, `GET /_cpcp/up`,
  `GET /up`.

**State evaporates with the process.** That is what lets a *write* live
at the `public_cpcp` scope at all: there is nothing here a caller can
damage, and a restart is the reset. Binding is loopback
(`127.0.0.1`, `PORT` defaulting to 18080) — see
`.cpcp/public_cpcp/package.json`, which records that as measured
exposure rather than asserted.

Run it alone:

```bash
PORT=18080 python3 seam/server.py
```

Or through the conformance loop, which starts it, checks the shapes,
asserts the seam against its own CIDs, then drives every example client
present on the machine:

```bash
./conformance/run.sh
```

This is a REFERENCE implementation, not a product. It shows what
conforming behaviour looks like; it is not a pod, and nothing durable
should ever be pointed at it.
