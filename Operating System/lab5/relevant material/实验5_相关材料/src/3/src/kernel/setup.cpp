#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include <time.h>
#define CLOCK_PER_SEC 1000000

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;

void delay()
{
    clock_t start_time;//, cur_time;
    start_time = clock();//clock()返回当前时间
    for (; (clock() - start_time) < 3 * CLOCKS_PER_SEC;);//延迟3秒
}



extern "C" void setup_kernel()
{
    // 中断处理部件
    interruptManager.initialize();
    // 屏幕IO处理部件
    stdio.initialize();
    interruptManager.enableTimeInterrupt();
    interruptManager.setTimeInterrupt((void *)asm_time_interrupt_handler);
    //asm_enable_interrupt();
    printf("print percentage: %%\n"
           "print char \"N\": %c\n"
           "print string \"Hello World!\": %s\n"
           "print decimal: \"-1234\": %d\n"
           "print hexadecimal \"0x7abcdef0\": %x\n",
           'N', "Hello World!", -1234, 0x7abcdef0);
    printf("\n\nmy test:\n");
    printf("print char %%3c N: %3c\n", 'N');
    printf("printf decimal %%8d -1234: %8d", -1234);
    //uint a = 1 / 0;
    asm_halt();
}
