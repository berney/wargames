#!/usr/bin/env python

# I've already manually solved this level, but I want to learn how to use angr
# I want to use it on future levels and on other tasks.
# Currently because of the loop this explodes and dies
# I've worked out how to add veritesting which is a technique to help with such cases but it still explodes
# I have worked out how to get registers from state after exploring
#
# angr has a Unicorn plugin that can give speed boosts, I'll try it.

# I haven't work out how to continue exploring, I want to explore, get the ESP, work out the address of the ptr var, make it symbolic (for tracking progress)
# I want to restrict input to help guide angr
# I want to iterate so I can see what's happening
# I think it's possible to start at main rather than the gcc entry point
#   - I can probably set ESP to a value I want, I can then know where locals on the stack, like ptr will be stored in memory
# Once I get to the goal of the backdoor, it then needs to cope with running the command, there was a trick of padding it out with spaces
# There is some other trick that I no longer understand.

import angr
import logging
import IPython

GOAL = 0x804862c
         
AVOID = (
    0x80486a2,  # getchar failed
    0x80485ff)  # '\n' print buf and continue
LEVEL = logging.INFO

logger = None

def setup_logging():
    global logger
    logging.basicConfig(level=LEVEL)
    handler = logging.StreamHandler()
    handler.setLevel(LEVEL)
    logger = logging.getLogger()
    logger.setLevel(LEVEL)
    logger.addHandler(handler)
    # don't print so much veritesting logs
    logging.getLogger('angr.analyses.veritesting').setLevel(logging.ERROR)


def main():
    setup_logging()
    logger.debug("Welcome to the Jungle")
    
    project = angr.Project('vortex1', load_options={"auto_load_libs": False})
    
    # entry_state loads it to the entry point.
    #initial_state = project.factory.entry_state(args=['./vortex1'])
    # LAZY_SOLVES is on by default, by turning it off paths will be eliminated which helps stop explosions.
    #initial_state = project.factory.entry_state(args=['./vortex1'], remove_options={angr.simuvex.o.LAZY_SOLVES})
    # Unicorn plugin uses Unicorn, which is a framework based on QEMU
    #initial_state = project.factory.entry_state(args=['./vortex1'], add_options=angr.simuvex.o.unicorn, remove_options={angr.simuvex.o.LAZY_SOLVES})
    
    # Let's go straight to main, skipping the gcc entry point bullshit
    # XXX TODO How to find this in angr
    main_addr = 0x80485c0
    initial_state = project.factory.entry_state(args=['./vortex1'], addr=main_addr, add_options=angr.simuvex.o.unicorn, remove_options={angr.simuvex.o.LAZY_SOLVES})
    
    # For educational purposes lets symbolically execute the block and find what ESP is
    sirsb = project.factory.sim_block(initial_state)
    #IPython.embed()
    # This is more of a pain in the ass, we'll use breakpoints below which seems easier/better
    
    # Use breakpoints to get address of local variable on stack - ptr
    # this doesn't get triggered until we start executing the path when we start exploring the path_group
    def debug_fn(state):
	esp = state.se.any_int(state.regs.esp)
	ptr_addr = esp + 0x14
	ptr_val = state.se.any_int(state.memory.load(ptr_addr, 4, endness='Iend_LE'))
        logger.info("eip = {}; esp = {} / {}; eax = {}; ptr {} [{}]".format(
		state.regs.eip,
		state.regs.esp,
		hex(esp),
		state.regs.eax,
		hex(ptr_addr),
		hex(ptr_val)))
        IPython.embed()
    def cond(state):
        return state.se.any_int(state.regs.eip) == 0x080485e6
    #initial_state.inspect.b('mem_write', when=angr.simuvex.BP_AFTER, action=debug_fn)
    initial_state.inspect.b('mem_write', when=angr.simuvex.BP_AFTER, action=debug_fn, condition=cond)
    
    if True:
            # Cheat a bit and constrain the first 256 bytes to backslashes. There's only 4 more left, so hopefully this means we solve the problem.
            for _ in xrange(0x100):
                c = initial_state.posix.files[0].read_from(1)
                #initial_state.se.add(c == '\\')     # must be a single back-slash
                initial_state.se.add(c != '\n')     # must not be a new line
            # Reset the symbolic stdin properties - Rewind stdin back to pos 0
            initial_state.posix.files[0].seek(0)
    
    initial_path = project.factory.path(initial_state)
    pg = project.factory.path_group(initial_path)
    
    # Enable veritesting. This technique, described in a paper[1] from CMU, attempts to address the problem of state explosions in loops by performing smart merging.
    veritester = angr.exploration_techniques.veritesting.Veritesting()
    pg.use_technique(veritester)
    
    ## TODO - There should be a way to get the ptr local variable on the stack as a symbolic var
    ## TODO - There should be a way to iterate the explorer and print the value of the symbolic var as a way to watch progress
    ## TODO - There should be a way to constrain the input of getchar() (STDIN) so that only values of interest are used, e.g. '\' and something else.
    
    # initially pg has no attribute found, it's created after we start to explore
    found = False
    i = 0
    while not found:
        i += 1
        pg.explore(find=GOAL,avoid=AVOID,n=10) 
        found = pg.found
        sin = pg.active[0].state.posix.dumps(0)
        sin_len = pg.active[0].state.se.any_int(pg.active[0].state.posix.files[0].read_pos)
        sin = sin[:sin_len]
        logger.info("{}: Active paths: {}, active path 0 runs: {}, stdin: {}, {!r}".format(
            i, len(pg.active), pg.active[0].length, len(sin), sin))
        if i >= 2:
            IPython.embed()
    
    found = pg.found[0]
    sin = found.state.posix.dumps(0)
    print repr(sin)


if  __name__ == '__main__':
    main()
