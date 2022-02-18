#!/usr/bin/env python3
# Authored by Timothy Mui 2/17/2022
# Version 0.1.0

import re
import argparse

version_info = (0, 1, 0)
version = '.'.join(str(c) for c in version_info)

usage = ["Command usage: nmap_parser.py {input file} {output file} {ports file} "]

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='''
   Parses .nmap text file for open ports and will exclude ports in supplied port file
   
   *NOTE* The ports file format should be one line per {port number}/{protocol}
          Example: 443/tcp
                   22/tcp    ''', 
   epilog=' ')
parser.add_argument("input_file", help='''Enter input file ''')
parser.add_argument("output_file", help='''Enter output file ''')
parser.add_argument('ports_file', help= 
'''Enter ports file with ports to ignore. 
File format should be one line per {port number}/{protocol} '''
   )
parser.add_argument('-v','--version', action='version', version='%(prog)s {}'.format(version), 
                    help='show the version number and exit')
args = parser.parse_args()

#print(f"input:  {args.input_file!r}")
#print(f"output:  {args.output_file!r}")
#print(f"ports:  {args.ports_file!r}")

input_file = args.input_file
output_file = args.output_file
ports_file = args.ports_file

# read in input file
with open(input_file) as infile:
    lines = infile.readlines()

outfile = open(output_file, 'w')

# read in ports file
#print("Opening port file")
with open(ports_file) as portfile:
    portlines = portfile.read().splitlines()

port_test = '(?:% s)' % '|'.join(portlines)
portfile.close()

for line in lines:
    ip_address_match = re.match('^Nmap\sscan', line)
    host_ip_pattern = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)

    if ip_address_match:
#        print('\n',host_ip_pattern[0])
        outfile.write(f"\n{host_ip_pattern[0]}\n")
    ports = re.findall(port_test, line)

    if not ports:
        if re.search('open\s\s',line):
#            print(line)
#            print ('    ',line,end='')
            outfile.write(f"    {line}")

outfile.write('\n')
outfile.close()
infile.close()
