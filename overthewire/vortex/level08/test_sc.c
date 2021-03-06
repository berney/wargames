#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/*
 * compile with gcc -m32 -z execstack -o test_sc test_sc.c
 */

/*
#define _BUFFER_SIZE 70
const uint8_t buffer[70] = {
  0xe9, 0x08, 0x00, 0x00, 0x00, 0x68, 0x65, 0x6c, 0x6c, 0x6f,
  0x21, 0x0a, 0x00, 0x53, 0xb8, 0x04, 0x00, 0x00, 0x00, 0xe8,
  0x2a, 0x00, 0x00, 0x00, 0x81, 0xc3, 0x17, 0x1e, 0x00, 0x00,
  0xba, 0x07, 0x00, 0x00, 0x00, 0x8d, 0x8b, 0xd6, 0xe1, 0xff,
  0xff, 0x53, 0xbb, 0x01, 0x00, 0x00, 0x00, 0xcd, 0x80, 0x5b,
  0xb8, 0x01, 0x00, 0x00, 0x00, 0x53, 0xbb, 0x00, 0x00, 0x00,
  0x00, 0xcd, 0x80, 0x5b, 0x5b, 0xc3, 0x8b, 0x1c, 0x24, 0xc3
};
*/
/*
#define _BUFFER_SIZE 162
const uint8_t buffer[162] = {
  0xe9, 0x0a, 0x00, 0x00, 0x00, 0x89, 0xe0, 0xc3, 0x45, 0x53,
  0x50, 0x20, 0x00, 0x0a, 0x00, 0x55, 0xb9, 0x05, 0x00, 0x00,
  0x00, 0x89, 0xe5, 0x31, 0xc0, 0x57, 0x56, 0x53, 0xe8, 0x7d,
  0x00, 0x00, 0x00, 0x81, 0xc3, 0x0e, 0x1e, 0x00, 0x00, 0x83,
  0xe4, 0xf0, 0x83, 0xec, 0x10, 0x8d, 0x7c, 0x24, 0x0b, 0xc7,
  0x44, 0x24, 0x07, 0x00, 0x00, 0x00, 0x00, 0xf3, 0xaa, 0xe8,
  0xc5, 0xff, 0xff, 0xff, 0x85, 0xc0, 0x74, 0x05, 0xc1, 0xe8,
  0x04, 0xeb, 0xf7, 0xbe, 0x04, 0x00, 0x00, 0x00, 0xba, 0x05,
  0x00, 0x00, 0x00, 0x89, 0xf0, 0x8d, 0x8b, 0xd9, 0xe1, 0xff,
  0xff, 0x53, 0xbb, 0x01, 0x00, 0x00, 0x00, 0xcd, 0x80, 0x5b,
  0x8d, 0x4c, 0x24, 0x07, 0x89, 0xf0, 0xb2, 0x09, 0x53, 0xbb,
  0x01, 0x00, 0x00, 0x00, 0xcd, 0x80, 0x5b, 0x89, 0xf0, 0xb2,
  0x02, 0x8d, 0x8b, 0xde, 0xe1, 0xff, 0xff, 0x53, 0xbb, 0x01,
  0x00, 0x00, 0x00, 0xcd, 0x80, 0x5b, 0xb8, 0x01, 0x00, 0x00,
  0x00, 0x53, 0xbb, 0x00, 0x00, 0x00, 0x00, 0xcd, 0x80, 0x5b,
  0x8d, 0x65, 0xf4, 0x5b, 0x5e, 0x5f, 0x5d, 0xc3, 0x8b, 0x1c,
  0x24, 0xc3
};
*/

#define _BUFFER_SIZE 121
const uint8_t buffer[121] = {
  0xeb, 0x5d, 0x5e, 0x89, 0xf1, 0x31, 0xd2, 0xb2, 0x04, 0x31,
  0xdb, 0x43, 0x31, 0xc0, 0xb0, 0x04, 0xcd, 0x80, 0x89, 0xf0,
  0x04, 0x05, 0x89, 0xc5, 0x89, 0xe0, 0x2c, 0x08, 0x94, 0x89,
  0xc7, 0x56, 0x85, 0xc0, 0x74, 0x13, 0x89, 0xc6, 0x83, 0xe6,
  0x0f, 0x4e, 0x0f, 0xb6, 0x5c, 0x35, 0x01, 0x4f, 0x88, 0x1f,
  0xc1, 0xe8, 0x04, 0xeb, 0xe9, 0x5e, 0x89, 0xf9, 0x31, 0xd2,
  0xb2, 0x08, 0x31, 0xdb, 0x43, 0x31, 0xc0, 0xb0, 0x04, 0xcd,
  0x80, 0x89, 0xf1, 0x80, 0xc1, 0x04, 0x31, 0xd2, 0x42, 0x31,
  0xdb, 0x43, 0x31, 0xc0, 0xb0, 0x04, 0xcd, 0x80, 0x31, 0xdb,
  0x31, 0xc0, 0x40, 0xcd, 0x80, 0xe8, 0x9e, 0xff, 0xff, 0xff,
  0x45, 0x53, 0x50, 0x20, 0x10, 0x30, 0x31, 0x32, 0x33, 0x34,
  0x35, 0x36, 0x37, 0x38, 0x39, 0x61, 0x62, 0x63, 0x64, 0x65,
  0x66
};


int main(int argc, char* argv[]) {
    //int* ret;
    char buf[0x420];
    void (*shellcode)(void);
    
    if (strlen(argv[1]) > sizeof(buf)) {
        printf("shellcode too big!");
        exit(1);
    }
    strncpy(buf, argv[1], sizeof(buf));

    shellcode = &buf;
    shellcode();
    printf("shellcode continued execution of main program!");
    exit(2);
    
    //ret = (int *)&ret + 2; // address of saved return address on stack
    //(*ret) = (int)buffer; // change saved return address on stack
    // after we return here, we'll effectively jump to our shellcode buffer
}
