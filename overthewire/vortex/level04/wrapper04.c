#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    char* fakev[8];

    fakev[0] = NULL;
    fakev[1] = "ENV0";
    fakev[2] = "ENV1";
    fakev[3] = argv[1];
    fakev[4] = NULL;
    fakev[5] = NULL;

    execve("/vortex/vortex4", &fakev[0], &fakev[1]);
    printf("execve failed\n");
}
