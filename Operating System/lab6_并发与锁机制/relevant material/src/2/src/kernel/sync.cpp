#include "sync.h"
#include "asm_utils.h"
#include "stdio.h"
#include "os_modules.h"

SpinLock::SpinLock()
{
    initialize();
}

void SpinLock::initialize()
{
    bolt = 0;
}

void SpinLock::lock()
{
    uint32 key = 1;

    do
    {
        asm_atomic_exchange(&key, &bolt);
        //printf("pid: %d\n", programManager.running->pid);
    } while (key);
}

void SpinLock::unlock()
{
    bolt = 0;
}



myLock::myLock()
{
    initialize();
}
void myLock::lock()
{
    printf("myLock::lock\n");
    while(!flag){
        //printf("%d", flag);
    }
    flag = 0;
}
void myLock::unlock()
{
    printf("myLock::unlock\n");
    flag = 1;
}
void myLock::initialize()
{
    printf("myLock::initialize\n");
    flag = 1;
}
