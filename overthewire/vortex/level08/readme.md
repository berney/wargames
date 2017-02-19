Reversing: -
  - Uses pthreads
  - Starts a thread running safecode()
    - Keeps looping print out a variable
  - Drops privileges, setting ruid, euid, suid, rgid, egid, rgid to uid, gid 
  - Calls unsafecode()
    - It's already dropped privs in this thread
    - Vulnerable to stackoverflow
        - Strcpy(buf_408, argv[1])
    - Can overwrite GOT/RELS or similar for library functions that privileged thread is making
      - I think shellcode will need to do do this hijacking of the GOT/RELS
      - pointing them the buffer with 2nd stage shellcode that drops shell
      - or if No-exec stack then malloc a RWX page and copy 2nd stage there

testing shellcode:
  - I created a `test_sc.c` to test shellcodes are working correctly
    - later expanded it to take arg from commandline

exploiting:
  - relatively easy
  - I took some time making a null-free shellcode that can print out printf `fmt_x` style longs.
    - `fmt_x` code stollen from musl c
  - first stage shellcode gets ESP and prints it out, then patches printf reloc to second stage shellcode
  - second stage shellcode is regular r2 exec /bin/sh shellcode
  - 1st stage shellcode calls exit syscall but that just terminates that thread not all threads.
  - 1st stage shellcode is in `getesp.asm`
    - assemble with NASM: `nasm getesp.asm`
  - inspect shellcode with r2: `r2 getesp`
  - do building of stage1 + stage2 + padding + addr (overwrite saved return address to point to start of stage1)
    - It fixes up stage1 shellcode's patch of printf reloc with addr of stage2 shellcode
  - To work you need to know the address stage1 will be at (e.g. argv[1]).
    - This changes for each login AFAICT
    - Easy way is to set overwrite address to something bad, e.g. 0x01020304, so it will crash immediately
    - then look around ESP - 0x400
    - Once you know the addr shellcode will start it should be the same for each try in that session.
    - Copy fixed-up buffer to `v8.rr2` script
  - Use rarun2 script `v8.rr2` to set arg1, clearenv, and a few other things
  - Open a second session, we will redirect I/O to 2nd tty,
    - In 2nd session get tty with `tty` command
    - Fix-up `v8.rr2` script with correct tty
    - In 2nd session run `clear; sleep 99999999` to clear terminal and block it from interfering with I/O
    - In 1st session running `v8.rr2` should now drop shell in 2nd session, where you can interact
    - Redirecting I/O is not necessary, but it makes debugging easier because safe thread is printing 0 in a loop.
    
