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

Semaphore chopsticks[5];
Semaphore mutex;
int count = 0;

void eating(){
    int delay = 0xfffffff;
    while(-- delay){}
}

void P1(void *arg){
    int i = 0;
    printf("philosopher 1 is going to eat.\n");
    mutex.P();
    printf("philosopher 1 starts picking up chopsticks.\n");
    chopsticks[i].P();
    eating();
    chopsticks[(i + 1) % 5].P();
    mutex.V();
    eating();
    printf("philosopher 1 finished eating.\n");
    chopsticks[i].V();
    chopsticks[(i + 1) % 5].V();
    count ++;
}
void P2(void *arg){
    int i = 1;
    printf("philosopher 2 is going to eat.\n");
    mutex.P();
    printf("philosopher 2 starts picking up chopsticks.\n");
    chopsticks[i].P();
    eating();
    chopsticks[(i + 1) % 5].P();
    mutex.V();
    eating();
    printf("philosopher 2 finished eating.\n");
    chopsticks[i].V();
    chopsticks[(i + 1) % 5].V();
    count ++;
}
void P3(void *arg){
    int i = 2;
    printf("philosopher 3 is going to eat.\n");
    mutex.P();
    printf("philosopher 3 starts picking up chopsticks.\n");
    chopsticks[i].P();
    eating();
    chopsticks[(i + 1) % 5].P();
    mutex.V();
    eating();
    printf("philosopher 3 finished eating.\n");
    chopsticks[i].V();
    chopsticks[(i + 1) % 5].V();
    count ++;
}
void P4(void *arg){
    int i = 3;
    printf("philosopher 4 is going to eat.\n");
    mutex.P();
    printf("philosopher 4 starts picking up chopsticks.\n");
    chopsticks[i].P();
    eating();
    chopsticks[(i + 1) % 5].P();
    mutex.V();
    eating();
    printf("philosopher 4 finished eating.\n");
    chopsticks[i].V();
    chopsticks[(i + 1) % 5].V();
    count ++;
}
void P5(void *arg){
    int i = 4;
    printf("philosopher 5 is going to eat.\n");
    mutex.P();
    printf("philosopher 5 starts picking up chopsticks.\n");
    chopsticks[i].P();
    eating();
    chopsticks[(i + 1) % 5].P();
    mutex.V();
    eating();
    printf("philosopher 5 finished eating.\n");
    chopsticks[i].V();
    chopsticks[(i + 1) % 5].V();
    count ++;
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

    mutex.initialize(1);
    for(int i = 0; i < 5; i ++){chopsticks[i].initialize(1);}

    programManager.executeThread(P1, nullptr, "P1", 1);
    programManager.executeThread(P2, nullptr, "P2", 1);
    programManager.executeThread(P3, nullptr, "P3", 1);
    programManager.executeThread(P4, nullptr, "P4", 1);
    programManager.executeThread(P5, nullptr, "P5", 1);
    while(true){
        if(count == 5){
            printf("\n\nOK, all precesses have been done.\n");
            break;
        }
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
