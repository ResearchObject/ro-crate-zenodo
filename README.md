# ro-crate-zenodo

Upload RO-Crates to Zenodo and automatically fill the Zenodo metadata.

This package uses the legacy Zenodo API and is not compatible with other InvenioRDM instances. For RO-Crate uploads using the InvenioRDM API, use the [rocrate-inveniordm](https://github.com/ResearchObject/ro-crate-inveniordm) package instead.

## Setup

### Install the package

Install from PyPI using `pip` or your preferred package manager:
```
pip install rocrate-zenodo
```
### Set up a Zenodo personal access token

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
1. Select the scopes `deposit:write` and `deposit:actions`.
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

The `rocrate-zenodo` package will read this token whenever it connects to Zenodo in order to perform actions under your account. It's recommended to use the Zenodo sandbox until you're confident using the package.

## Usage

To upload a crate to Zenodo sandbox:
```
rocrate_zenodo -s demo/demo_crate
```
Replace `demo/demo_crate` with the path to the RO-Crate directory you want to upload. The `-s` flag sets the destination to the Zenodo sandbox; you can omit `-s` to upload to real Zenodo.

Once complete, you should see the draft record in your Zenodo dashboard.

For further help and options, run:
```
rocrate_zenodo --help
```

## Tips

1. Set `givenName` and `familyName` on authors of the RO-Crate. This ensures that author names are formatted correctly in Zenodo.
2. Use the SPDX URI for the top-level license, e.g. `https://spdx.org/licenses/CC-BY-NC-SA-4.0.html`. Other URIs for licenses are not currently well supported.
3. Check your upload carefully in the Zenodo web interface before publishing. Not all metadata will be carried across from the RO-Crate, and some may be transferred incorrectly. Please [raise an issue](https://github.com/ResearchObject/ro-crate-zenodo/issues/new) if you notice a discrepancy.

## For Developers

See the [Developer Guide](docs/developer_guide.md).
