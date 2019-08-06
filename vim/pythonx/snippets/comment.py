#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# @author   Solomon Ng <solomon.wzs@gmail.com>
# @date     2018-10-10
# @version  1.0
# @license  MIT

from snippets.common import strtoday
import re

c_style_comment_symbol = {
    'left': '//',
    'right': '',
    'start': '/*',
    'end': '*/',
}

sh_style_comment_symbol = {
    'left': '#',
    'right': '',
}

xml_style_comment_symbol = {
    'left': '<!--',
    'right': '-->',
}

lang_symbol_info = {
    'c': {'comment': c_style_comment_symbol},
    'cpp': {'comment': c_style_comment_symbol},
    'go': {'comment': c_style_comment_symbol},
    'rust': {'comment': c_style_comment_symbol},
    'java': {'comment': c_style_comment_symbol},
    'javascript': {'comment': c_style_comment_symbol},
    'erlang': {
        'comment': {
            'left': '%%',
            'right': '',
        }
    },
    'lua': {
        'exec': '#!/usr/bin/lua',
        'comment': {
            'left': '--',
            'right': '',
        }
    },
    'scheme': {
        'comment': {
            'left': ';',
            'right': '',
        }
    },
    'vim': {
        'comment': {
            'left': '"',
            'right': '',
        }
    },
    'python': {'exec': '#!/usr/bin/python3'},
    'ruby': {'exec': '#!/usr/bin/ruby'},
    'sh': {'exec': '#!/usr/bin/bash'},
    'awk': {'exec': '#!/usr/bin/awk -f'},
}


def exec_comment(filetype):
    return lang_symbol_info.get(filetype, {}).get('exec', '#!')


def get_line_comment_symbol(filetype):
    comment = lang_symbol_info.get(filetype, {}).get(
        'comment', sh_style_comment_symbol)
    return comment.get('left', ''), comment.get('right', '')


def header_comment(snip):
    START, END = get_line_comment_symbol(snip.ft)
    now = strtoday()
    return f"""{START} @author     Solomon Ng <solomon.wzs@gmail.com>{END}
{START} @version    1.0{END}
{START} @date       {now}{END}
{START} @license    MIT{END}"""


def vi_set_filetype(snip):
    lines = snip.v.text.split('\n')[:-1]
    if len(lines) != 1:
        return snip.v.text

    filetype = lines[0].strip()
    START, END = get_line_comment_symbol(snip.ft)
    return f'{START} vi: set filetype={filetype} :{END}'


def encode_bytes_str(snip, enc):
    bs = snip.v.text.encode(enc)
    s = ''
    for byte in bs:
        s += "\\x%02x" % byte
    return s


def comment_line(snip):
    START, END = get_line_comment_symbol(snip.ft)

    lines = snip.v.text.split('\n')[:-1]
    first_line = lines[0]
    spaces = ''
    initial_indent = snip._initial_indent

    # Get the first non-empty line
    for idx, l in enumerate(lines):
        if l.strip() != '':
            first_line = lines[idx]
            sp = re.findall(r'^\s+', first_line)
            if len(sp):
                spaces = sp[0]
            break

    # Uncomment
    if first_line.strip().startswith(START):
        result = [line.replace(START, "", 1).replace(END, "", 1)
                  if line.strip() else line for line in lines]
    else:
        result = [f'{spaces}{START}{line[len(spaces):]}{END}'
                  if line.strip() else line for line in lines]

    # Remove initial indent
    if result[0] and initial_indent:
        result[0] = result[0].replace(initial_indent, '', 1)

    if result:
        return '\n'.join(result)
    else:
        return ''


def comment_block(snip, START, END):
    text = snip.v.text
    lines = text.split('\n')[:-1]
    first_line = lines[0]
    initial_indent = snip._initial_indent
    spaces = ''

    # Get the first non-empty line
    for idx, l in enumerate(lines):
        if l.strip() != '':
            first_line = lines[idx]
            sp = re.findall(r'^\s+', first_line)
            if len(sp):
                spaces = sp[0]
            break

    if text.strip().startswith(START):
        result = text.replace(START, '', 1).replace(END, '', 1)
    else:
        result = text.replace(spaces, spaces + START, 1).rstrip('\n') + END
        + '\n'

    if initial_indent:
        result = result.replace(initial_indent, '', 1)

    return result