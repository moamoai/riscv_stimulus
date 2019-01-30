#include <stdio.h>

#define UI32 unsigned int

// void OUTPUT(UI32 addr, UI32 data){
//   *(volatile UI32 *)(addr) = data;
// }
#define OUTPUT(addr, data) *(volatile UI32 *)(addr) = data; 

void main(void) {
  // printf("Hello World\n");
  int a = 1;
  int b = 10;
  OUTPUT(0x1000,a+b);
  OUTPUT(0x1000,0xdeadbeef);
}
