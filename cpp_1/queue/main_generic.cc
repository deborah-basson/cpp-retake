// main_generic.cc

#include <cassert>
#include <iostream>

#include "generic_queue.hh"

int main()
{
    auto q = GenericQueue<std::string>{};
    q.enqueue("12");
    q.enqueue("15");
    auto x = q.dequeue();
    assert(x == "12");
    q.print();
    q.dequeue();
    q.enqueue("42");
    q.enqueue("62");

    auto n = q.get_node(1);
    assert(n->next == nullptr);
    assert(n->value == "62");
    assert(q.length() == 2);

    q.print();
    q.dequeue();
    q.dequeue();
    q.print();
    std::cout << std::endl;

    return 0;
}
