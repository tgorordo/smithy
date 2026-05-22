#!/usr/bin/env -S uv run python

import cgi, cgitb
import sys, os
import html

import polars as pl

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../smithy/src"
        )
    )
)
from smithy import smith_set

cgitb.enable()

form = cgi.FieldStorage()

if 'spreadsheet' in form:

    fileitem = form['spreadsheet']
    if fileitem.filename:
        filename = os.path.basename(fileitem.filename)
        filepath = os.path.join("/tmp", filename)

        with open(filepath, 'wb') as f:
            f.write(fileitem.file.read())
        print(f"<h2>Upload Successful!</h2>")

        try:
            if filename.endswith(".csv"):
                df = pl.read_csv(filepath)
            elif filename.endswith((".xlsx", ".xls")):
                df = pl.read_excel(filepath)
            else:
                message = """
                <h1>Error</h1>
                <p>File extension is not valid. Use CSV (.csv) or Excel (.xlsx, .xls).</p>
                <p><a href="../smithy.html">Go Back</a></p>
                """

            # Normalize
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

            smiths = smith_set(df) # Solve!

            message = """
            <h1>The Smith set winners are:</h1>
            {smiths}
            <p><a href="../smithy.html">Go Back</a></p>
            """

        except Exception as e:
            message = """
            <h1>Error<h1>
            <p>Internal Error Encountered: {e}
            <p><a href="../smithy.html">Go Back</a></p>
            """
                
    else:
        message = """
        <h1>Error</h1>
        <p>Filename not found/valid.</p>
        <p><a href="../smithy.html">Go Back</a></p>
        """

else:
    message = """
    <h1>Error</h1>
    <p>No file field found in the form.</p>
    <p><a href="../smithy.html">Go Back</a></p>
    """

response = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> Smithy - RCV Ballot Counter </title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
   {message}
</body>
<footer>
  <hr>
  <p>Author: <a href="https://pages.uoregon.edu/tgorordo">Thomas (Tom) C. Gorordo</a>
     Source: <a href="https://github.com/tgorordo/pages.uoregon.edu">pages.uoregon.edu/tgorordo</a>,
             <a href="https://github.com/tgorordo/smithy">smithy</a></p>
</footer> 
"""

print(response)
