#!/usr/bin/env python
#coding=utf-8

from .ply_sh import parser

import sys
from subprocess import call
import os
import re

oldline = ''
regexpr = '#\s+(.+)\s+->\s*(.+)'

cmd_block = {}

def parse_filenames(s):
    statement = parser.parse(s)
    return ','.join(statement['cmd'])
        
with open(sys.argv[1]) as fid:
    for line in fid:
        if len(line)<2:
            continue
        if line[0]=='#':
            m = re.match(regexpr, line)
            if m:
                inputs, outputs = m.groups()
                inputs = map(parse_filenames, inputs.split(','))
                outputs = map(parse_filenames, outputs.split(','))
                cmd_block = {'inputs' : inputs,
                             'outputs' : outputs}
        else:
            if cmd_block:
                inputs = cmd_block['inputs']
                outputs = cmd_block['outputs']
                inputs_modification = [os.path.getmtime(inp) for inp in inputs]
                need_to_run=False
                for out in outputs:
                    try:
                        mtime = os.path.getmtime(out)
                        for inp in inputs_modification:
                            if mtime < inp:
                                need_to_run=True
                    except OSError:
                        need_to_run=True
            else:
                need_to_run = True
            if not need_to_run:
                continue
                
            oldline += line
            if oldline[-2]=='\\':
                oldline = oldline[:-2] + ' '
                continue
            print oldline
            statement = parser.parse(oldline)
            cmd = statement['cmd']
            env = os.environ.copy()
            env.update(statement['env'])
            print(cmd)
            if cmd:
                call(cmd, env=env)
            oldline = ''
