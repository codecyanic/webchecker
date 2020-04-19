#!/usr/bin/env python3

import logging
import time
from binascii import crc32
from sched import scheduler

import requests

from regex import safe_search

logger = logging.getLogger(__name__)


def search_pattern(pattern, text):
    if not isinstance(pattern, str):
        raise TypeError('pattern must be a string')

    result = {'pattern': pattern}
    try:
        result['found'] = safe_search(pattern, text, .1)
    except Exception as e:
        result['exception'] = e

    return result


def check_website(url, pattern=''):
    if not isinstance(url, str):
        raise TypeError('url must be a string')

    logging.debug('Checking: {}'.format(url))

    result = {'url': url}

    start_time = time.monotonic()
    try:
        r = requests.get(url, timeout=30)
    except Exception as e:
        result['exception'] = e
        return result

    time_ms = round((time.monotonic() - start_time) * 1000)
    result['response'] = {
        'time': time_ms,
        'code': r.status_code,
    }

    if pattern:
        search = search_pattern(pattern, r.text)
        result['response']['search'] = search
        if 'exception' in search:
            result['exception'] = search.pop('exception')

    return result


class WebsiteChecker():
    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic
        self.scheduler = scheduler()
        self.schedule = {}

    def check(self, url, pattern, interval):
        args = (url, pattern, interval)
        at = self.abstime(url, interval)
        self.scheduler.enterabs(at, 0, self.check, args)

        data = None
        try:
            data = check_website(url, pattern)
            if 'exception' in data:
                raise data.pop('exception')
        except Exception as e:
            logger.exception(e)

        if data:
            try:
                self.producer.send(self.topic, data)
            except Exception as e:
                logger.exception(e)

    def add(self, url, pattern='', interval=3600):
        logger.debug('Add URL: {}'.format(url))
        if url in self.schedule:
            self.remove(url)

        at = self.abstime(url, interval)
        args = (url, pattern, interval)
        event = self.scheduler.enterabs(at, 0, self.check, args)
        self.schedule[url] = event

    def remove(self, url):
        event = self.schedule.pop(url)
        self.scheduler.cancel(event)

    def run(self, *args, **kwargs):
        return self.scheduler.run(*args, **kwargs)

    def abstime(self, key, interval):
        # Get offset for key
        crc = crc32(bytes(key, 'utf-8'))
        offset = crc % interval

        # Calculate time until next occurrence
        until_next = offset - time.time() % interval
        if until_next < 0:
            until_next += interval

        # Return as monotonic
        return until_next + time.monotonic()
