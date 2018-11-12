#!/usr/bin/env python3

"""
Decode mail subjects from non-plaintext encoding as per RFC 2047.
$ decode_mail "=?utf-8?B?data..."
$ echo "=?utf-8?B?data..." | mail-decode.py

Designed to be smart: you can invoke
$ decode_mail "=?utf-8?B?UkU6I..." "=?utf-8?Q?blah =?ISO-8859-1?B?..."  # two blocks in that second parameter
and the stdin equivalent.
It can handle if you mix more than one block of text in one parameter/line.
"""

import re, sys, collections.abc
from base64 import b64decode
from typing import Iterable
import quopri

# parsing the value in https://www.ietf.org/rfc/rfc2047.txt section "8. Examples"
# (ie: not 'Subject: =?ISO-8859...' but just '=?ISO-8859-1?B?SWYge...')
pattern = re.compile(r'=\?([^\?]*)\?([^\?].*)\?([^\?].*)\?=')

def flatten(items: Iterable) -> Iterable:
    """ Flatten arbitrarily-nested lists.
    Source: https://stackoverflow.com/a/40857703/2209946
    >>> list(flatten(['a', ['b', 'c'], [['d', 'e'], ['f', 'g']]]))
    ['a', 'b', 'c', 'd', 'e', 'f', 'g']"""
    for x in items:
        if isinstance(x, collections.abc.Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x

def parse_blocks(blocks: Iterable[str]) -> Iterable[str]:
    """ For each block, decode it and offer to translate it. """
    for block in blocks:
        yield parse_block(block)

def parse_block(block: str) -> str:
    try:
        match = pattern.search(block)
        charset, encoding, raw_text = match.groups()
    except AttributeError:
        # match is None so .groups fails
        raise ValueError(f"Could not recognise format of: {block}") from None

    if str.lower(encoding) == 'b':
        text = b64decode(raw_text)
    elif str.lower(encoding) == 'q':
        text = quopri.decodestring(raw_text)
    else:
        raise ValueError(f"Unknown encoding '{encoding}'") from None
        exit(1)

    decoded = text.decode(charset)
    return decoded

if __name__ == '__main__':
    # If arguments are provided, parse them. Otherwise read from stdin.
    if len(sys.argv) > 1:
        blocks = list(flatten(a.split() for a in sys.argv[1:]))
    else:
        blocks = list(flatten(sys.stdin.read().split()))

    result = ''.join(parse_blocks(blocks))
    print(result)

    if not blocks:  # gracefully handle an immediate EOF (don't offer to translate it)
        exit(1)
    try:
        if str.lower(input("Translate? [y/n] ")) == 'y':
            from googletrans import Translator
            t = Translator()
            print(t.translate(result))
    except EOFError:
        pass # take it as a "no"
