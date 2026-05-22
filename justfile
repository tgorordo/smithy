list:
  just --list --unsorted

run spreadsheet:
  uv run smithy {{spreadsheet}}

marimo:
  uv run marimo --edit

example:
  uv run python src/main.py test/test_ballot.csv

format:
  uv run ruff format src test

check:
  uv run pyright src

test:
  uv run pytest -vvv --tb=short --log-cli-level=INFO

compile:
  uv run pyinstaller --clean -F src/cmd.py --name smithycmd
  
clean:
  uv run pyclean src test
  uv run ruff clean
  rm -rf main.spec cli.spec build dist .pytest_cache .hypothesis .benchmarks __marimo__
  
wipe:
  just clean
  rm -rf .venv

lock:
  uv lock
  uv pip compile pyproject.toml -o requirements.txt --group dev
