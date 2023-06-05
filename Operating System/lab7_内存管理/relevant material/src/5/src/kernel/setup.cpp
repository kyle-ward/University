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


SpinLock lock;
void my_thread1(void *arg){
    lock.lock();
    char *p = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 50);
    printf("my_thread1: p = %x\n", p);
    lock.unlock();
}
void my_thread2(void *arg){
    lock.lock();
    char *p = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 50);
    printf("my_thread2: p = %x\n", p);
    lock.unlock();
}



void first_thread(void *arg)
{
    // 第1个线程不可以返回
    // stdio.moveCursor(0);
    // for (int i = 0; i < 25 * 80; ++i)
    // {
    //     stdio.print(' ');
    // }
    // stdio.moveCursor(0);

    char *p1 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 100);
    char *p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 10);
    char *p3 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 100);

    printf("%x %x %x\n", p1, p2, p3);

    memoryManager.releasePages(AddressPoolType::KERNEL, (int)p2, 10);
    p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 100);

    printf("%x\n", p2);

    p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 10);
    
    printf("%x\n", p2);
    printf("-------------------------------------------------------\n");
    int pid1 = programManager.executeThread(my_thread1, nullptr, "my first thread", 1);
    int pid2 = programManager.executeThread(my_thread2, nullptr, "my second thread", 1);
    printf("\n\nend\n");
    asm_halt();
}

void FIFO_thread(void *arg){
    int p[8] = {1, 2, 3, 4, 5, 2, 1, 3};
    printf("The order of pages :");    //输出页分区访问顺序
    for(int i = 0; i < 8; i ++){
        printf("%d  ",p[i]);
    }
    printf("\n");
    for (int i = 0; i < 8; i ++){    //按照顺序访问页分区
        char *temp = (char *)memoryManager.allocatePagesFIFO(AddressPoolType::KERNEL, 10, p[i]);
        printf("p%d's Virtual address :%x    ",p[i], temp);
        printf("p%d's Physical address :  %x \n",p[i],memoryManager.vaddr2paddr((int)temp));
    }
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

    // 创建第一个线程
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
