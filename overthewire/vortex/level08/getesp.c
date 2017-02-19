#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

unsigned long get_esp(void) {
   __asm__("movl %esp,%eax");
}


#define print(s)   (write(1, (s), sizeof((s))))

int main() {
    unsigned long x;
    char *s;
    static const char xdigits[16] = {
        "0123456789abcdef"
    };
    char hexstring[9]="";
    
    //fmt_x(get_esp(), (char *)hexstring+8);
    x = get_esp();
    s = &hexstring[7];
    for (; x; x>>=4) {
        *--s = xdigits[(x&15)];
    }
    print("ESP ");
    print(hexstring);
    print("\n");
    exit(0);
}
