# Recorded verification runs

`split-replay.json` records the fresh six-worker Intel frontier replay and exact
assembly with the local root and sieve replays. All six workers exited zero.
`split-linkage.json.gz` is the byte-preserved complete assembly record, including
source hashes and output bindings. Its decompressed SHA256 is recorded in the
summary. Absolute paths identify historical run outputs; the reproducer creates
new paths and new output bindings on the reader's machine.

The prefix comparison records show exact proof-object agreement with the earlier
run. The distribution records describe byte-preserving copying and an actual
archive extraction with all input hashes checked. These packaging records do
not perform mathematical verification.

The separate M1 public one-command run is still pending. Its acceptance record
will be included before publication. No completion of that run is claimed here.
Use `verify_portable.py` for a fresh complete numerical check; do not treat these
historical JSON records as a substitute for executing the checker.
