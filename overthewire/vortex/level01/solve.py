#!/usr/bin/env python
import angr
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.debug("Welcome to the Jungle")
    project = angr.Project('vortex1')
    state = project.factory.entry_state(args=['./vortex1'])
    pg = project.factory.path_group(state)
    pg.explore(find=0x804862c) 
    found = pg.found[0]
    sin = found.state.posix.dumps(0)
    print repr(sin)


if  __name__ == '__main__':
    main()
