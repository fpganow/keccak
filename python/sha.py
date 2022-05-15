#!/usr/bin/env python3.8
#
# Compare to online calculator:
#  http://emn178.github.io/online-tools/keccak_224_checksum.html
# - sha3-224sum on mac outputs matches sha3-224, but not keccak224

# Read more here:
# https://ethereum.stackexchange.com/questions/550/which-cryptographic-hash-function-does-ethereum-use

from argparse import ArgumentParser, Namespace
from io import StringIO
from pathlib import Path
import sha3
import shutil
import sys


def get_sha(args: Namespace, data: str, size: int, bits: int) -> str:
    if bits == 224:
        sha = sha3.keccak_224()
    elif bits == 256:
        sha = sha3.keccak_256()
    elif bits == 384:
        sha = sha3.keccak_384()
    elif bits == 512:
        sha = sha3.keccak_512()

    if size > 0:
        text = data[0:size]
#        print(f'encoding: {text}')
        text = bytes(text, encoding='utf-8')
        sha.update(text)
    hex_digest = sha.hexdigest()
    # 01 23 45 67 89 ab cd ef => ef cd ab 89 67 45 23 12
    # c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
    # little_endian := # [c5 d2 46 01 ... 70]
#    print(f'hex_digest: {hex_digest}')
    if args.little_endian:
        little_endian = [ hex_digest[x:x+2] for x in range(0, len(hex_digest), 2) ]
        # le_grouped = [ [cd d2 46 01 ...], [xx yy zz ...], ... ]
        le_grouped = [ ''.join(list(reversed(little_endian[x:x+8]))) for x in range(0, len(little_endian), 8) ]
        hex_digest = ''.join(le_grouped)

    return hex_digest


def get_exp_hashes(args: Namespace, test_data: str) -> str:
    exp_hashes = StringIO()

    for size in range(len(test_data)+1):
        sha224 = get_sha(args, test_data, size, 224)
        sha256 = get_sha(args, test_data, size, 256)
        sha384 = get_sha(args, test_data, size, 384)
        sha512 = get_sha(args, test_data, size, 512)
        exp_hashes.write(f'{size:>3} {sha224} {sha256} {sha384} {sha512}\n')
        #print(f'{size:>3} {sha224} {sha256} {sha384} {sha512}')

    return exp_hashes.getvalue()


def get_args() -> Namespace:
    my_parser = ArgumentParser(
        prog='sha',
        description='Sha-3 (Keccak) test case generator'
    )

    group = my_parser.add_mutually_exclusive_group()
    group.add_argument(
        '--big-endian',
        action='store_true',
        help='Sets the output format to big-endian.'
    )
    group.add_argument(
        '--little-endian',
        action='store_true',
        help='Sets the output format to little-endian.'
    )

    args = my_parser.parse_args()
    if not args.little_endian and not args.big_endian:
        args.big_endian = True
    return args

def main():
    args = get_args()
    if args.big_endian:
        print(f' - big endian')
    elif args.little_endian:
        print(f' - little endian')

    out_data_file = 'exp_results.dat'
    in_data_text_file = 'test_data.txt'
    in_data_file = 'test_data.dat'

    #print('\n')
    # Read the raw text
    in_data_str = Path(in_data_text_file).read_text().rstrip()

    print('')
    # Generate hex version of raw text
    print(f'Writing HEX version of input string to:\n  {in_data_file}\n')
    n = 8

    # Little-endian
    # data is "As Estha"
    # gets written as "ahtsE sA"
    in_data = StringIO()
    for line in [ in_data_str[x:x+8] for x in range(0, len(in_data_str), n)]:
        hex_line = line
        if len(hex_line) < n:
            hex_line += '\0' * (n - len(hex_line))
        if args.little_endian:
            hex_line = list(reversed([ f'{ord(x):02x}' for x in hex_line]))
        else:
            hex_line = list([ f'{ord(x):02x}' for x in hex_line])
        in_data.write(f"{''.join(hex_line)}\n")
    Path(in_data_file).write_text(in_data.getvalue())

    # Generate hex version of expected hashes
    exp_hash = get_exp_hashes(args, in_data_str)
    print(f'Writing expected hashes/results to:\n  {out_data_file}\n')
    Path(out_data_file).write_text(exp_hash)

    # Copy generated files
    vivado_data_dir = '../vivado/src/data'

    print(f'Copying {out_data_file} to {vivado_data_dir}')
    shutil.copy2(out_data_file, vivado_data_dir)

    print(f'Copying {in_data_file} to {vivado_data_dir}')
    shutil.copy2(in_data_file, vivado_data_dir)

    print('')

if __name__ == '__main__':
    main()

