#!/usr/bin/env python3

import json
import logging
import sys
import yaml

from kafka import KafkaProducer

import websitechecker
from websitechecker import WebsiteChecker, check_website

logger = logging.getLogger(__name__)


def json_serialize(obj):
    try:
        return json.dumps(obj).encode('ascii')
    except Exception as e:
        logger.exception(e)


def load_config():
    config_paths = [
        '/etc/webchecker/webchecker.yaml',
        'config.yaml',
    ]
    for path in config_paths:
        try:
            with open(path) as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            pass
        except Exception as e:
            logger.error(e)

    try:
        return config
    except UnboundLocalError:
        logger.critical('\nError while loading config file')
        exit(1)


def add_urls(checker, urls):
    for url, args in urls.items():
        if isinstance(args, dict):
            args['url'] = url
            checker.add(**args)
        elif isinstance(args, list):
            checker.add(url, *args)
        elif isinstance(args, str):
            checker.add(url, args)
        elif isinstance(args, (int, float)):
            checker.add(url, interval=args)
        elif args is None:
            checker.add(url)


if __name__ == '__main__':
    config = load_config()

    debug = config.get('debug')
    if debug:
        websitechecker.logger.addHandler(logging.StreamHandler())
        websitechecker.logger.setLevel(logging.DEBUG)

    single_check = False
    if len(sys.argv) > 1:
        single_check = sys.argv[1:3]

    if not single_check:
        print('Connecting to Kafka...')
    kafka = config.get('kafka', {})
    kafka['value_serializer'] = json_serialize
    topic = kafka.pop('topic', '')
    producer = KafkaProducer(**kafka)

    if single_check:
        result = check_website(*single_check)
        if 'exception' in result:
            logger.exception(result.pop('exception'))
        if debug:
            print(result)
        producer.send(topic, result)
        producer.flush()
        exit()

    print('Adding URLs...')
    checker = WebsiteChecker(producer, topic)
    urls = config.get('urls', {})
    add_urls(checker, urls)

    print('\nWebChecker service is running\n')
    checker.run()
