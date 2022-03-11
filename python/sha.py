#!/usr/bin/env python3.8

from io import StringIO
from pathlib import Path
import sha3
import sys

#def read_test_text(file_name: str):
#    text = Path(file_name).read_text()[:-1]
#
#    print(f'Calculating Keccak 256 and 512 on {file_name}')
#    print(f'len(text): "{len(text)}"')
#    sha = sha3.keccak_256()
#    print(f'sha.name: {sha.name}')
#    print(f'sha.digest_size: {sha.digest_size}')
#
#
#    text = bytes(text, encoding='utf-8')
#    print(f'text: "{text}"')
#    sha.update(text)
#    print(f'sha.hexdigest(): {sha.hexdigest()}')


def get_sha(data: str, size: int, bits: int) -> str:
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
        text = bytes(text, encoding='utf-8')
        sha.update(text)
    return sha.hexdigest()


def get_exp_hashes(test_data: str, num_cases: int) -> str:
    exp_hashes = StringIO()

    for size in range(num_cases):
        #sha224 = get_sha(test_data, size, 224)
        sha256 = get_sha(test_data, size, 256)
        #sha384 = get_sha(test_data, size, 384)
        sha512 = get_sha(test_data, size, 512)
        exp_hashes.write(f'{size:>3} {sha256} {sha512}\n')
        #print(f'{size:>3} {sha256} {sha512}')
        #print(f'{size:>3} {sha224} {sha256} {sha384} {sha512}')

    return exp_hashes.getvalue()

out_data_file = 'exp_results.dat'
in_data_text_file = 'test_data.txt'
in_data_file = 'test_data.dat'

print('\n')
# Read the raw text
in_data_str = Path(in_data_text_file).read_text().rstrip()

# Generate hex version of raw text
print(f'Writing HEX version of input string to:\n  {in_data_file}\n')
n = 8

in_data = StringIO()
for line in [ in_data_str[x:x+8] for x in range(0, len(in_data_str), n)]:
    hex_line = line
    if len(hex_line) < n:
        hex_line += '\0' * (n - len(hex_line))
    hex_line = list(reversed([ f'{ord(x):02x}' for x in hex_line]))
    in_data.write(f"{''.join(hex_line)}\n")
Path(in_data_file).write_text(in_data.getvalue())

# Generate hex version of expected hashes
exp_hash = get_exp_hashes(in_data_str, 167)
print(f'Writing expected hashes/results to:\n  {out_data_file}\n')
Path(out_data_file).write_text(exp_hash)

