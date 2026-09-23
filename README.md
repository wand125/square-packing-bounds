# Lower bounds for packing 26, 29, 39, 53, 55, 56, 69, 70 and 72 unit squares

Let `s(n)` be the least side of a square that holds `n` unit squares with
arbitrary orientations, no two overlapping. This repository contains exact
weighted fractional certificates proving

```
s(26) >= 109/20  = 5.45
s(29) >= 557/100 = 5.57
s(39) >= 13/2    = 6.5
s(53) >= 369/50  = 7.38
s(55) >= 377/50  = 7.54
s(56) >= 381/50  = 7.62
s(69) >= 841/100 = 8.41
s(70) >= 171/20  = 8.55
s(72) >= 861/100 = 8.61
```

and, as a cross-check on the generator, a tenth certificate for `s(40) >= 13/2`
that also follows from the `n = 39` bound by monotonicity.

It also contains one certificate of a different kind, a rectangle-density
certificate in tokoharu's format built here with his solver, proving

```
s(29) >= 287/50 = 5.74
```

which supersedes the `n = 29` point certificate above; see
[s(29) >= 5.74](#s29--574-a-rectangle-density-certificate-built-here).

The previous figures for these cases come from a private communication from
Trevor Green to Erich Friedman, reported in Friedman's survey *Packing Unit
Squares in Squares* (Electronic Journal of Combinatorics, DS7), whose last
revision is dated 14 August 2009. The underlying argument has not been
published. The bounds here are the first to improve them, and they arrive with
certificates anyone can re-check.

| `n` | previously reported | this repository | improvement |
|---|---|---|---|
| 26 | 5.3923 | 5.45 (since improved, see below) | +0.0577 |
| 29 | 5.5119 | 5.57 (since improved, see below) | +0.0581 |
| 39 | 6.3512 | **6.5** | +0.1488 |
| 53 | 7.3246 | **7.38** | +0.0554 |
| 55 | 7.4807 | **7.54** | +0.0593 |
| 56 | 7.5574 | **7.62** | +0.0626 |
| 69 | 8.3485 | **8.41** | +0.0615 |
| 70 | 8.4162 | **8.55** | +0.1338 |
| 72 | 8.5498 | **8.61** | +0.0602 |
| 40 | 6.4061 | 6.5 (follows from `n = 39`) | +0.0939 |

For `n = 53, 55, 56, 69, 70, 72` the standing figure is Nagamochi's closed form, which
is the strongest independently verified bound the survey records for those
cases; for `n = 26, 29, 39` it is Green's. By monotonicity `s(39) >= 6.5` also
covers `n = 40..44` against the DS7 table and `s(70) >= 8.55` covers `n = 71`.

The `n = 53`, `n = 56`, `n = 69` and `n = 72` certificates carry no further
entries with them. Nagamochi's closed form already exceeds 7.38 from `n = 54`
on, 7.62 from `n = 57` on and 8.61 from `n = 73` on, and this repository's own
`s(70) >= 8.55` covers everything above `n = 69`, so monotonicity gives nothing
there; these four improve their own cases only.

`s(56)` and `s(72)` improve on what our own earlier certificates already gave.
Monotonicity from `s(55) >= 7.54` put `s(56)` at 7.54 and from `s(70) >= 8.55`
put `s(72)` at 8.55; the direct certificates raise those by 0.08 and 0.06.

## n = 26 and n = 29 have since been improved

[tokoharu/square-packing-density-bounds](https://github.com/tokoharu/square-packing-density-bounds)
proves `s(26) >= 1377/250 = 5.508` and `s(29) >= 571/100 = 5.71`, past the two
certificates here, and by monotonicity those also carry `n = 27, 30, 31`.

That work generalizes the basis from point masses to uniform densities on
axis-aligned rectangles, D4-symmetrized about the centre, so the quantity a
placement captures is an area integral rather than a sum of point weights. A
point is caught or missed outright; a rectangle is captured in proportion to
the overlap, which gives the optimizer a degree of freedom the point basis does
not have. For `n = 29` it reaches the better bound with *fewer* basis elements
(552 rectangles against 748 atoms here), so the gain is in what each element
can express, not in how many there are.

The certificates here are unaffected as proofs -- they still establish what
they claim -- but for these two cases they are no longer the strongest known.
Both of tokoharu's certificates were re-checked against their verifier,
compiled and run independently, as part of confirming this.

## s(29) >= 5.74, a rectangle-density certificate built here

`certificates/rect_n29_L574/` is a certificate in tokoharu's format proving
`s(29) >= 287/50 = 5.74`, above his own `571/100 = 5.71`. It was produced with
his solver, driven by `push.py`, the ladder driver we contributed to his
repository ([PR #1](https://github.com/tokoharu/square-packing-density-bounds/pull/1),
[PR #2](https://github.com/tokoharu/square-packing-density-bounds/pull/2), both
merged). Starting from his certified `n = 29` certificate at 5.71, the driver
raises the side one rung at a time, running his `engine.py` search, then his
`certify.py`, and keeping a rung only when the certificate is accepted. The
rungs that produced this file were 5.73, 5.7325, 5.73375, 5.735, 5.7375,
5.738125, 5.73875 and 5.74; every one of them was certified before the next
was attempted. The climb is still running; this is the highest certified rung
at the time of writing.

The directory holds the data his verifier reads and the verifier itself:

| file | meaning |
|---|---|
| `certified_candidate.json` | the certificate: `L = 287/50`, `B = 9977/10000`, 1000 rectangles (125 seed rectangles under `D4`) with exact rational densities |
| `certificate_input.txt` | the same data in the text form `verify.cpp` parses |
| `certificate_metadata.json` | exact total mass `283074999609155607507/10^19 = 28.3075` against budget 29, and the SHA-256 of the input |
| `verify.cpp`, `run_verify.py` | tokoharu's interval verifier and its runner, unchanged (MIT; `verify.cpp` SHA-256 `a75140df…`) |
| `verification_summary.json`, `verified_angles.jsonl` | the record of the accepting run: 201 angle cases, 6,220,710 nodes, every leaf lower bound at least `10001/10000` |

To re-check it (needs `g++`; about four minutes on four cores):

```bash
cd certificates/rect_n29_L574 && python3 run_verify.py --workers 4
```

It ends by writing `verification_summary.json` with `"status": "VERIFIED"`. We
re-ran it from these exact bytes on 2026-09-24 before publishing. The argument
behind `verify.cpp` — outward-rounded interval arithmetic, a certified
inscribed-polygon area for each rectangle overlap, derivative bounds over
centre boxes, and the same rational angular net as above — is tokoharu's and is
documented in his repository; nothing in the mathematics is ours. What is ours
is the driver and the machine time.

`src/verify.py` does not read this format: it checks point certificates only.

## How the proof works

Scatter finitely many points in the container and give each a nonnegative
rational weight. If every unit square that fits, at every orientation and
position, covers total weight at least 1, then `n` non-overlapping squares
cover at least `n`. Choose the weights so the total is strictly below `n` and
no such packing exists.

The certificate is the list of points and weights. Checking it means checking
five conditions, of which the fifth — that *every* placement covers mass 1 —
is the one that needs a computer. Two devices make it finite: a shrunken square
of side `B < 1` tested against a rational net of 201 directions, with
`B(1 + D) < 1` so the shrink absorbs the net's angular gap; and a sweep over
regions of centre positions rather than individual points.

This is the weighted fractional unavoidable-set method. It is not ours; see
[Attribution](#attribution).

## Verifying the certificates

### With this repository's checker

Requires Python 3.10+, NumPy.

```bash
pip install -r requirements.txt
python3 src/verify.py certificates/cert_n29_L557.json
```

It prints each condition as it decides it and ends with `VERIFIED`. It accepts
only JSON; a certificate is data, and loading one from a pickle would run
whatever the file contained.

Conditions 1 to 4 are decided exactly in `Fraction`. Condition 5 runs a
branch-and-bound recursion over centre boxes in float64 under a stated error
budget: `EPS = 1e-9` on geometric comparisons, mass threshold `1 + 1e-9`, boxes
not subdivided below `1e-7`. Coordinates stay under 100 in magnitude and each
compared quantity takes at most six floating-point operations, so rounding error
stays near `1e-13`; the mass is a sum of at most `10^4` nonnegative terms below
1, so its error stays near `1e-11`. Weights are rounded *up* to multiples of
`1e-8`, so rounding can only add mass.

Box counts, zero failures in each: 4,811,681 (`n=26`), 2,524,711 (`n=29`),
8,409,303 (`n=39`), 7,531,281 (`n=40`). Counts vary slightly between runs
because the split order is not deterministic; the outcome does not.

### With jlevy/squares' checker

[`jlevy/squares`](https://github.com/jlevy/squares) carries an independent
implementation that decides Condition 5 in exact integers on the weights'
common scale and returns the true minimum over event cells, rather than testing
a threshold in floating point. **It is the stronger check**, and all four
certificates pass it unmodified.

```bash
git clone https://github.com/jlevy/squares.git
cp src/check_with_sqpack.py certificates/*.json squares/
cd squares && python3 check_with_sqpack.py cert_n29_L557.json
```

```
n = 29   L = 557/100 = 5.57
atoms = 748   total mass = 453011/15625 = 28.992704   budget = 29
accepted = True   (13.8s)
  [ok  ] Condition 1 atoms carry the declared symmetry: 748 atoms closed under D4 about the centre
  [ok  ] Condition 2 total mass below n: total 453011/15625 against n = 29
  [ok  ] Condition 3 net reaches pi/4: final half-tangent 83/200, t^2 + 2t - 1 = 89/40000
  [ok  ] Condition 4 containment B(1 + D) < 1: B = 9977/10000, D = 83/40000, B(1 + D) = 399908091/400000000
  [ok  ] Condition 5 every reachable cell carries mass 1: least cell mass 1000003/1000000 at direction 0
=> s(29) >= 557/100 = 5.57
```

Results on one core, single worker:

| `n` | atoms | distinct under `D4` | total mass | margin under `n` | `verify` |
|---|---|---|---|---|---|
| 26 | 1376 | 179 | 646393601/25000000 = 25.855744 | 0.144256 | accepted, 28.2s |
| 29 | 748 | 100 | 453011/15625 = 28.992704 | **0.007296** | accepted, 13.8s |
| 39 | 2724 | 362 | 481487971/12500000 = 38.519038 | 0.480962 | accepted, 73.4s |
| 55 | 3196 | 410 | 1362984297/25000000 = 54.519372 | 0.480628 | accepted, 131.4s |
| 70 | 8060 | 1058 | 108946291/1562500 = 69.725626 | 0.274374 | accepted, 548.5s |
| 40 | 1892 | 250 | 975019903/25000000 = 39.000796 | 0.999204 | accepted, 45.1s |

The `n = 29` margin is the interesting one: the weights land `0.0073` under
budget, close to the ceiling the method allows. That is why `n = 29` was the
hardest of the three to find, while `n = 39` had room to spare.

## Certificate format

Each JSON file carries

| field | meaning |
|---|---|
| `n` | number of unit squares |
| `L` | container side, exact rational string |
| `B` | shrink factor `9977/10000` |
| `net` | the direction net as a rule: `theta_r = 2*atan(r*83/40000)`, `r = 0..200` |
| `atoms` | `[x, y, weight]` triples, exact rational strings |
| `total_mass` | sum of weights |
| `claim`, `verification` | the statement proved and the command that checks it |

The net is stored as a rule rather than a list; the half-angle tangents are
exactly `r * 83/40000`. `src/check_with_sqpack.py` shows the one-line
conversion to the form `jlevy/squares` expects.

## Finding the certificates

`src/lp.py` and `src/certify.py` search for them. The program is a covering
linear program over `D4` orbit representatives, solved with HiGHS through SciPy,
with rows generated by using the Condition 5 sweep as a separation oracle and
columns generated from dual reduced costs. A run is abandoned once the LP
optimum reaches `n`, since further rows only raise it.

```bash
python3 src/certify.py --n 29 --L 557/100
```

Runs are long and memory-hungry; the searches behind these four certificates
took hours each on a 128 GB machine, and `certify.py` checkpoints its own
progress so a run can resume. Those checkpoints are pickles it wrote itself
and are not part of the verification path.

## Attribution

The method is not ours.

- **Walter Stromquist** introduced unavoidable point sets with unit weights
  (unpublished memos 1984–85; *Packing 10 or 11 Unit Squares in a Square*,
  Electron. J. Combin. 10 (2003) #R8).
- **Hiroshi Nagamochi** introduced weighted score systems tuned by hand
  (Electron. J. Combin. 12 (2005) #R37).
- **Sam Burns** and **Gustavo Massaccesi** fractionalized the weights and
  introduced the exact rational direction net with the `B(1 + D) < 1` shrink,
  in August 2026. Our `B = 9977/10000` on 201 directions is a parameter choice
  within their framework.
- **[jlevy/squares](https://github.com/jlevy/squares)** added row generation
  via a separation oracle, dual-priced column generation, and branch-and-bound
  as a second Condition 5 decider, and documents the whole pipeline.

What is ours is the observation that nobody had run this machinery above
`n = 21`, the search runs, and the certificates. [`docs/prior-art-method.md`](docs/prior-art-method.md)
breaks the method into six components and attributes each;
[`docs/prior-art-results.md`](docs/prior-art-results.md) records the search for
prior publication of the bounds themselves. Japanese originals are alongside as
`*.ja.md`.

If any attribution here is wrong, please open an issue and we will correct it.

## Layout

```
certificates/   the ten point certificates as JSON, and rect_n29_L574/ in tokoharu's format
src/verify.py            our checker
src/check_with_sqpack.py adapter for the jlevy/squares checker
src/lp.py, src/certify.py the search
docs/lower-bounds.md      write-up of the argument and the numbers
docs/prior-art-method.md  which parts of the method are prior art, and whose
docs/prior-art-results.md search for prior publication of these bounds
docs/prior-art-*.ja.md    Japanese originals of the two notes above
```

## Status

Computer-assisted certificates, checked by two independent implementations.
They have not been peer reviewed. [jlevy/squares](https://github.com/jlevy/squares)
records the point bounds for `n = 39, 40, 53, 55, 56, 69, 70, 72` in its
frontier register, in both the reported and the verified lane, after an exact
replay of these files with its own checker (evidence
`E-wand125-point-source-replay`, 2026-09-22).

Parts of this work were produced with AI assistance under human direction.

## License

MIT. See `LICENSE`.
