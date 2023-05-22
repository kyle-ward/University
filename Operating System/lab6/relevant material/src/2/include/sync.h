#ifndef SYNC_H
#define SYNC_H

#include "os_type.h"

class SpinLock
{
private:
    uint32 bolt;
public:
    SpinLock();
    void initialize();
    void lock();
    void unlock();
};


class myLock
{
public:
    uint32 flag = 1;
public:
    myLock();
    void initialize();
    void lock();
    void unlock();
};
#endif
