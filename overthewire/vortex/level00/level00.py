#!/usr/bin/env python
import socket
import struct
import sys

a = "vortex.labs.overthewire.org"
p = 5842

s = socket.socket()
print "Connecting..."
s.connect((a,p))

b = ""
tries = 0
while len(b) < 16 and tries < 16:
    b += s.recv(16 - len(b))
    tries += 1
    print tries, len(b), b
if len(b) < 16:
    print "Fuck"
    sys.exit(1)

x = 0
u = struct.unpack("<LLLL", b)
for i in u:
    x += i

print "Answer: {:x}".format(x)

s.send(struct.pack("<L", x & 0xFFFFFFFF))

print "Got: "
b = s.recv(128)
print b

