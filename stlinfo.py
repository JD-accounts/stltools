#! /usr/bin/env python
# -*- python coding: utf-8 -*-
# Copyright © 2012,2013 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# $Date$
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

'''Reads an STL file and prints information about the object or a text
representation of the object in the file.'''

import argparse
import sys
import time
from brep import stlfile, stlobject

ver = ('stlinfo [ver. ' + '$Revision$'[11:-2] +
       '] ('+'$Date$'[7:-2]+')')

def main(argv):
    """Main program.

    Keyword arguments:
    argv -- command line arguments (without program name!)
    """
    parser = argparse.ArgumentParser(description=__doc__)
    astr = 'find unique points, normals.'
    parser.add_argument('-a', '--assemble', action='store_true',
                        help=astr)
    parser.add_argument('-t', '--text', action='store_true',
                        help='print text representation of the file')
    parser.add_argument('file', nargs='*', help='one or more file names')
    args = parser.parse_args(argv)
    if not args.file:
        parser.print_help()
        sys.exit(0)
    for fn in args.file:
        try:
            rf = stlfile.StlReader(fn)
        except ValueError as e:
            print fn + ':', e        
        print "Information for:", fn
        print "Generated by {}\non {}.".format(ver, time.asctime())
        print 'type:', rf.filetype
        raw = stlobject.RawStl(rf.name)
        fcts = rf.readall()
        degen = raw.addfacets(fcts)
        nf = 'Number of facets:'
        if degen:
            print len(degen), 'degenerate facets found:', degen
        if args.assemble:
            indexed = stlobject.IndexedStl.fromraw(raw)
            if args.text:
                print indexed
            else:
                print 'name:', indexed.name
                print nf, indexed.numfacets
                print 'number of unique vertices:', indexed.numvertices
                print 'number of unique normals:', indexed.numnormals
                print indexed.bbox()
        else:
            if args.text:
                print raw
            else:
                print 'name:', raw.name
                print nf, raw.numfacets
                print raw.bbox()


if __name__ == '__main__':
    main(sys.argv[1:])

