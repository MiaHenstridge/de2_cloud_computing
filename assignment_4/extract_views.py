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
DATE_PARAM = '2024-11-18'

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
# %%
# save the contents of `wiki_response_body` to file called `raw-views-YYYY-MM-DD.txt`
# in variable `RAW_LOCATION_BASE`.
# i.e: `data/raw-views/raw-views-2024-10-01.txt`.
# Store the path to the file in the variable `raw_views_file`.

raw_views_file = (
    RAW_LOCATION_BASE / f"raw-views-{date.strftime('%Y-%m-%d')}.txt"
)

with open(raw_views_file, 'w', encoding='utf-8') as file:
    file.write(wiki_response_body)

# print(wiki_response_body)
# %%
# create a new bucket for your wikipedia pipeline
S3_WIKI_BUCKET = "mainong-wikidata-assignment4"
# Create a new bucket for your wikipedia pipeline
# > Choose a name ending with "-wikidata"
# > Store the bucket name in the variable S3_WIKI_BUCKET
# > Create the bucket if it does not exist
s3 = boto3.client("s3", region_name="eu-west-1")

# YOUR SOLUTION COMES HERE =========================
# create a new S3 bucket with the name stored in S3_WIKI_BUCKET
default_region = "eu-west-1"

try:
    bucket_configuration = {"LocationConstraint": default_region}
    response = s3.create_bucket(Bucket=S3_WIKI_BUCKET, CreateBucketConfiguration=bucket_configuration)

    print("\n AWS Resonse:")
    pp.print(response)
except Exception as e:
    print(f"Error creating bucket: {str(e)}")
# %%
# upload the file you created to S3
s3_key = f"datalake/raw/raw-view-{date.strftime('%Y-%m-%d')}.txt"

# upload file to S3 bucket
try:
    s3.upload_file(raw_views_file, S3_WIKI_BUCKET, s3_key)
    print("Upload successful!")
except Exception as e:
    print(f"Error uploading file: {str(e)}")

print(f"Uploaded raw edits to s3://{S3_WIKI_BUCKET}/{s3_key}")
# %%
# process and transform the data
wiki_response_parsed = wiki_server_response.json()
top_views = wiki_response_parsed["items"][0]["articles"]

# print(top_views)
current_time = datetime.datetime.now(datetime.timezone.utc)
json_lines = ""

for page in top_views:
    record = {
        "article": page["article"],
        "views": page["views"],
        "rank": page["rank"],
        "retrieved_at": current_time.replace(
            tzinfo=None
        ).isoformat(),
    }
    json_lines += json.dumps(record) + "\n"

JSON_LOCATION_DIR = current_directory / "data" / "views"
JSON_LOCATION_DIR.mkdir(exist_ok=True, parents=True)
print(f"Created directory {JSON_LOCATION_DIR}")
print(f"JSON lines:\n{json_lines}")

# %%
# save and upload processed data
json_lines_filename = f"views-{date.strftime('%Y-%m-%d')}.json"
json_lines_file = JSON_LOCATION_DIR / json_lines_filename

with json_lines_file.open('w') as file:
    file.write(json_lines)

s3.upload_file(json_lines_file, S3_WIKI_BUCKET, f"datalake/views/{json_lines_filename}")
print(f"Uploaded processed data to s3://{S3_WIKI_BUCKET}/datalake/views/{json_lines_filename}")
# %%
