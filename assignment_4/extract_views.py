# %% Verification Functions
import datetime
import json
import pprint
from pathlib import Path

import boto3
import requests

pp = pprint.PrettyPrinter(indent=2)
# %%
# retrieve data from wikipedia
# subject date
DATE_PARAM = '2024-11-15'

date = datetime.datetime.strptime(DATE_PARAM, "%Y-%m-%d")

# wikipedia API URL formation
url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{date.strftime('%Y/%m/%d')}"
print(f"Requesting REST API URL: {url}")

# Getting response from Wikimedia API
wiki_server_response = requests.get(url, headers={"User-Agent": "curl/7.68.0"})
wiki_response_status = wiki_server_response.status_code
wiki_response_body = wiki_server_response.text

print(f"Wikipedia REST API Response body: {wiki_response_body}")
print(f"Wikipedia REST API Response Code: {wiki_response_status}")

# Check if response status is not OK
if wiki_response_status != 200:
    print(
        f"❌ Received non-OK status code from Wiki Server: {wiki_response_status}. Response body: {wiki_response_body}"
    )
else:
    print(f"✅ Successfully retrieved Wikipedia data, content-length: {len(wiki_response_body)}")

# %%
# set up local directory structure
current_directory = Path(__file__).parent
RAW_LOCATION_BASE = current_directory / "data" / "raw-views"
RAW_LOCATION_BASE.mkdir(exist_ok=True, parents=True)
print(f"Created directory {RAW_LOCATION_BASE}")