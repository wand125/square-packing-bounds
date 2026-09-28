# Point-only endpoint certificate for s(21) = 5

**Unpublished staging draft. The complete split replay and distribution integrity
checks have passed. The public one-command run is still in progress on M1.
Publication remains pending its successful completion.**

This certificate uses 4,604 nonnegative point weights in the side-5 container.
Its all-pose capture threshold is `q = 249987/250000`, and its total mass is
`2624862500021/125000000000`. Thus

```
21q - mass = 999979/125000000000 > 0.
```

The proof excludes packings in every smaller container. It allows boundary
contact: enlarge a hypothetical packing from side `L < 5` to side 5, then take
the concentric closed unit squares strictly inside the enlarged squares. They
are pairwise disjoint, so their captured point masses cannot sum to more than
the total measure. This contradicts the displayed strict gap. The 5-by-5 unit
grid supplies the matching upper bound. The same grid and monotonicity give
`s(n)=5` for `22 <= n <= 25` as corollaries.

Evan Daniel already published a mixed point-and-segment proof of `s(21)=5`.
This work does not claim priority for that value. Our supports are derived from
his earlier point certificate and the weights were re-optimised. Attribution,
exact provenance, and his retained licence accompany the distribution.

## Reproduce

Use Python 3.12 or later. Run these commands from this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-tested.txt
python inspect_certificate.py
python unpack_bundle.py
python verify_portable.py --workers 2 --out /tmp/n21-proof-replay
```

The output directory must not already exist. The lightweight inspection checks
only data identities and rational algebra. The full runner must execute all
numerical stages successfully and finish with `FRESH_ALL_DOMAIN_REPLAY_VERIFIED`.
It checks 5,000 roots, 8,758 sieve parents, and all 31,678 required frontier
parents; 7,052 further parents lie strictly outside the representative angle
domain. Reducing `--workers` changes scheduling, not mathematical coverage.
Do not use Python's `-O` option.

This is a separate rational verification route. The repository's older
`src/verify.py` and its rectangle checkers do not verify this endpoint bundle.
Successful execution is a computer-assisted check, not a proof-assistant proof
or an external review.

The package includes `PUBLICATION.md`, `PROOF-LEMMAS.md`, `FORMAT.md`, the original
and normalised point data, and `archive-index.json`. The 14 archive parts total
463,568,316 bytes; unpacked inputs occupy about 2.54 GB. Allow additional space
for temporary extraction and replay outputs. `unpack_bundle.py` requires a new
`bundle/` directory, verifies every archive part and all 75,130 input files,
and reports `BUNDLE_BYTES_VERIFIED`. This reports byte integrity only.

All Python files from the bundle are also readable under `verifier-source/`.
The unpacker checks these copies against the extracted sources. The numerical
runner uses the extracted `bundle/`. Do not edit either copy before replay.

The full split replay and exact assembly have succeeded. Acceptance records for
the public one-command run will be added after it finishes; this draft does not
claim that end-to-end success yet.
