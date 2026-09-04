# cpcp_demo — executable PushNote/PullNote demo

The runnable companion to the
[CPCP contracts](https://github.com/laquereric/coordination-protocol-contract-package):
two CID documents, a stub seam that implements them, and push/pull
clients in eight languages, all verified against each other by
`demo/run-demo.sh`.

## Run it

```bash
./demo/run-demo.sh
```

Needs only Python 3 for the reference loop; every other language runs
if its toolchain is present and SKIPs loudly otherwise. All green means
every present client pushed, replayed, and pulled through the stub seam.

Point any client at your own pod instead via `CPCP_URL`:

```bash
CPCP_URL=http://localhost:13002/_cpcp python3 languages/python/examples/pull/pull.py
```

## Layout

See `.cpcp/package.json` — the machine-readable manifest of this
package (CIDs, seam routes, runners, languages). The canonical repo
format is documented in the contracts repo.
