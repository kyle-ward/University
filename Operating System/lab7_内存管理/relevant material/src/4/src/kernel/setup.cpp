#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"
#include "sync.h"
#include "memory.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;
// 内存管理器
MemoryManager memoryManager;


void my_first_thread(void *arg)
{
    printf("my first thread\n");
}


void first_thread(void *arg)
{
    // 第1个线程不可以返回
    //stdio.moveCursor(0);
    //for (int i = 0; i < 25 * 80; ++i)
    //{
        //stdio.print(' ');
    //}
    //stdio.moveCursor(0);
    char *p1 = (char *)memoryManager.allocatePhysicalPages(AddressPoolType::KERNEL, 200);
    char *p2 = (char *)memoryManager.allocatePhysicalPages(AddressPoolType::KERNEL, 80);
    char *p3 = (char *)memoryManager.allocatePhysicalPages(AddressPoolType::KERNEL, 200);
    char *p4 = (char *)memoryManager.allocatePhysicalPages(AddressPoolType::KERNEL, 20);
    char *p5 = (char *)memoryManager.allocatePhysicalPages(AddressPoolType::KERNEL, 200);

    printf("%x %x %x %x %x\n\n\n", p1, p2, p3, p4, p5);

    memoryManager.releasePhysicalPages(AddressPoolType::KERNEL, (int)p2, 80);
    memoryManager.releasePhysicalPages(AddressPoolType::KERNEL, (int)p4, 20);
    char *p6 = (char *)memoryManager.allocatePhysicalPages(AddressPoolType::KERNEL, 10);
    char *p7 = (char *)memoryManager.allocatePhysicalPages(AddressPoolType::KERNEL, 20);

    printf("%x %x\n", p6, p7);

    asm_halt();
}

extern "C" void setup_kernel()
{

    // 中断管理器
    interruptManager.initialize();
    interruptManager.enableTimeInterrupt();
    interruptManager.setTimeInterrupt((void *)asm_time_interrupt_handler);

    // 输出管理器
    stdio.initialize();

    // 进程/线程管理器
    programManager.initialize();

    // 内存管理器
    memoryManager.openPageMechanism();
    memoryManager.initialize();
    //memoryManager.allocatePhysicalPages(AddressPoolType::USER, 4);

    // 创建第一个线程
    //printf("%x\n", first_thread);
    
    int pid = programManager.executeThread(first_thread, nullptr, "first thread", 1);
    if (pid == -1)
    {
        printf("can not execute thread\n");
        asm_halt();
    }
    
    ListItem *item = programManager.readyPrograms.front();
    PCB *firstThread = ListItem2PCB(item, tagInGeneralList);
    firstThread->status = RUNNING;
    programManager.readyPrograms.pop_front();
    programManager.running = firstThread;
    asm_switch_thread(0, firstThread);
    
    asm_halt();
}
