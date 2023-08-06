import platform
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from multiprocessing import Pool

from pb_amarder.bar import Progress

from cloudtrace.read.convert import ConvertTrace

verbose = 0
fix = True

def pattern(infile, gzip=False, bzip2=False):
    if infile.endswith('.bz2'):
        outfile = infile[:-4]
    elif infile.endswith('.gz'):
        outfile = infile[:-3]
    else:
        outfile = infile
    outfile = '{}.jsonl'.format(outfile)
    if gzip:
        outfile += '.gz'
    elif bzip2:
        outfile += '.bz2'
    return outfile

def convert(infile, outfile):
    sidefile = (infile.rpartition('.')[0] if infile.endswith('.gz') or infile.endswith('.bz2') else infile) + '.sidecar'
    c = ConvertTrace(infile, outfile, sidefile)
    c.convert_trace(fix=fix, verbose=verbose)
    if verbose:
        print(c)

def convert_wrapper(args):
    infile, outfile = args
    convert(infile, outfile)

def main():
    global fix, verbose
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--raw', action='store_true')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-o', '--outfiles', nargs='+')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-z', '--gzip', action='store_true')
    group.add_argument('-b', '--bzip2', action='store_true')
    parser.add_argument('-p', '--processes', default=1, type=int)
    parser.add_argument('-i', '--infiles', nargs='+')
    parser.add_argument('-I', '--file')
    parser.add_argument('-H', '--hostname', default=platform.node())
    args = parser.parse_args()

    fix = not args.raw
    print('Fixing pcap file: {}'.format(fix))
    verbose = args.verbose

    infiles = args.infiles if args.infiles is not None else []
    if args.file:
        with open(args.file, 'rt') as f:
            for filename in f:
                infiles.append(filename.strip())

    if args.outfiles:
        if len(args.outfiles) != len(infiles):
            print('Outfiles must match number of infiles.')
            exit(1)
        outfiles = args.outfiles
    else:
        outfiles = []
        for infile in infiles:
            outfile = pattern(infile, gzip=args.gzip, bzip2=args.bzip2)
            outfiles.append(outfile)

    # print(outfiles)

    processes = min(args.processes, len(infiles))

    pb = Progress(len(infiles), message=f'Creating traceroutes with {processes} process')
    if processes == 1:
        for infile, outfile in pb.iterator(zip(infiles, outfiles)):
            convert(infile, outfile)
    else:
        with Pool(processes) as pool:
            for _ in pb.iterator(pool.imap_unordered(convert_wrapper, zip(infiles, outfiles))):
                pass

    # pb = Progress(len(infiles), message='Creating traceroutes')
    # if args.processes == 1:
    #     for t in pb.iterator(zip(args.infiles, outfiles)):
    #         convert(t)
    # else:
    #     with Pool(max(args.processes, len(infiles))) as pool:
    #         for _ in pb.iterator(pool.imap_unordered(convert, zip(infiles, outfiles))):
    #             pass


if __name__ == '__main__':
    main()
