# User Guide - Under Construction

## Install the project

```
git clone https://github.com/ResearchObject/ro-crate-uploader.git
cd ro-crate-uploader
pip install -r requirements.txt
pip install .
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

## Run the code

Run the `rocrate_zenodo` command in your terminal. Use the `-s` flag to upload to Zenodo sandbox, or omit it to upload to real Zenodo.
```
rocrate_zenodo -s demo/demo_crate
```
Replace `demo/demo_crate` with the path to the RO-Crate directory you want to upload.

Once complete, you should see the draft record in your Zenodo dashboard.

Further info:
```
rocrate_zenodo --help
```

## Tips

1. Set `givenName` and `familyName` on authors of the RO-Crate.
2. Use the SPDX URI for the top-level license, e.g. `https://spdx.org/licenses/CC-BY-NC-SA-4.0.html`
3. Check your upload carefully before publishing.
