import polars as pl
import numpy as np


def irv_from_rcv(ballots: pl.DataFrame, method: str = "bigslow") -> list[str]:
    """
    Compute the set of all-paths IRV winners from an RCV ballot.

    parameters
    ---
    ballots: pl.DataFrame
    An RCV table of ballots.

    method: str
    Either "bigslow" or "smallfast" for selecting an internal method for counting
    first-choices during IRV rounds. Defaults to "bigslow" but you can use "smallfast"
    so long as the table of ballots is expected to fit in a reasonable numpy array (after compression).

    returns
    ---
    winners: list[srt]
    A lexicographically sorted list of IRV winners. If a candidate wins every elimination path
    then this set will contain only one entry, otherwise it will contain all candidates that win
    at least one IRV elimination path.
    """
    compressed = ballots.group_by(ballots.columns).len().rename({"len": "count"})
    return sorted(_irv_winners(compressed, method=method))


def _fst_counts_bigslow(compressed: pl.DataFrame) -> pl.DataFrame:

    surviving = [c for c in compressed.columns if c != "count"]

    fstcexpr = (
        pl.concat_list([pl.col(c) for c in surviving])
        .list.arg_min().map_elements(lambda i: surviving[i], return_dtype=pl.String).alias("first_choice")
    )

    tally = (
        compressed.with_columns(fstcexpr)
        .group_by("first_choice")
        .agg(pl.col("count").sum())
        .filter(pl.col("first_choice").is_not_null())
    )
    return tally


def _fst_counts_smallfast(compressed: pl.DataFrame) -> pl.DataFrame:

    surviving = [c for c in compressed.columns if c != "count"]

    a = compressed.select(surviving).to_numpy()

    cs = compressed["count"].to_numpy()

    fstc_idxs = np.argmin(a, axis=1)

    tally = {c: 0 for c in surviving}
    for i, c in zip(fstc_idxs, cs):
        tally[surviving[i]] += int(c)

    return pl.DataFrame(
        {"first_choice": surviving, "count": [tally[c] for c in surviving]}
    )


def _irv_round(compressed: pl.DataFrame, method="bigslow"):

    if method == "bigslow":
        count_fn = _fst_counts_bigslow
    elif method == "smallfast":
        count_fn = _fst_counts_smallfast
    else:
        raise NotImplementedError(
            f"Error: _fst_counts method={method} not implemented."
        )

    tally = count_fn(compressed)

    eliminate = tally.filter(pl.col("count") == pl.col("count").min())[
        "first_choice"
    ].to_list()

    for e in eliminate:
        surviving = [c for c in compressed.columns if c not in ("count", e)]
        yield (
            compressed.select(surviving + ["count"])
            .group_by(surviving)
            .agg(pl.col("count").sum())
        )


def _irv_winners(compressed, method="bigslow"):

    surviving = [c for c in compressed.columns if c != "count"]
    if len(surviving) == 1:
        return set(surviving)

    winners = set()
    for branch in _irv_round(compressed, method=method):
        winners |= _irv_winners(branch, method=method)
    return winners
