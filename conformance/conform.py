#!/usr/bin/env python3
"""CID conformance: the stub seam honors what the CIDs declare.

Loads cid/push-note.cid.json and cid/pull-note.cid.json, then drives
the seam and asserts behavior matches the declarations: methods exist,
required params are required, operationId replays, results carry the
declared shape (@graph of typed nodes), and every envelope carries
@context. Anything here failing means the package drifted from its own CIDs.

Usage:  PORT=18080 python3 conformance/conform.py   (server must be running)
Exit non-zero on the first mismatch.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

# ROOT, NOT HERE. The CIDs used to sit beside this script in demo/ and now live
# in cid/ at the top of the package.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CID_DIR = os.path.join(ROOT, "cid")
PORT = int(os.environ.get("PORT", "18080"))
BASE = "http://127.0.0.1:%d/_cpcp" % PORT

failures = []


def check(name, cond, detail=""):
    print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        failures.append(name)
    return cond


def post(method, params=None, operation_id=None):
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    if operation_id:
        body["operationId"] = operation_id
    req = urllib.request.Request(
        BASE + "/rpc", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            return res.status, json.loads(res.read().decode() or "{}")
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read().decode() or "{}")


def load_cid(name):
    with open(os.path.join(CID_DIR, name), encoding="utf-8") as fh:
        return json.load(fh)


def main():
    pull_cid = load_cid("pull-note.cid.json")
    push_cid = load_cid("push-note.cid.json")

    pull_methods = {op["method"] for op in pull_cid["operations"]}
    push_methods = {op["method"] for op in push_cid["operations"]}
    check("cids-declare-distinct-methods", pull_methods.isdisjoint(push_methods),
          "%s vs %s" % (sorted(pull_methods), sorted(push_methods)))

    # Pull contract: {} params in, @graph of typed notes out, @context on it.
    st, env = post("note.list", {})
    check("pull-status", st == 200, st)
    check("pull-context", "@context" in env, "LD profile envelope")
    graph = ((env.get("result") or {}).get("@graph"))
    check("pull-graph", isinstance(graph, list) and len(graph) >= 1, "nodes=%s" % (
        len(graph) if isinstance(graph, list) else "?"))
    if isinstance(graph, list):
        check("pull-nodes-typed", all(
            isinstance(n, dict) and isinstance(n.get("title"), str)
            and isinstance(n.get("body"), str) and n.get("@type") == "Note"
            for n in graph), "title+body+@type on every node")

    # Push contract: title+body+operationId required, typed echo, replay.
    st, env = post("note.create", {"title": "t", "body": "b"})
    check("push-requires-operation-id",
          st == 400 and env.get("reason") == "operation_id_required", st)
    st, env = post("note.create", {"title": "t"}, operation_id="conf-op-1")
    check("push-requires-body",
          st == 400 and env.get("reason") == "missing_params", st)
    st, env = post("note.create", {"title": "ct", "body": "cb"}, operation_id="conf-op-1")
    first = env.get("result") or {}
    check("push-creates", st == 200 and first.get("@type") == "Note"
          and first.get("title") == "ct", st)
    check("push-context", "@context" in env, "LD profile envelope")
    st, env = post("note.create", {"title": "other", "body": "other"}, operation_id="conf-op-1")
    check("push-replays", st == 200 and (env.get("result") or {}) == first,
          "same operationId, same receipt")
    st, env = post("note.create", {"title": "x", "body": "y"}, operation_id="conf-op-2")
    check("push-new-op-writes", st == 200 and (env.get("result") or {}).get("title") == "x", st)

    # Unknown methods refuse on the seam the CIDs do not declare.
    st, env = post("note.delete", {})
    check("unknown-refused", st == 400 and env.get("reason") == "unknown_operation", st)

    print("conform: %d failures" % len(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
