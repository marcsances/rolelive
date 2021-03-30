#!/usr/bin/env python3

import logging
import os

from util.injector import Injector


def main():
    print("Rolelive started!")
    while True:
        pass


if __name__ == "__main__":
    if "ROLELIVE_DEBUG" in os.environ:
        logging.basicConfig(level=logging.DEBUG)
    Injector.bind_injector()
    main()
