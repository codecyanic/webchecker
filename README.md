# WebChecker

WebChecker is a website activity monitor.

It checks HTTP response time, HTTP status code, checks the returned page
contents for a regular expression pattern and sends the data to Kafka.
It can be used in conjunction with WebChecker-pg to store the data in a
PostgreSQL database.

## Setup

Create a configuration file named `config.yaml` by customizing
`example.config.yaml`.

Install package requirements by running:
```
pip install -r requirements.txt
```

Installing is currently not supported.

## Running

Run from the project directory by using the command:
```
./main.py
```

## Testing

For unit testing run:
```
python3 -m pytest
```

## Usage

In the configuration file you can set multiple URLs for checking.
Setting the same URL more than once is not supported.

Optionally you can set `pattern` and `interval` parameters using the formats
expressed in the example configuration file:

 - `pattern` is used for checking raw HTML response body and uses
   [Python regular expression syntax](https://docs.python.org/3/library/re.html#regular-expression-syntax)
 - `interval` is the number of seconds between checks

The URLs will be checked in regular intervals,
but the time of the check is not user controllable.
This ensures that checks are evenly distributed in case multiple pages on the
same site are checked, but also that checks are on schedule even if the service
is restarted.

A WebChecker instance can only use one Kafka topic.
Although using multiple instances is supported, using the same URL in two
instances should be avoided, and is not supported when using WebChecker-pg.

When doing a check, WebChecker follows redirects, therefore under normal
circumstances redirect codes will not be collected.

WebChecker has built-in protection against Regular expression Denial of Service
(ReDoS) attacks, but this means that in some cases search results will not get
collected.

### Single check mode

By default WebChecker will run in service mode.

To use external scheduling or for one-off checks it can be run in single check
mode by providing the URL as a command line parameter:
```
./main.py URL [PATTERN]
```
