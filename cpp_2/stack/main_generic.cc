// main_generic.cc

#include <cassert>
#include <iostream>

#include "generic_stack.hh"

int main()
{
    auto s = GenericStack<std::string>{};
    s.push("12");
    s.push("15");
    auto x = s.pop();
    assert(x == "15");
    s.print();
    s.pop();
    s.push("42");
    s.push("62");

    auto n = s.top();
    assert(n->next->value == "42");
    assert(n->value == "62");
    assert(s.length() == 2);

    s.print();
    s.pop();
    s.pop();
    s.print();
    std::cout << std::endl;

    return 0;
}
