# Refactor: imrw ops module

## Scope

`src/imrw/ops.py` — the module containing the library's two public functions
`imread` and `imwrite`. Diagnosed via `/refactor` sweep on 2026-04-11.

## Context summary

Sources read:
- `CLAUDE.md` (project guidance)
- `src/imrw/__init__.py`, `src/imrw/ops.py`
- `tests/test_ops.py`
- `git log` (recent history: shape/dtype validation, grayscale/RGBA write tests,
  rename to `imrw`)

## Selected findings

### F-01: imread/imwrite are not inverses on RGBA

- **Location**: `src/imrw/ops.py:8-10` (and its asymmetry with `src/imrw/ops.py:24`)
- **Category**: `gap` (MECE)
- **Observation**: `imread` unconditionally calls `.convert("RGB")`, always
  returning `HxWx3`. `imwrite` explicitly accepts 4-channel arrays
  (`shape[2] in (1, 3, 4)`) and writes them via PIL's RGBA mode. No 4-channel
  read path exists.
- **Reconstruction attempt**: The pair exists to let a user move a numpy image
  to disk and back. The MECE partition of "valid image layouts" the library
  claims to support is `{gray, RGB, RGBA}` — that set is explicit in
  `imwrite`'s validation.
- **Failure point**: The same partition is not honored on the read side. RGBA
  has a write cell but no read cell, so the library's own accepted layouts
  don't roundtrip. A user who does
  `imwrite(p, rgba); assert_equal(rgba, imread(p))` silently loses alpha. The
  CLAUDE.md line "imread always returns HxWx3 RGB" documents the asymmetry but
  does not justify it — it is a restatement, not a reason.
- **Chosen direction**: **(a) preserve source mode on read.** `imread` returns
  `HxWxC` where C matches the file's layout: `HxW` for grayscale (PIL mode L),
  `HxWx3` for RGB, `HxWx4` for RGBA. Other PIL modes (P, 1, CMYK, ...) are
  converted to RGB as a fallback so the function still always succeeds on any
  image PIL can open.
- **Axes**: Impact: med, Confidence: high, Effort: S

### F-02: duplicated `ndim == 3` guard

- **Location**: `src/imrw/ops.py:24` and `src/imrw/ops.py:30`
- **Category**: `complexity` (Feynman)
- **Observation**: Two adjacent `if img.ndim == 3:` blocks. First validates
  channel count, second squeezes a singleton channel dim.
- **Reconstruction attempt**: Each block exists for a distinct invariant
  (reject bad channel counts; adapt `HxWx1` to PIL's `HxW`). Splitting them
  should be justified by the two concerns having different exit behavior (one
  raises, one rebinds).
- **Failure point**: The split doesn't save anything — both sit inside the
  same `ndim == 3` cone and could share the check. Nothing in the current
  layout makes the separation load-bearing; it's just sequential code that
  repeats a branch.
- **Chosen direction**: Collapse into a single `if img.ndim == 3:` block
  containing channel validation followed by the singleton-dim squeeze.
- **Axes**: Impact: low, Confidence: high, Effort: S

## Refactoring constraints

- All existing tests in `tests/test_ops.py` must continue to pass unchanged.
- Public API surface (`imread`, `imwrite` names and import paths) stays
  identical.
- `imwrite` behavior is unchanged — only `imread` gains new return shapes.
- The new `imread` contract: returns an `HxW` uint8 array for grayscale
  sources, `HxWx3` for RGB sources, `HxWx4` for RGBA sources, and falls back
  to `HxWx3` RGB for any other PIL mode.
- Update `CLAUDE.md`'s "imread always returns H x W x 3 uint8 RGB" line to
  reflect the new contract.
- New tests must cover the RGBA roundtrip (the motivating gap) and at least
  one grayscale roundtrip. Keep the existing RGB roundtrip.

## Success criteria

- `imwrite(p, rgba); np.array_equal(rgba, imread(p))` is `True` for an RGBA
  uint8 array.
- `imwrite(p, gray_2d); np.array_equal(gray_2d, imread(p))` is `True` for a
  2D uint8 array.
- Existing tests pass unchanged.
- Re-running the Feynman reconstruction on `imread` no longer stalls on "why
  does this discard alpha?" — the partition `{gray, RGB, RGBA}` is now
  symmetric between read and write.
- Re-running the Feynman reconstruction on `imwrite`'s validation block no
  longer notes a duplicated `ndim == 3` check.
