#!/usr/bin/env python3.8

from pathlib import Path
import sha3
import sys

def read_test_text(file_name: str):
    text = Path(file_name).read_text()[:-1]

    print(f'Calculating Keccak 256 and 512 on {file_name}')
    print(f'len(text): "{len(text)}"')
    sha = sha3.keccak_256()
    print(f'sha.name: {sha.name}')
    print(f'sha.digest_size: {sha.digest_size}')


    text = bytes(text, encoding='utf-8')
    print(f'text: "{text}"')
    sha.update(text)
    print(f'sha.hexdigest(): {sha.hexdigest()}')


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


test_datafile = 'test_text.txt'
test_data = Path(test_datafile).read_text()

for size in range(167):
    #sha224 = get_sha(test_data, size, 224)
    sha256 = get_sha(test_data, size, 256)
    #sha384 = get_sha(test_data, size, 384)
    sha512 = get_sha(test_data, size, 512)
    print(f'{size:>3} {sha256} {sha512}')
    #print(f'{size:>3} {sha224} {sha256} {sha384} {sha512}')

