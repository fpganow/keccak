#!/usr/bin/env python3.8
#
# Compare to online calculator:
#  http://emn178.github.io/online-tools/keccak_224_checksum.html
# - sha3-224sum on mac outputs matches sha3-224, but not keccak224

# Read more here:
# https://ethereum.stackexchange.com/questions/550/which-cryptographic-hash-function-does-ethereum-use

from io import StringIO
from pathlib import Path
import sha3
import shutil
import sys


def get_sha(data: str, size: int, bits: int) -> str:
    if bits == 224:
        sha = sha3.keccak_224()
    elif bits == 256:
        sha = sha3.keccak_256()
    elif bits == 384:
        sha = sha3.keccak_384()
    elif bits == 512:
        sha = sha3.keccak_512()

    print(f'size: {size}')
    if size > 0:
        text = data[0:size]
        print(f'encoding: {text}')
        text = bytes(text, encoding='utf-8')
        sha.update(text)
    hex_digest = sha.hexdigest()
    # 01 23 45 67 89 ab cd ef => ef cd ab 89 67 45 23 12
    # c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
    print(f'hex_digest:\n{hex_digest}')
    # little_endian := # [c5 d2 46 01 ... 70]
    little_endian = [ hex_digest[x:x+2] for x in range(0, len(hex_digest), 2) ]
    # le_grouped = [ [cd d2 46 01 ...], [xx yy zz ...], ... ]
    le_grouped = [ ''.join(list(reversed(little_endian[x:x+8]))) for x in range(0, len(little_endian), 8) ]
    # 3c23f7860146d2c5c000....
    return ''.join(le_grouped)


def get_exp_hashes(test_data: str) -> str:
    exp_hashes = StringIO()

    sha224 = get_sha(test_data, len(test_data), 224)
    print(f'{len(test_data):>3} {sha224}')
    import sys; sys.exit(0)

    for size in range(len(test_data)+1):
        sha224 = get_sha(test_data, size, 224)
        sha256 = get_sha(test_data, size, 256)
        sha384 = get_sha(test_data, size, 384)
        sha512 = get_sha(test_data, size, 512)
        exp_hashes.write(f'{size:>3} {sha224} {sha256} {sha384} {sha512}\n')
        #print(f'{size:>3} {sha256} {sha512}')
        print(f'{size:>3} {sha224} {sha256} {sha384} {sha512}')

    return exp_hashes.getvalue()

out_data_file = 'exp_results.dat'
in_data_text_file = 'test_data.txt'
in_data_file = 'test_data.dat'

print('\n')
# Read the raw text
in_data_str = Path(in_data_text_file).read_text().rstrip()
print(f'Length of input (raw) text: {len(in_data_str)}')
print(f'first: {in_data_str[0]}')
print(f'last: {in_data_str[-1]}')

print('\n')
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
    hex_line = list(reversed([ f'{ord(x):02x}' for x in hex_line]))
    in_data.write(f"{''.join(hex_line)}\n")
Path(in_data_file).write_text(in_data.getvalue())

# Generate hex version of expected hashes
exp_hash = get_exp_hashes(in_data_str)
print(f'Writing expected hashes/results to:\n  {out_data_file}\n')
Path(out_data_file).write_text(exp_hash)

# 9c a9 48 52 98
# Copy generated files to ../vivado/src/data
shutil.copy2(out_data_file, '../vivado/src/data')
