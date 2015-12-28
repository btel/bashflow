#!/usr/bin/env python
#coding=utf-8

import subprocess
import argparse
import tempfile
import sys
import re

class NotARule(Exception):
    pass

def parse_rule(line):
    regexpr = '#\s+(.+)\s+->\s*(.+)'
    m = re.match(regexpr, line)
    if m:
        inputs, outputs = m.groups()
        inputs = inputs.split(',')
        outputs = outputs.split(',')
        return inputs, outputs
    else:
        raise NotARule('not a rule')

def make_if_statement(inputs, outputs):
    conditions = []
    inputs_exist = ""
    for inp in inputs:
        inputs_exist += '[ ! -e {} ] && echo "Input file {} does not exist" >&2 && exit\n'.format(inp, inp)

    for outp in outputs:
        for inp in inputs:
            conditions.append('[ {} -nt {} ]'.format(inp, outp))
    if_stmt = "if {}\nthen\n".format(" | ".join(conditions))
    return inputs_exist + if_stmt





parser = argparse.ArgumentParser()
parser.add_argument('script')
args = parser.parse_args()

generated_scripts = tempfile.NamedTemporaryFile(mode='w',
        delete=False)

print(generated_scripts.name)
open_statement = False
with file(args.script) as fid:
    for line in fid:
        if line.startswith("#"):
            try:
                inputs, outputs = parse_rule(line)
                if open_statement:
                    generated_scripts.write('fi\n')
                    open_statement = False
                line = make_if_statement(inputs, outputs)
                open_statement = True
            except NotARule:
                pass
        generated_scripts.write(line) 

if open_statement:
    generated_scripts.write('fi\n')
    open_statement = False
generated_scripts.flush()

subprocess.call(['/bin/bash', generated_scripts.name])

generated_scripts.close()
