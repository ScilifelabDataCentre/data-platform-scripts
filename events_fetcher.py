## Fetching all upcoming events from scilifelab website
## and outputed in JSON format that can be used as base
## to update the data_platform_events blob

import html
import json
import requests
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

def get_event_type(event):
    type = event.get("categories")
    if len(type) > 1:
        print("WARN: Event '{}' has multiple categories, double check the 'type' in output JSON\nEvent URL: {}".format(
            event["title"], event["url"]
        ))
    return type[0].get("name", "") if type else ""

def get_event_venue(event):
    venue = event.get("venue", {})
    if venue:
        venue = html.unescape(venue.get("venue", ""))
        if venue.lower().startswith("online") or (not venue and event.get("is_virtual")):
            venue = "Online"
    else:
        venue = ""
    return venue

def get_event_location(event):
    location = []
    venue = event.get("venue", {})
    if venue:
        city = html.unescape(venue.get("city", ""))
        if city:
            location.append(city)
    if event.get("is_virtual"):
        location.append("Online")
    return location

def get_event_organisers(event):
    organizer = event.get("organizer")
    if len(organizer) > 1:
        print("WARN: Event '{}' has mutliple organisers, double check the 'type' in output JSON\nEvent URL: {}".format(
            event["title"], event["url"]
        ))
    return organizer[0].get("organizer", "") if organizer else ""

dc_events_request = validate_request("https://blobserver.dc.scilifelab.se/blob/data_platform_events.json", "DC")
dc_events = dc_events_request.json().get("items", [])
dc_events_upcoming = [event["event_url"] for event in dc_events if date_not_past_today(event["date_start"])]

sll_events_formatted = []
sll_events_url = "https://www.scilifelab.se/wp-json/tribe/events/v1/events"
sll_events_request = validate_request(sll_events_url, "SciLifeLab")
page_num, sll_events_total_pages = (1, int(sll_events_request.headers["X-TEC-TotalPages"]))
while page_num <= sll_events_total_pages:
    if page_num > 1:
        sll_events_url = "{}?page={}".format(sll_events_url, str(page_num))
        sll_events_request = validate_request(sll_events_url, "Scilifelab")
    sll_events = sll_events_request.json().get("events", [])
    for event in sll_events:
        if get_event_type(event) == "Community" or event["url"] in dc_events_upcoming:
            continue
        start_date, start_time = event["start_date"].split(" ")
        end_date, end_time = event["end_date"].split(" ")
        event_info = {
            "title": event["title"],
            "type": get_event_type(event),
            "date_start": start_date,
            "time_start": start_time[:5],
            "date_end": end_date,
            "time_end": end_time[:5],
            "venue": get_event_venue(event),
            "location": get_event_location(event),
            "category": [],
            "organisers": get_event_organisers(event),
            "event_url": event["url"],
            "description": ""
        }
        sll_events_formatted.append(event_info)
    page_num += 1

if len(sll_events_formatted) == 0:
    print(
        "There are no new events to add, all upcoming events in scilifelab are already in DC platform"
    )
else:
    print(json.dumps(sll_events_formatted, indent=4, ensure_ascii=False))
