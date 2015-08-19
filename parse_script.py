#!/usr/bin/env python
#coding=utf-8

from ply_sh import parser

import sys
from subprocess import call

with open(sys.argv[1]) as fid:
    for line in fid:
        if line:
            statement = parser.parse(line)
            cmd = statement['cmd']
            if cmd:
                call(cmd, env=statement['env'])
