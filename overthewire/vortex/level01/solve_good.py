#!/usr/bin/env python
import angr
import IPython

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines)

proj = angr.Project("./vortex1")
s = proj.factory.entry_state()
s.add_constraints(s.posix.read_from(0,256)=="\\"*256)
s.posix.get_file(0).seek(0)
s.options.discard("LAZY_SOLVES")
pg = proj.factory.path_group(s)
pg.explore(find=0x804862C)
solution_input = pg.found[0].state.posix.dumps(0)
print solution_input

IPython.embed()
