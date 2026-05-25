# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click>=8.4.1",
#     "rich>=15.0.0",
#     "polars>=1.40.1"
# ]
# ///
import sys, io
import click

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

import polars as pl
from smithy import smith_set

@click.command()
@click.argument("ballots", type=click.Path(exists=True, dir_okay=False))
@click.option("--show-ballots", "-b", is_flag=True, help="Show relevant ballots (after selections).")
@click.option("--pretty", "-p", is_flag=True, help="Pretty-print output.")
def cli(ballots: str, show_ballots=False, pretty=False) -> None:
    """
    Compute the Smith set from a box of ranked-choice ballots -- .csv or .xls(x).

    The Smith set is the minimal set of candidates which can beat all others pairwise
    (simple ranking majority) - if there is a single winner in the set, 
    they are guaranteed the Condorcet i.e. Majority winner.
    """

    console = Console()

    try:
        # Load ballots
        if ballots.endswith(".csv"):
            df = pl.read_csv(ballots)

        elif ballots.endswith((".xlsx", ".xls")):
            df = pl.read_excel(ballots)

        else:
            console.print(
                "[bold red]Unsupported file type.[/bold red]\nUse CSV or Excel."
            )
            raise SystemExit(1)

        # Normalize numerical dataframe entries
        df = df.with_columns(
            [
                pl.col(c)
                .cast(pl.Utf8)
                .str.strip_chars()
                .cast(pl.Int64, strict=False)
                .fill_null(0)
                for c in df.columns
            ]
        )

        # Compute Smith set
        smiths = smith_set(df)


        if show_ballots and pretty:
            preview = Table(title="Ballot Box")

            for col in df.columns:
                preview.add_column(col)

            for row in df.head(5).iter_rows():
                preview.add_row(*map(str, row))

            console.print(preview)
            console.print()
        elif show_ballots and not pretty:
            buf = io.StringIO()
            df.write_csv(buf)
            console.print(buf.getvalue())
            console.print("---")

        if pretty:
            console.print(
                Panel.fit(
                    "\n".join(f"• {c}" for c in smiths),
                    title="Resulting Smith Set",
                    border_style="green",
                )
            )
        else:
            console.print(", ".join(f"{c}" for c in smiths))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

        raise SystemExit(1)

if __name__ == "__main__":
    cli()
