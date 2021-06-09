#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# @author   Solomon Ng <solomon.wzs@gmail.com>
# @date     2021-03-17
# @version  1.0
# @license  MIT

import re
import sys


def encode_str(text: str, enc: str):
    bs = text.encode(enc)
    s = ""
    for byte in bs:
        if 0 <= byte and byte <= 127:
            s += chr(byte)
        else:
            s += "\\x%02x" % byte
    sys.stdout.write(s)


def decode_str(text: str, enc: str):
    def _hex(matchobj):
        str_hex = matchobj.group(1)
        i = int(str_hex, base=16)
        return bytes([i])

    bs = re.sub(br"\\x([a-fA-F0-9]{2})", _hex, text.encode("utf8"))
    sys.stdout.write(bs.decode(enc))


def encode_quotation_str(text: str, enc: str):
    def _encode(matchobj) -> str:
        bs = matchobj.group(2).encode(enc)
        s = ""
        for byte in bs:
            s += "\\x%02x" % byte
        return matchobj.group(1) + s + matchobj.group(3)

    sys.stdout.write(re.sub("(['\"])(.*?)(['\"])", _encode, text))
