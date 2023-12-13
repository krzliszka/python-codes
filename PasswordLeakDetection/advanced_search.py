#!/usr/bin/env python3


import fnmatch
import os
import yaml

import core

from termcolor import colored

RULES = yaml.safe_load(open("rules.yaml"))
FILETYPE = RULES['filetype']
FILETYPE_WEIGHT = RULES['filetype_weight']
GREP_WORDS = RULES['grep_words']
GREP_WORD_OCCURRENCE = RULES['grep_word_occurrence']
GREP_WORDS_WEIGHT = RULES['grep_words_weight']


class AdvancedSearch(object):
    def __init__(self):
        self._filetype = FILETYPE
        self._filetype_weight = FILETYPE_WEIGHT
        self._grep_words = GREP_WORDS
        self._grep_word_occurrence = GREP_WORD_OCCURRENCE
        self._grep_words_weight = GREP_WORDS_WEIGHT
        self._occurrence_counter = 0
        self._final_weight = 0
        self._exist = True

    def grepper(self, word):
        for search_expression in self._grep_words:
            if fnmatch.fnmatch(word, search_expression):
                self._occurrence_counter += 1

        if self._occurrence_counter >= self._grep_word_occurrence:
            self._final_weight += self._grep_words_weight

    def filetype_check(self, _file):
        file_name, extension = os.path.splitext(_file)
        for ext in self._filetype:
            if fnmatch.fnmatch(extension, ext):
                self._final_weight += self._filetype_weight

    def final(self, _file):
        if self._final_weight >= 10:
            print(colored('Interesting file has been found', 'cyan'))
            print(colored("The rule defined in 'rules.yaml' file has been triggerred. Check this file " + _file, 'cyan'))
            core.logger.info("The rule defined in 'rules.yaml' file has been triggerred while analyzing file " + _file)
            return True
        else:
            return False

