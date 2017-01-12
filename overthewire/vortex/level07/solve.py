import angr
## The beginning of the BB for the strcpy argv1 -> buf (buffer overflow) path
goal_ip = 0x08048506
## The beginning of the BB for the printf hi
avoid_ip = 0x08048520
proj = angr.Project("./vortex7", load_options={'auto_load_libs': False})
argv1 = angr.claripy.BVS("argv1", 0xE * 4)
s = proj.factory.entry_state(args=['./vortex7', argv1])
#s.add_constraints(s.posix.read_from(0,256)=="\\"*256)
#s.posix.get_file(0).seek(0)
## Speed optimization trade off
s.options.discard("LAZY_SOLVES")
pg = proj.factory.path_group(s)
pg.explore(find=goal_ip, avoid=avoid_ip)
if len(pg.found) == 0:
    print "[-] Solution not found"
else:
    #print pg.found[0].state.posix.dumps(0)
    sol = pg.found[0].state.se.any_str(argv1)
    print "[+] Solution: {!r}".format(sol)
