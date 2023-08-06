#!/usr/bin/env python3

import io
import sys
import base64
import fileinput
import pandas as pd
from typing import Union
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


SALT = b'6#t\x148\xf8\x01\xa5\xcdZ}\xd7\x89)\x19@'


def _getKey():
    kdf = Scrypt(salt=SALT, length=32, n=2**20, r=8, p=1)
    password = getpass().encode('utf-8')
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)


def _encrypt_cli(file: str = None):
    """ Encrypt file and write to stdout """
    sys.stdout.buffer.write(encrypt(file))


def _decrypt_cli(file: str):
    """ Decrypt file and write to stdout """
    sys.stdout.write(decrypt(file, _stream=False))


def _encrypt_pandas(df: pd.DataFrame, path: str):
    """ Encrypt pandas in parquet format """
    fernet = _getKey()
    f = io.BytesIO()
    df.columns = df.columns.astype(str)
    df.to_parquet(f)
    f.seek(0)
    data = fernet.encrypt(f.read())
    with open(path, 'wb') as f:
        f.write(data)


def _encrypt_file(file: str = None):
    """ Encrypt files """
    fernet = _getKey()
    if file is None:
        fileobj = sys.stdin
    else:
        fileobj = open(file, 'rb')
    with fileobj:
        data = fileobj.read()
    data = data.encode('utf-8') if file is None else data
    return fernet.encrypt(data)


def encrypt(file: Union[str, pd.DataFrame] = None, path: str = None):
    """ Encrypt pandas of file according to input """
    if isinstance(file, pd.DataFrame):
        assert file is not None
        return _encrypt_pandas(file, path)
    else:
        return _encrypt_file(file)


def decrypt(file: str, _stream: bool = True):
    fernet = _getKey()
    with open(file, 'rb') as fh:
        encrypted = fh.read()
        data = fernet.decrypt(encrypted)
    try:
        data = data.decode('utf-8')
        buffer = io.StringIO
    except UnicodeDecodeError:
        buffer = io.BytesIO
    return buffer(data) if _stream else data
