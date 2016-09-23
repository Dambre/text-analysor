'''
readers.py is intended for describing different filetype readers
'''


class BaseReader(object):
    def __init__(self, file):
        self.file = file

    def read(self):
        raise NotImplementedError


class TxtReader(BaseReader):
    def __init__(self, file):
        super().__init__(file)

    def read(self):
        return open(self.file).read().lower()


def get_reader(filetype):
    if filetype == '.txt':
        return TxtReader
    return BaseReader