# Developer Guide - Under Construction

## Environment

### Poetry setup

If you do not already have `poetry` installed, install it following the [Poetry installation documentation](https://python-poetry.org/docs/#installation).

Then install dependencies from `poetry.lock`:

```bash
poetry install
```

Activate the virtual environment:
```bash
poetry shell
```

### Zenodo access token setup

Configure Zenodo access token(s) as in [user guide - Set up a Zenodo personal access token](user_guide.md#set-up-a-zenodo-personal-access-token).

## Run tests

Beware that tests can make Zenodo uploads using your access token.

In the root directory:
```bash
pytest
```
