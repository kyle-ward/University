#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"
#include "sync.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;

Semaphore semapple;
Semaphore semorange;
Semaphore mutex;
Semaphore semplate;
int apple, orange, plate;

void dad(void *arg){
    semplate.P(); 

    mutex.P();
    printf("dad: let me prepare an apple for my son.\n");
    semapple.V(); 
    apple += 1;
    plate -= 1;
    printf("apple: %d\n", apple);
    printf("orange: %d\n", orange);
    printf("plate: %d\n\n", plate);
    mutex.V();
}
void mum(void *arg){
    semplate.P();
    
    mutex.P();
    printf("mum: let me prepare an orange for my daughter.\n");
    semorange.V(); 
    orange += 1;
    plate -= 1;
    printf("apple: %d\n", apple);
    printf("orange: %d\n", orange);
    printf("plate: %d\n\n", plate);
    mutex.V();
}
void son(void *arg){
    //printf("semapple: %d\n", semapple.counter);
    semapple.P(); 
    
    mutex.P();
    printf("son: thank you dad, I have eaten an apple.\n");
    apple -= 1;
    semplate.V(); 
    plate += 1;
    printf("apple: %d\n", apple);
    printf("orange: %d\n", orange);
    printf("plate: %d\n\n", plate);
    mutex.V();
}
void daughter(void *arg){
    semorange.P(); 
    
    mutex.P();
    printf("daughter: thank you mum, I have eaten an orange.\n");
    orange -= 1;
    semplate.V();
    plate += 1;
    printf("apple: %d\n", apple);
    printf("orange: %d\n", orange);
    printf("plate: %d\n\n", plate);
    mutex.V();
}



void first_thread(void *arg)
{
    // 第1个线程不可以返回
    stdio.moveCursor(0);
    for (int i = 0; i < 25 * 80; ++i)
    {
        stdio.print(' ');
    }
    stdio.moveCursor(0);
    apple = 0; semapple.initialize(0);
    orange = 0; semorange.initialize(0);
    plate = 1; semplate.initialize(1);
    mutex.initialize(1);
    //semaphore.initialize(1);

    programManager.executeThread(mum, nullptr, "mum", 1);
    programManager.executeThread(son, nullptr, "son", 1);
    programManager.executeThread(dad, nullptr, "dad", 1);
    programManager.executeThread(daughter, nullptr, "daughter", 1);
    
    int delay = 0xfffffff;
    while(-- delay){}
    printf("OK, all precesses have been done.\n");
    
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
