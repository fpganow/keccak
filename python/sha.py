#!/usr/bin/python3.8

from pathlib import Path
import sha3
import sys


#file_name = 'test_text.txt'
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


def gen_hash(size: int) -> str:
    pass


