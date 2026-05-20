import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from pathlib import Path

    return (mo,)


@app.cell
def _():
    import polars as pl
    from smithy import smith_set

    return pl, smith_set


@app.cell
def _(mo, pl):
    df = pl.read_csv(mo.notebook_dir() / "test_ballot.csv")
    df = df.with_columns([ pl.col(c) # make safe, clean up
                             .cast(pl.Utf8)
                              .str.strip_chars()
                              .cast(pl.Int64, strict=False).fill_null(df.width + 1)
                                 for c in df.columns ])
    df
    return (df,)


@app.cell
def _(df, smith_set):
    smith_set(df) # find the smith set (should be "Alice" and "Bob" as a pair)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
