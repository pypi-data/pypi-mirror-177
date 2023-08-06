#!/usr/bin/env python3
from os.path import abspath, basename, dirname, join
import toml
import json
import sys
import requests

PROJECTDIR = dirname(abspath(dirname(__file__)))
pyproject_file = join(PROJECTDIR, "pyproject.toml")


# handle status
def handle_status(r: requests.Response):
    print("Status: %s" % r.status_code)
    if r.status_code >= 400:
        print(r.json())
        sys.exit(1)


# get the access token
if len(sys.argv) != 3:
    print("Usage: zenodo.py <access_token> <zip_file>")
    sys.exit(1)

# get the access token
ACCESS_TOKEN = sys.argv[1]
zip_file = sys.argv[2]
params = {"access_token": ACCESS_TOKEN}

# access api
print("Accessing zenodo API...")
r = requests.get(f"https://zenodo.org/api/deposit/depositions", params={"sort": "mostrecent", **params})
handle_status(r)

# check for current record
current_record = [record for record in r.json() if record["title"] == "omni"]
if len(current_record) == 0:
    current_record = None
else:
    current_record = current_record[0]

# if current record exists, update it
if current_record:
    deposition_id = current_record["record_id"]
    # create a new version of the deposition
    r = requests.post(f"https://zenodo.org/api/deposit/depositions/{deposition_id}/actions/newversion", params=params)
    handle_status(r)

    # get the link for the latest draft
    latest_draft = r.json()["links"]["latest_draft"]

    # get the current file id
    current_file_id = current_record["files"][0]["id"]

    # delete the existing file record
    r = requests.delete(latest_draft + "/files/" + current_file_id, params=params)
    handle_status(r)

    # get the bucket url for the latest draft
    r = requests.get(latest_draft, params=params)
    handle_status(r)
    bucket_url = r.json()["links"]["bucket"]

    # set the deposition url
    deposition_url = latest_draft
else:  # else ready new upload
    print("Creating new upload...")
    r = requests.post("https://zenodo.org/api/deposit/depositions", params=params, json={})
    deposition_id = r.json()["id"]
    handle_status(r)

    # get bucket url
    bucket_url = r.json()["links"]["bucket"]

    # deposition url
    deposition_url = f"https://zenodo.org/api/deposit/depositions/{deposition_id}"

# form file upload
print("Uploading file...")
with open(zip_file, "rb") as fp:
    r = requests.put(
        "%s/%s" % (bucket_url, basename(zip_file)),
        data=fp,
        params=params,
    )
handle_status(r)
print("\nFile Metadata:")
print(r.json())
print("")

# load the zenodo file
data = {"metadata": {}}
with open(join(PROJECTDIR, ".zenodo.json"), "r") as fp:
    data["metadata"] = json.load(fp)
# add the version
sys.path.append(PROJECTDIR)
from omni.version import __version__  # noqa: E402

data["metadata"]["version"] = __version__
# add description
config = toml.load(pyproject_file)
data["metadata"]["description"] = config["project"]["description"]

# add metadata to record
print("Adding metadata to record...")
r = requests.put(
    deposition_url,
    params=params,
    data=json.dumps(data),
    headers={"Content-Type": "application/json"},
)
handle_status(r)

# publish record
print("Publishing record...")
r = requests.post("https://zenodo.org/api/deposit/depositions/%s/actions/publish" % deposition_id, params=params)
handle_status(r)
