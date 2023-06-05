#include <iostream>


extern "C" void function_from_CPP() {
    std::cout << "This is a function from C++." << std::endl;
}

extern "C" void function_from_me_CPP() {
    std::cout << 21307261 << std::endl;
}
