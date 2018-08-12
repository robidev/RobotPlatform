#!/usr/bin/env python
import gzip
import zlib
import Image


WINDOW_BUF = 16 + zlib.MAX_WBITS

text = "testaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbba"


print "gzip test"
_zip = zlib.decompressobj(WINDOW_BUF)
data = zlib.compress(text, -1)
print "data: %s text: %s" % (data,zlib.decompress(data))

Image.frombytes('RGBA',(10,1),text).show()

