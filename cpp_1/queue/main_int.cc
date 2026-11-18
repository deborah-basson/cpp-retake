// main_int.cc

#include <cassert>
#include <iostream>

#include "int_queue.hh"

int main()
{
    auto q = IntQueue{};
    q.print(); // prints "[]" on std::cout.
    q.enqueue(12); // q = [ 12 ]
    q.enqueue(13); // q = [ 12, 13 ]
    assert(q.length() == 2);
    int x = q.dequeue(); // q = [ 13 ] , x = 12
    assert(x == 12);
    q.print(); // prints "[13]" on std::cout.
    q.enqueue(14); // q = [ 13, 14 ]
    q.print(std::cerr); // prints "[13,14]" on std::cerr.
    int y = q.dequeue(); // q = [ 14 ] , y = 13
    assert(y == 13);
    assert(q.length() == 1);

    /****** get_node ******/
    q.enqueue(6);
    const IntQueue::IntNode* index1 = q.get_node(1);
    assert(index1->next == nullptr);
    assert(index1->value == 6);

    const IntQueue::IntNode* index0 = q.get_node(0);
    assert(index0->next->value == 6);
    assert(index0->value == 14);
    std::cout << std::endl;

    /*
    q.get_node(2); // should throw std::out_of_range
    q.dequeue(); // we pop 14 q = [ 6 ]
    q.dequeue(); // we pop 6 q = []
    q.get_node(0); // should throw std::out_of_range
    */

    return 0;
}
