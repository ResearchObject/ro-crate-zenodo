# User Guide - Under Construction

## Install requirements

```
pip install -r requirements.txt
```

## Set up a Zenodo personal access token

Create a file called `~/.config/zenodo.ini` on your computer with the following contents:

```ini
# if using the Zenodo sandbox
[zenodo:sandbox]
sandbox_api_token = 

# if using the real Zenodo
[zenodo]
api_token = 
```

Now create a Zenodo access token:

1. Register for a Zenodo account if you don’t already have one.
1. Go to your profile and select Applications.
1. You should see a section called "Personal access tokens." Click the "New token" button.
1. Give the token a name that reminds you of what you're using it for (e.g. _RO-Crate uploader token_)
1. Select the scopes `deposit:write` and `deposit:actions` [confirm later].
1. Click "Create."
1. Copy the access token into your `~/.config/zenodo.ini` file.

The resulting file should look like this:

```ini
# if using the Zenodo sandbox
[zenodo:sandbox]
sandbox_api_token = your-sandbox-token-here

# if using the real Zenodo
[zenodo]
api_token = your-token-here
```

`ro-crate-uploader` will read this token whenever it connects to Zenodo in order to perform actions under your account. It's recommended to use the Zenodo sandbox until you're confident using `ro-crate-uploader`.
