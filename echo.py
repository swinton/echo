#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json


def handler(event, context):
    # A simple function that just returns the event we were passed, along with
    # the current environment
    return dict(event=event, environment=dict(os.environ))


if __name__ == "__main__":
    # Read event, context from sys.argv
    args = [json.loads(arg) for arg in sys.argv[1:2]]

    # Provide None for event, context if not provided
    while len(args) < 2:
        args.append(None)

    # Print the output
    print handler(*args)
