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
        inputs = re.findall('[^ ,]+', inputs)
        outputs = re.findall('[^ ,]+', outputs)
        return inputs, outputs
    else:
        raise NotARule('not a rule')

def make_if_statement(inputs, outputs):
    conditions = []
    filedefs = 'INPUTFILES=`echo {}`\n'.format(" ".join(inputs))
    filedefs += 'OUTPUTFILES=`echo {}`\n'.format(" ".join(outputs))
    inputs_exist = 'for file in $INPUTFILES; do [ ! -e "$file" ] && echo "Input file $file does not exist" >&2 && exit 1; done\n'

    conditions = """
    runblock=0
    for inp in $INPUTFILES
    do
        for out in $OUTPUTFILES
        do
            if [ "$inp" -nt "$out" ]
            then
                runblock=1
            fi
        done
    done
    """
    if_stmt = 'if [ "$runblock" -eq 1 ]\nthen\n'

    return filedefs + inputs_exist + conditions + if_stmt


def run_shell():
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
                    outp_line = make_if_statement(inputs, outputs)
                    open_statement = True
                    outp_line += 'echo "Running rule: {}"\n'.format(line[1:])
                except NotARule:
                    outp_line = line
            else:
                outp_line = line
            generated_scripts.write(outp_line) 

    if open_statement:
        generated_scripts.write('fi\n')
        open_statement = False
    generated_scripts.flush()

    subprocess.call(['/bin/bash', generated_scripts.name])

    generated_scripts.close()

if __name__ == '__main__':
    run_shell()
