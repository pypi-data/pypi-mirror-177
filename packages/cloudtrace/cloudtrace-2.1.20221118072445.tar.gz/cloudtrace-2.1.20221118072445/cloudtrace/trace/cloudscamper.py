import os
import random
import subprocess
import tempfile
import time
import urllib.request
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import date

from file2 import fopen

from cloudtrace.trace.cloudinfo import get_cloud_info
from cloudtrace.trace.shuffle import shuf
from cloudtrace.trace.fasttrace import remote_notify
from cloudtrace.version import __version__

def new_filename(default_output, pps, ext, gzip=False, bzip2=False, hostname=None):
    if hostname is None:
        hostname = get_cloud_info()
    dirname, basename = os.path.split(default_output)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    if basename:
        basename += '.'
    timestamp = int(time.time())
    dt = date.fromtimestamp(timestamp)
    datestr = dt.strftime('%Y%m%d')
    filename = os.path.join(dirname, f'{basename}{hostname}.{datestr}.{timestamp}.{pps}.{ext}')
    if gzip:
        filename += '.gz'
    elif bzip2:
        filename += '.bz2'
    return filename

def print_duration(start, end):
    secs = end - start
    mins = secs / 60
    hours = mins / 60
    print(f'Duration: {hours:,.2f} h {mins:,.2f} m {secs:,.2f} s')

def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--input')
    group.add_argument('-i', '--addr', nargs='*')
    parser.add_argument('-p', '--pps', default=5000, type=int, help='Packets per second.')
    parser.add_argument('-o', '--default-output', required=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-z', '--gzip', action='store_true')
    group.add_argument('-b', '--bzip2', action='store_true')
    parser.add_argument('--remote')
    parser.add_argument('--cycles', type=int, default=1)
    parser.add_argument('--random', action='store_true')
    parser.add_argument('--shuffle', action='store_true')
    parser.add_argument('-O', '--extension', choices=['warts', 'json'], default='json')
    subparsers = parser.add_subparsers()
    tparser = subparsers.add_parser('trace')
    tparser.set_defaults(cmd='trace')
    pparser = subparsers.add_parser('ping')
    pparser.set_defaults(cmd='ping')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    args, remaining = parser.parse_known_args()

    hostname = get_cloud_info()
    addr = urllib.request.urlopen('https://api.ipify.org/').read().decode('utf8')

    sccmd = args.cmd + ' ' + ' '.join(remaining)

    cycle = 0
    while args.cycles == 0 or cycle < args.cycles:
        infile = args.input
        if args.shuffle:
            shuf(infile, inplace=True)
        f = tempfile.NamedTemporaryFile(mode='wt', delete=False)
        tmp = f.name
        try:
            if args.input:
                with fopen(infile, 'rt') as g:
                    for line in g:
                        if args.random:
                            addr, _, _ = line.rpartition('.')
                            addr = f'{addr}.{random.randint(0, 255)}'
                        else:
                            addr = line.strip()
                        f.write(f'{addr}\n')
            else:
                f.writelines(f'{addr}\n' for addr in args.addr)
            f.close()

            ftype = args.extension
            filename = new_filename(args.default_output, args.pps, ftype, gzip=args.gzip, bzip2=args.bzip2, hostname=hostname)
            if args.gzip:
                write = f'| gzip > {filename}'
            elif args.bzip2:
                write = f'| bzip2 > {filename}'
            else:
                write = f'-o {filename}'
            cmd = f'sudo scamper -O {ftype} -p {args.pps} -l {addr} -M {hostname} -c "{sccmd}" -f {tmp} {write}'
            print(cmd)
            start = time.time()
            subprocess.run(cmd, shell=True, check=False)
            end = time.time()
            print_duration(start, end)
            if args.remote:
                dirname, basename = os.path.split(args.default_output)
                pattern = os.path.join(dirname, f'{basename}.warts*')
                remote_notify(pattern, args.remote)
            try:
                cycle += 1
            except OverflowError:
                cycle = 1
        finally:
            os.unlink(tmp)
