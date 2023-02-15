# data-platform-scripts
This repository holds the scripts produced for the SciLifeLab Data Platform, that are not directly associated with visualisations or the underlying code used to generate the Platform itself.

#### ddls_jobs_fetcher.py

This script collects the DDLS jobs that are available in scilifelab [job lisitng](https://www.scilifelab.se/careers?filter=ddls) but not yet in the platform [jobs page](https://data.scilifelab.se/jobs/). The output is list of jobs in JSON format, that can be copy pasted (upon review) to the job's [data file](https://github.com/ScilifelabDataCentre/data.scilifelab.se/blob/develop/data/jobs.json) of the platform.

**Usage:**
```
python ddls_jobs_fetcher.py
```
