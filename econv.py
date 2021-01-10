# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 13:08:40 2020

@author: solis

It changes the encoding of a file; command line version
"""
import argparse

from chardet.universaldetector import UniversalDetector


def __detect_encode(file):
    detector = UniversalDetector()
    detector.reset()
    with open(file, 'rb') as f:
        for row in f:
            detector.feed(row)
            if detector.done: break
    detector.close()
    return detector.result


def econv(fsource: str, ftarget: str = None,
          target_encoding: str='utf-8') -> None:
    """
    changes the file encoding
    args:
        fsource: file source
        ftarget (optional): fsource with the new encoding
        target_encoding: target encoding of the new file
    """
    from os.path import splitext
    BLOCKSIZE = 1024*1024
    source_encoding = __detect_encode(fsource)
    print('encoding source file: ', source_encoding)
    if ftarget is not None:
        if fsource == ftarget:
            print('file source and file target can not have the some name')
            return
    else:
        fname, fextension = splitext(fsource)
        ftarget = f'{fname}_{target_encoding}{fextension}'
    with open(fsource, 'rb') as inf:
      with open(ftarget, 'wb') as ouf:
        while True:
          data = inf.read(BLOCKSIZE)
          if not data:
              break
          converted = \
              data.decode(source_encoding['encoding']).encode(target_encoding)
          ouf.write(converted)


def main():

    try:
        from time import time
        import traceback

        startTime = time()

        my_parser = \
            argparse.ArgumentParser(prog='ecnov',
                                    usage='%(prog)s [options] file',
                                    description=\
                                        'Changes the encoding of a file; type -h for help',
                                    allow_abbrev=False)

        my_parser.add_argument('File',
                               type=str, help='The file name you want to ' +\
                                   'change its encoding to a new ' +\
                                   'encoding')

        my_parser.add_argument('-ft', '--file_target',
                               default=None,
                               type=str,
                               help='New file name encoded with' +\
                                   ' the new encoding; if you' +\
                                   ' do not provide a new name it will' +\
                                   ' be named with a new one; the' +\
                                   ' source file will not be overwritten')

        my_parser.add_argument('-te', '--target_encoding',
                               default='utf-8',
                               type=str,
                               help='The new encoding')

        args = my_parser.parse_args()
        fsource = args.File
        ftarget = args.file_target
        target_encoding = args.target_encoding

        econv(fsource, ftarget, target_encoding)

        xtime = time() - startTime
        print(f'El script tardó {xtime:0.1f} s')

    except Exception:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
