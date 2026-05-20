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

compile:
  uv run pyinstaller src/main.py

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
