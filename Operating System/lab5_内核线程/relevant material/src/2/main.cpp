#include <iostream>
#include <time.h>

typedef char *va_list;
#define _INTSIZEOF(n) ((sizeof(n) + sizeof(int) - 1) & ~(sizeof(int) - 1))
#define va_start(ap, v) (ap = (va_list)&v + _INTSIZEOF(v))
#define va_arg(ap, type) (*(type *)((ap += _INTSIZEOF(type)) - _INTSIZEOF(type)))
#define va_end(ap) (ap = (va_list)0)
#define CLOCKS_PER_SEC 1000000

void delay()
{
    clock_t start_time;//, cur_time;
    start_time = clock();//clock()返回当前时间
    for (; (clock() - start_time) < 3 * CLOCKS_PER_SEC;);//延迟3秒
}



void print_any_number_of_integers(int n, ...);

int main()
{
    print_any_number_of_integers(1, 213);
    delay();
    print_any_number_of_integers(2, 234, 2567);
    print_any_number_of_integers(3, 487, -12, 0);
}

void print_any_number_of_integers(int n, ...)
{
    // 定义一个指向可变参数的指针parameter
    va_list parameter;
    // 使用固定参数列表的最后一个参数来初始化parameter
    // parameter指向可变参数列表的第一个参数
    va_start(parameter, n);
    
    for (int i = 0; i < n; ++i)
    {
        // 引用parameter指向的int参数，并使parameter指向下一个参数
        std::cout << va_arg(parameter, int) << " ";
    }

    // 清零parameter
    va_end(parameter);

    std::cout << std::endl;
}
