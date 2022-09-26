# check_gitlab

Nagios plugin for doing a GitLab health check.

Copyright (c) 2022 Dennis Neufeld
Copyright (c) 2021 Hernán Collazo
Copyright (c) 2020 Kevin Krumbiegel

## Usage:

### In Nagios:
1. Download the check_gitlab.py file.
2. Mark the file as executable (i.e. using `sudo chmod +x ~/check_gitlab.py`)
3. Move the file to /usr/lib/nagios/plugins/ (i.e. using `mv ~/check_gitlab.py /usr/lib/nagios/plugins/check_gitlab.py`)

### Standalone:
1. Download the check_gitlab.py file.
2. Execute the file (Python 3 needs to be installed)

Usage:
```check_gitlab.py [-h] -s <server_url> [-t <access_token>] [--check-all] [--check-cache] [--check-db] [--check-gitaly] [--check-master] [--check-queues] [--check-rate-limiting] [--check-sessions] [--check-shared-state] [--check-trace-chunks]```

* General
  * `-s <server_url>`       = URL of the server to be checked. (i.e. https://gitlab.example.org/)
  * `-t <access_token>`     = Access token for Gitlab Health Checks. (visit https://gitlab.example.org/admin/health_check)
  * `-h`                    = This help screen
* Checks:
  * `--check-all`           = Enable all checks
  * `--check-cache`         = Enable checking cache status
  * `--check-db`            = Enable checking database status
  * `--check-gitaly`        = Enable checking gitaly status
  * `--check-master`        = Enable checking master status
  * `--check-queues`        = Enable checking queues status
  * `--check-rate-limiting` = Enable checking rate limiting status
  * `--check-sessions`      = Enable checking session status
  * `--check-shared-state`  = Enable checking shared state status
  * `--check-trace-chunks`  = Enable checking trace chunks status

## Background
The check_gitlab script queries the JSON-API endpoint of a GitLab server using the "Readiness" feature.
By now it checks whether the status of all specified modules is "ok".
In case the status is not okay, a cricital condition will be reported.
If an exception occurs or the check is executed with bad parameter configuration, an unknown condition will be reported.

## Further information

For further information see:
* [GitLab web page](https://about.gitlab.com/)
* [GitLab Health Check documentation](https://docs.gitlab.com/ee/user/admin_area/monitoring/health_check.html)
* [Original Project](https://github.com/KevinKrumbiegel/check_gitlab)
* [Previous Project Fork](https://github.com/hernancollazo/check_gitlab)
