# Smithy
*A simple Smith set solver for ranked-choice ballots.* 

The Smith set is the minimal set of election candidates which can beat all others pairwise
(by simple majority ranking preference) - if there is a single winner in the set they are 
guaranteed the standard Condorcet i.e. Majority winner (they beat all others pairwise). 

`smithy` currently identifies the set by brute-force search which is combinatoric complexity
in the worst case (TODO: better [algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm)) 
but appears approximately O(n^2) on-average in the number of candidates for typical/random ballots, 
and linear in the number of ballots.


## Usage
`smithy` can be used a few different ways: as a CLI command, via a web form upload, 
or imported as a python package (TODO: a small [GUI](https://doc.qt.io/qtforpython-6/)).


### CLI Command
`smithy` provides a [`click`](https://click.palletsprojects.com/en/stable/) 
CLI command defined in `src/smithycmd.py` which can be invoked a couple of ways:

- The [GitHub Releases Page](https://github.com/tgorordo/smithy/releases) provides standalone
CLI executables bundled using [PyInstaller](https://pyinstaller.org/en/stable/index.html)
for linux and windows on `x86_64` and linux on `aarch64`. Downloading the appropriate
executable should give you access to the `smithycmd` CLI command.

- Alternatively, if you are using `uv` (see [Development](#Development)), you can invoke 
this in your shell as `uv run src/smithycmd.py [...]` from within the repo after cloning it locally.

In either case, the command expects the same argument structure:
TODO

While plain output is the default, so that the command can easily be used in a unix-pipe
or `stdio` workflows, it can also pretty-print its output for your reading pleasure
using [`rich`](https://rich.readthedocs.io/en/stable/introduction.html) if you pass it the 
`--pretty` (or `-p`) flag.


### UOregon CGI Application
[**This** `pages.uoregon.edu` page](https://pages.uoregon.edu/tgorordo/files/smithy/src/cgi/form.html)
hosts a [CGI form](https://service.uoregon.edu/TDClient/2030/Portal/KB/ArticleDet?ID=43069)
which accepts a `.csv` or `.xls`(`x`) upload of a ballot-box and responds with the resulting
Smith set. The application can typically handle ~100s of candidates and ~10ks of votes 
before running into hosting resource limitations and timing out (pathological cases, involving
many or large cycles, or especially a large cyclic tie, may perform worse and are not extensively tested).


### Python Package
The `smithy` python package primarily provides the function `smith_set(ballot_box_df)` 
(defined in `src/smithy), which returns the smith set given a 
[polars](https://docs.pola.rs/api/python/stable/reference/index.html) 
dataframe `ballot_box_df` whose columns are candidates and whose rows are RCV ballots.

e.g. `smithy` can be imported into a [marimo](https://docs.marimo.io/#highlights) notebook
as seen in `test/test_nb.py` - if you're using `uv` you can launch marimo via 
`uv run marimo --edit` and navigate to that example notebook 
(`just marimo` is an available shorthand if you are using the `just` taskrunner -- 
see [Development](#Development)). Cloning `smithy` then working in scratch notebooks within the repo
(e.g. makeing your own `nbs/` directory)
is probably the easiest way to use it if you need to do some of cleanup of the tabular 
data before invocation - just do your cleanup in a notebook using 
[polars](https://docs.pola.rs/py-polars/html/reference/) then pass a tidy dataframe to `smith_set(df)`.

Of course, you can also import into any python script or package for a more involved project
as well:
- If you're using `uv` adding `smithy` should be as simple as
```bash
uv add git+https://github.com/tgorordo/smithy.git
```
- Alternatively, if you're using the more default `pip` you can make it available by
```bash
git clone https://github.com/tgorordo/smithy.git # or submodule add somewhere appropriate in your project
cd smithy
pip install .
```
(if you're new to pip-venvs, 
[this brief guide might be helpful](https://pages.uoregon.edu/tgorordo/courses/uoph410-510a_Image-Analysis/setup.html)).


## Development
Current development tooling is based on the [`uv`](https://docs.astral.sh/uv/) Python package and
project manager. A [`justfile`](https://github.com/casey/just) lists some common useful
task commands. A simple [`shell.nix`](https://nix.dev/tutorials/first-steps/declarative-shell.html)
can be used to load these tools into a local environment, and you might find
[`direnv`](https://github.com/direnv/direnv) a convenient pairing to `nix` - but just having a 
system-provided `uv` available is more than enough to use and develop `smithy`.



### Formatting, Checking, Testing and Locking
Source can be formatted using [`ruff`](https://docs.astral.sh/ruff/) by running
```bash
uv run ruff format src test
```
(or `just format`)
which should be done before any `git` commit.

This is not really taken full advantage of at the moment, but type hints can be checked
by running [pyright](https://github.com/microsoft/pyright)
```bash
uv run pyright src
```
(or `just check`).

A [pytest](https://docs.pytest.org/en/stable/) test suite can be run as
```bash
uv run pytest -vvv --tb=short --log-cli-level=INFO
```
(or `just test`).

Dependencies can be locked by running
```bash
uv lock
uv pip compile pyproject.toml -o requirements.txt --group dev
```
(or `just lock`).


### Bundling, Releases, Deployment and Cleanup
Bundling with [PyInstaller](https://pyinstaller.org/en/stable/index.html) can be done by
```bash
uv run pyinstaller --clean -F src/cmd.py --name smithycmd
```
which will output an executable `smithycmd` for the CLI in `dist/`, which can be uploaded
to the latest [GitHub Releases Page](https://github.com/tgorordo/smithy/releases).

Deploying the main CGI page at 
[`pages.uoregon.edu/tgorordo/files/smithy/src/cgi`](https://pages.uoregon.edu/tgorordo/files/smithy/src/cgi)
requires shell or SFTP access to [my `pages.uoregon.edu`](https://pages.uoregon.edu/tgorordo),
which you won't get unless you're [me](https://github.com/tgorordo).

If you want to deploy it to your own `pages.uoregon.edu` page, then it should be enough to
ensure you have [CGI set up](https://service.uoregon.edu/TDClient/2030/Portal/KB/ArticleDet?ID=43069)
then SFTP into `sftp.uoregon.edu` and `put -r smithy` (or git clone when `ssh`ed into 
`shell.uoregon.edu`) wherever you'd like in your `public_html`, ensure `smithy.cgi` has
`chmod 755` permissions, 
[standalone install `uv` for your user](https://docs.astral.sh/uv/getting-started/installation/) 
then run `uv sync` from somewhere inside the `smithy` directory. Navigating to the `smithy.cgi`
 file in `pages.uoregon.edu/YOUR_USER/.../cgi/smithy.cgi` should give you a working form.

If you're using `just` you can cleanup working files by running `just clean` and can fully
wipe your `uv` generated `.venv` with `just wipe` (if you want manual versions of those,
check the `justfile` definition). It's probably best to do this before any commit as well,
though probably not required if you're careful or have `.gitignore` updated appropriately
for any changes you made.

