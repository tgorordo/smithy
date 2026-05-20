list:
  just --list

run spreadsheet:
  uv run smithy {{spreadsheet}}

check:
  uv run pyright src

test:
  uv run pytest -vvv --tb=short --log-cli-level=INFO

format:
  uv run ruff format src test

example:
  uv run python src/main.py test/test_ballot.csv

compile:
  uv run pyinstaller --clean -F src/main.py --name smithy
  

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
