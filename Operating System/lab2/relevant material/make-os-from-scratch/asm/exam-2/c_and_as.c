#include <stdio.h>
int main()
{
        int a=10, b;
        asm ("movl %1, %%eax;"
             "movl %%eax, %0;"
             :"=r"(b)        /* output */
             :"r"(a)         /* input */
             :"%eax"         /* clobbered register */
             );       
  
    return 0;
}