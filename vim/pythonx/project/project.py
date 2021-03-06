#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# @author   Solomon Ng <solomon.wzs@gmail.com>
# @date     2018-10-10
# @version  1.0
# @license  MIT

import fnmatch
import os
from subprocess import PIPE
from subprocess import Popen


VIM_HOME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def find(pattern, path, n=0):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
                if n > 0 and len(result) == n:
                    return result
    return result


def get_makefile_variable(makefiles, var):
    var_mk = os.path.join(VIM_HOME, "other/makefile/variable.mk")
    cmd = ["make"]
    for f in makefiles:
        cmd += ["-f", f]
    cmd += ["-f", var_mk, "debug-var-%s" % var]
    p = Popen(" ".join(cmd), shell=True, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    if p.returncode != 0:
        return ""
    else:
        return output.decode("utf8")


def get_file_lines(filename):
    flags = []
    with open(filename, "r") as fd:
        line = fd.readline()
        while line:
            flags.append(line.strip())
            line = fd.readline()
    return flags
