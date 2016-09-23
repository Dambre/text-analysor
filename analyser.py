#!/usr/bin/python3

'''
This python program analyses given text files and returns some statistics
1. 10 Most frequent words
2. All unique words in all files
3. All unique words in specific file
'''

import argparse
import re
import sys
import os
import string
from collections import Counter

import nltk; nltk.data.path.append('nltk_data')

from readers import get_reader


PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
TEXT_FILES_PATH = PROJECT_PATH + '/text_files/'
FILES_LIST = [TEXT_FILES_PATH + file for file in os.listdir(TEXT_FILES_PATH)]
PARTS_TO_CLEAN = (
    ('_', ''),
    ('--', ' '),
)


class Analyser(object):
    '''
    Analyser object to analyse text
    '''
    def __init__(self, files):
        self._words = list()
        self._files_list = files
        self._errors = list()
        self._messages = list()

    @property
    def words(self):
        '''
        words property set by _get_words method
        '''
        return self._words 
    
    @property
    def errors(self):
        '''
        errors property for capturing errors
        '''
        return self._errors

    @property
    def messages(self):
        '''
        messages property for capturing output
        '''
        return self._messages

    @property
    def files_list(self):
        '''
        files_list property FILES_LIST
        '''
        return self._files_list

    def _read_text_from_file(self, file):
        '''
        read files using reader from readers.py
        '''
        filetype = os.path.splitext(file)[1]
        reader = get_reader(filetype)
        try:
            return reader(file).read()
        except NotImplementedError:
            self._errors.append('"{}" files are not supported..'.format(filetype))
            return ''

    def _clean_word_parts(self, text):
        '''
        clean signs from words. e.g:
            __
            --
        '''
        for part in PARTS_TO_CLEAN:
            text = text.replace(part[0], part[1])
        return text

    def _filter_words(self, words):
        '''
        Check if word have any letter 
        because filters leaves numbers , some signs
        '''
        filtered = list()
        for word in words:
            if re.search('[a-zA-Z]', word):
                filtered.append(word)
        return filtered

    def _get_cleaned_words(self, text):
        '''
        method intented to split and clean extracted text
        '''
        text = self._clean_word_parts(text)
        words = nltk.word_tokenize(text)
        return self._filter_words(words)

    def _extract_words(self, files):
        '''
        get text from files
        '''
        parsed_words = list()
        for file in files:
            text = self._read_text_from_file(file)
            parsed_words += self._get_cleaned_words(text)
        self._words = parsed_words

    def execute(self):
        pass

    def run(self):
        '''
        base run method - runs execute method, prints messages
        '''
        self.execute()
        for mes in self.messages:
            print(mes)
        for err in self.errors:
            print(err)
        sys.exit(2)


class TopWords(Analyser):
    '''
    TopWords object to get most frequent words
        limit=10 is the number of how many top words to return
    '''
    def __init__(self, files, limit=10):
        super().__init__(files)
        self.limit = limit
    
    @property
    def top_words(self):
        '''
        get top-x most frequent words 
        x = self.limit
        '''
        return Counter(self.words).most_common(self.limit)

    def execute(self):
        '''
        Execution rules
        '''
        self._extract_words(self.files_list)
        self._messages.append(self.top_words)


class Unique(Analyser):
    '''
    Unique object to get unique words
    '''
    def __init__(self, files):
        super().__init__(files)

    @property
    def unique_words(self):
        '''
        unique words from self.words
        '''
        return list(set(self.words)) 

    def execute(self):
        '''
        Execution rules
        '''
        self._extract_words(self.files_list)
        self._messages.append(self.unique_words)   


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--top', action='store_true',
        help='return 10 most frequent words with their occurrences')
    
    parser.add_argument('-u', '--unique', action='store_true',
        help='return unique words')

    _args = parser.parse_args()
    command = None
    if _args.top:
        command = TopWords(FILES_LIST)

    elif _args.unique:
        _files = FILES_LIST
        while True:
            counter = 0
            print('Select one option:\n{}) All files'.format(counter))
            for file in _files:
                counter += 1
                print('{}) {}'.format(counter, file))
            
            try:
                option = int(input())
            except ValueError:
                continue

            if option < 0:
                continue

            elif option == 0:
                break

            elif option > 0 and option <= counter:
                _files = [_files[option-1],]
                break

            elif option > counter:
                continue

        command = Unique(_files)


    if not command:
        print(parser.print_help())
        sys.exit(2)

    command.run()


if __name__ == '__main__':
    main()
