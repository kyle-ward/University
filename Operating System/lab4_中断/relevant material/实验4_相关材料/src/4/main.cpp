#include <iostream>

extern "C" void function_from_asm();
extern "C" void function_from_me_asm();

int main() {
    std::cout << "Call function from assembly." << std::endl;
    function_from_asm();
    function_from_me_asm();
    std::cout << "Done." << std::endl;
}
