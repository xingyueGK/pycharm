#-*- coding:utf-8 -*-
import os
import json
import sys
import logging
import tempfile
import subprocess

ISATTY = sys.stdout.isatty()

def make_color(code):
    def color_func(s):
        # if not ISATTY:
        #     return s
        tpl = '\x1b[{}m{}\x1b[0m'
        return tpl.format(code, s)
    return color_func


red = make_color(31)
green = make_color(32)
yellow = make_color(33)
blue = make_color(34)
magenta = make_color(35)
cyan = make_color(36)

bold = make_color(1)
underline = make_color(4)

grayscale = {(i - 232): make_color('38;5;' + str(i)) for i in xrange(232, 256)}

#grayscale[14]()
print yellow('Error: {} is not allowed in extra curl args')