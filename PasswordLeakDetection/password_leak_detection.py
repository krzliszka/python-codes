#!/usr/bin/env python3

import argparse
import os
import sys

import colorama
from termcolor import colored

import advanced_search
import core

colorama.init()


class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


def opening():
    title = """
        PASSWORD LEAK DETECTION
    """

    print(colored(title, 'magenta'))
    print()
    print()


if __name__ == '__main__':

    opening()
    parser = argparse.ArgumentParser(formatter_class=SmartFormatter)
    pass
