#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# @author   Solomon Ng <solomon.wzs@gmail.com>
# @date     2019-04-03
# @version  1.0
# @license  MIT

import argparse
import ctypes
import json
import requests
import sys
import urllib


def RL(a: int, b: str):
    t = "a"
    Yb = "+"
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]
        d = ord(d) - 87 if d >= t else int(d)
        if b[c + 1] == Yb:
            d = ctypes.c_uint32(a).value >> d
        else:
            d = ctypes.c_int32(a << (d & 0x1f)).value
        a = a + d & 0xffffffff if b[c] == Yb else a ^ d
    return a


def TL(a: str):
    b = 406644
    b1 = 3293161072
    jd = "."
    _b = "+-a^+6"
    Zb = "+-3^+b+-f"

    e = []
    g = 0
    while g < len(a):
        m = ord(a[g])
        if 128 > m:
            e.append(m)
        else:
            if 2048 > m:
                e.append(m >> 6 | 192)
            else:
                if 55296 == (m & 64512) and g + 1 < len(a) and 56320 == (ord(a[g + 1]) & 64512):
                    g += 1
                    m = 65536 + ctypes.c_int32((m & 1023) << 10).value \
                        + (ord(a[g]) & 1023)
                    e.append(m >> 18 | 240)
                    e.append(m >> 12 & 63 | 128)
                else:
                    e.append(m >> 12 | 224)
            e.append(m >> 6 & 63 | 128)
        g += 1

    a = b
    for f in e:
        a += f
        a = RL(a, _b)
    a = RL(a, Zb)
    a ^= b1 or 0
    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a %= 1000000
    return f"{a}{jd}{a ^ b}"


def parse_response(res):
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        return f"Error: {res.status_code}"


def translate_with_tk(text: str, tl="zh-CN"):
    url = "https://translate.google.cn/translate_a/single"
    params = [
        ("client", "t"),
        ("s1", "auto"),
        ("t1", tl),
        ("h1", "en"),
        ("dt", "at"),
        ("dt", "bd"),
        ("dt", "ex"),
        ("dt", "ld"),
        ("dt", "md"),
        ("dt", "qca"),
        ("dt", "rw"),
        ("dt", "rm"),
        ("dt", "ss"),
        ("dt", "t"),
        ("ie", "UTF-8"),
        ("oe", "UTF-8"),
        ("otf", 1),
        ("pc", 1),
        ("ssel", 0),
        ("tsel", 0),
        ("kc", 2),
        ("tk", TL(text)),
        ("q", text),
    ]
    res = requests.get(url, params=params)
    return parse_response(res)


def translate(text: str, tl="zh-CN"):
    url = "https://translate.googleapis.com/translate_a/single"
    params = [
        ("client", "gtx"),
        ("sl", "auto"),
        ("tl", tl),
        ("dt", "t"),
        ("dt", "bd"),
        ("dj", 1),
        ("q", text),
    ]
    res = requests.get(url, params=params)
    return parse_response(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="call google translate api")
    parser.add_argument("text", type=str, help="text")
    parser.add_argument("-t", "--tl", type=str, default="zh-CN",
                        help="target language")
    args = parser.parse_args()

    text = urllib.parse.unquote_plus(args.text)
    res = translate(text)
    if isinstance(res, str):
        sys.stderr.write(res)
        sys.exit(1)

    lines = []
    for i in res.get("dict", []):
        pos = i.get("pos", "")
        term = ','.join(i.get("terms", []))
        lines.append(f"{pos}: {term}")
    sys.stdout.write('; '.join(lines))
    sys.exit(0)
