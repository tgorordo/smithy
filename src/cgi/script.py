import traceback
import sys, os
import html

import re

import polars as pl

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../smithy/src"
        )
    )
)
from smithy import smith_set

print("Content-Type: text/html\n")
message = ""

content_type = os.environ.get("CONTENT_TYPE", "")
content_length = int(os.environ.get("CONTENT_LENGTH", 0) or 0)
boundary = content_type.split("boundary=")[-1].encode()

body = sys.stdin.buffer.read(content_length)
parts = body.split(b"--" + boundary)

spreadsheet = None

for part in parts:
    if b'Content-Disposition' in part and b'name="spreadsheet"' in part:
        header, _, data = part.partition(b"\r\n\r\n")

        filename_match = re.search(br'filename="([^"]+)"', header)
        if filename_match:
            filename = filename_match.group(1).decode()
            filedata = data.rstrip(b"\r\n--")

            spreadsheet = (filename, filedata)
            break


if spreadsheet is not None:

    filename, filedata = spreadsheet

    if filename and filedata:
        filepath = os.path.join("/tmp", filename)

        with open(filepath, 'wb') as f:
            f.write(filedata)

        try:
            if filename.endswith(".csv"):
                df = pl.read_csv(filepath)
            elif filename.endswith((".xlsx", ".xls")):
                df = pl.read_excel(filepath)
            else:
                message = """
                <h1>Error</h1>
                <p>File extension is not valid. Use CSV (.csv) or Excel (.xlsx, .xls).</p>
                <p><a href="form.html">Go Back</a></p>
                """

            if df is not None:
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

                message = f"""
                <h1>The Smith set winners are:</h1>
                {smiths}
                <p><a href="form.html">Go Back</a></p>
                """
            else:
                message = """
                <h1>Error</h1>
                <p>DataFrame was empty.</p>
                <p><a href="form.html">Go Back</a></p>
                """


        except Exception as e:
            message = f"""
            <h1>Error</h1>
            <p>Internal Error Encountered: {e}
            <p><a href="form.html">Go Back</a></p>
            """
            traceback.print_exc()

    else:
        message = """
        <h1>Error</h1>
        <p>Filename or File Data not found/valid in form submission.</p>
        <p><a href="form.html">Go Back</a></p>
        """

else:
    message = """
    <h1>Error</h1>
    <p>No file field found in the form.</p>
    <p><a href="form.html">Go Back</a></p>
    """

print("""
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
""")
print(message)
print("""
</body>
<footer>
  <hr>
  <p>Author: <a href="https://pages.uoregon.edu/tgorordo">Thomas (Tom) C. Gorordo</a>
     Source: <a href="https://github.com/tgorordo/pages.uoregon.edu">pages.uoregon.edu/tgorordo</a>,
             <a href="https://github.com/tgorordo/smithy">smithy</a></p>
</footer>
</html>
""")
