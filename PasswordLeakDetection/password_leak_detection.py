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
    basic = parser.add_argument_group('BASIC USAGE')
    configuration = parser.add_argument_group('CONFIGURATION')
    basic.add_argument('-p', dest='local_path', required=True, help="Path to the folder containing files to be analyzed")
    basic.add_argument('-r', '--remove', action='store_true', help="Files which don't contain any secret will be removed when this flag is set")
    basic.add_argument('-a', '--advance', action='store_true', help="All files will be additionally analyzed using rules specified in 'rules.yaml' file when this flag is set")
    basic.add_argument('-s', '--secret', action='store_true', help="All files will be additionally analyzed in search of hardcoded passwords when this flag is set")
    basic.add_argument('-o', dest='outfile', default='results.json', help="Output file in JSON format")

    configuration.add_argument('--min_key')