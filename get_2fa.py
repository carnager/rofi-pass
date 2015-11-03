#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Manfred Touron <m@42.am>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import base64
import hashlib
import hmac
import math
import struct
import sys
import time


def get_hotp_token(key, intervals_no):
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(h[19]) & 15
    h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000
    return h


def get_totp_token(key):
    token = get_hotp_token(key, intervals_no=int(time.time()) // 30)
    return str(token).zfill(6)


def get_totp_time_remaining():
    return int(30 - (time.time() % 30))


def is_otp_secret_valid(secret):
    try:
        secret = secret.replace(' ', '')
        if not len(secret):
            return False
        secret = secret.ljust(int(math.ceil(len(secret) / 16.0) * 16), '=')
        key = base64.b32decode(secret, casefold=True)
        get_totp_token(key)
    except:
        return False

    return True


def get_hotp_key(key=None, secret=None, hexkey=None):
    if hexkey:
        key = hexkey.decode('hex')
    if secret:
        secret = secret.replace(' ', '')
        secret = secret.ljust(int(math.ceil(len(secret) / 16.0) * 16), '=')
        key = base64.b32decode(secret, casefold=True)
    return key


def get_token(secret):
    key = get_hotp_key(secret=secret)
    return get_totp_token(key)


def main():
    sys.stdout.write(get_token(sys.stdin.read().strip()))


if __name__ == "__main__":
    main()
