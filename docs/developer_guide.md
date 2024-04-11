# Developer Guide - Under Construction

## Environment

Install dependencies:

```bash
# general dependencies
pip install -r requirements.txt
# dev dependencies
pip install flake8 black pytest
```

Configure Zenodo access token(s) as in [user guide - Set up a Zenodo personal access token](user_guide.md#set-up-a-zenodo-personal-access-token).

## Run tests

Beware that tests may make Zenodo uploads using your access token.

```bash
cd ro_crate_uploader
pytest
```
