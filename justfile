list:
  just --list --unsorted

run *args:
  uv run src/smithycmd.py {{args}}

marimo:
  uv run marimo --edit

format:
  uv run ruff format src test

check:
  uv run pyright src

test:
  uv run pytest -vvv --tb=short --log-cli-level=INFO

compile:
  uv run --with-requirements src/smithycmd.py pyinstaller --clean -F src/smithycmd.py
  
clean:
  uv run pyclean src test
  uv run ruff clean
  rm -rf smithycmd.spec build dist .pytest_cache .hypothesis .benchmarks __marimo__
  
wipe:
  just clean
  rm -rf .venv

lock:
  uv lock
  uv pip compile pyproject.toml -o requirements.txt --group dev
