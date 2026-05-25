# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click>=8.4.1",
#     "rich>=15.0.0",
#     "polars>=1.40.1"
# ]
# ///
import click

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

import polars as pl
from smithy import smith_set

@click.command()
@click.argument("spreadsheet", type=click.Path(exists=True, dir_okay=False))
def cli(spreadsheet: str) -> None:
    """
    Compute the Smith set from a ranked-choice ballot spreadsheet.

    The Smith set is the minimal set of candidates which can beat all others pairwise - if there is a single winner
    in the set they are guaranteed the Condorcet i.e. Majority winner.
    """

    console = Console()

    try:
        # Load spreadsheet
        if spreadsheet.endswith(".csv"):
            df = pl.read_csv(spreadsheet)

        elif spreadsheet.endswith((".xlsx", ".xls")):
            df = pl.read_excel(spreadsheet)

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

        # Preview table
        preview = Table(title="Ballot Box")

        for col in df.columns:
            preview.add_column(col)

        for row in df.head(5).iter_rows():
            preview.add_row(*map(str, row))

        console.print(preview)

        # Results
        console.print()

        console.print(
            Panel.fit(
                "\n".join(f"• {c}" for c in smiths),
                title="Resulting Smith Set",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

        raise SystemExit(1)

if __name__ == "__main__":
    cli()
