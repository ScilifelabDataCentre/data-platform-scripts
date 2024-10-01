## Fetching available new DDLS jobs listed in scilifelab website
## and create a new json file, where the content can be copy
## pasted (upon review) to data/jobs.json on the platform repo

import requests
import json
import sys

from datetime import datetime


def date_not_past_today(date_str):
    given_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    today_date = datetime.now().date()
    return given_date >= today_date


def validate_request(url, target):
    r = requests.get(url)
    if r.status_code != 200:
        sys.exit("Fetching jobs from {} failed, check the URL {}".format(url, target))
    return r


sll_jobs_url = (
    "https://www.scilifelab.se/wp-json/wp/v2/career?orderby=archive_date&per_page=50"
)
dc_jobs_url = "https://blobserver.dc.scilifelab.se/blob/data_platform_jobs.json"

# try and get jobs from scilifelab and data centre platform

sll_jobs_request = validate_request(sll_jobs_url, "Scilifelab")
dc_jobs_request = validate_request(dc_jobs_url, "DC")

dc_all_jobs = dc_jobs_request.json()
dc_open_jobs = []
for job in dc_all_jobs["items"]:
    if date_not_past_today(job["app_deadline"]):
        dc_open_jobs.append(job["job_url"])

page_num, sll_jobs_total_pages = (1, int(sll_jobs_request.headers["X-WP-TotalPages"]))
sll_new_open_jobs = []
while page_num <= sll_jobs_total_pages:
    if page_num > 1:
        sll_jobs_url = "{}&page={}".format(sll_jobs_url, str(page_num))
        sll_jobs_request = validate_request(sll_jobs_url, "Scilifelab")
    sll_all_jobs = sll_jobs_request.json()
    for job in sll_all_jobs:
        if date_not_past_today(job["archive_date"]):
            try:
                job_url = job["acf"]["read_more_external_link"]["url"]
            except:
                job_url = job["link"]
            if job_url not in dc_open_jobs:
                job_info = {
                    "title": job["title"]["rendered"],
                    "type": [],
                    "app_deadline": job["archive_date"],
                    "employer": job["acf"]["university"]["title"],
                    "job_url": job_url,
                    "description": "",
                }
                sll_new_open_jobs.append(job_info)
        else:
            break
    page_num += 1

if len(sll_new_open_jobs) == 0:
    print(
        "There are no new jobs to add, all open jobs in scilifelab are already in DC platform"
    )
else:
    print(json.dumps(sll_new_open_jobs, indent=4, ensure_ascii=False))
