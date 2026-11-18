// main_int.cc

#include <cassert>
#include <iostream>

#include "int_stack.hh"

int main()
{
    auto s = IntStack{};
    s.print(); // prints "[]" on std::cout.
    s.push(13); // s = [ 13 ]
    s.push(12); // s = [ 12, 13 ]
    assert(s.length() == 2);

    int x = s.pop(); // s = [ 13 ] , x = 12
    assert(x == 12);

    s.print(); // prints "[13]" on std::cout.
    s.push(14); // s = [ 14, 13 ]
    s.print(std::cerr); // prints "[14,13]" on std::cerr.

    int y = s.pop(); // s = [ 13 ] , y = 14
    assert(y == 14);
    assert(s.length() == 1);

    int z = s.pop(); // s = [ ] , z = 13
    assert(z == 13);
    assert(s.length() == 0);

    /****** top ******/
    s.push(6);
    const IntStack::IntNode* top = s.top();
    assert(top->next == nullptr);
    assert(top->value == 6);

    return 0;
}
