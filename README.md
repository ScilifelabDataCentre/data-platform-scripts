# data-platform-scripts
This repository holds the scripts produced for the SciLifeLab Data Platform, that are not directly associated with visualisations or the underlying code used to generate the Platform itself.

### ddls_jobs_fetcher.py

This script collects the jobs that are available in [SciLifeLab jobs page](https://www.scilifelab.se/careers?filter=ddls), but not yet on the corresponding platform [jobs page](https://data.scilifelab.se/jobs/). The output is list of jobs in JSON format that can be copy pasted (upon review) to the job's [data file](https://blobserver.dc.scilifelab.se/blob/data_platform_jobs.json/info) used for the platform.

**Usage:**

To print the out to stdout
```
python ddls_jobs_fetcher.py
```

To save the output in a file called `latest_ddls_jobs.json` on the current folder
```
python ddls_jobs_fetcher.py > latest_ddls_jobs.json
```

### events_fetcher.py

This script collects all upcoming events listed in the [SciLifeLab website](https://www.scilifelab.se/events), but not yet in the corresponding platform [events page](https://data.scilifelab.se/events/). The output is list of events in JSON format, that can be copy pasted (upon review) to the event's [data file](https://blobserver.dc.scilifelab.se/blob/data_platform_events.json/info), which is used to build the platform's events page.

**Usage:**

To print the out to stdout
```
python events_fetcher.py
```

To save the output in a file called `latest_events.json` on the current folder
```
python events_fetcher.py > latest_events.json
```
