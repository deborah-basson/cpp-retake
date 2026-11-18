#include "int_queue.hh"

#include <stdexcept>
#include <utility>

IntQueue::IntQueue(std::initializer_list<int> values)
{
    for (int value : values)
        enqueue(value);
}

IntQueue::IntQueue(IntQueue&& other) noexcept
    : head_(std::move(other.head_))
    , tail_(std::exchange(other.tail_, nullptr))
    , size_(std::exchange(other.size_, 0))
{}

IntQueue& IntQueue::operator=(IntQueue&& other) noexcept
{
    head_ = std::move(other.head_);
    tail_ = std::exchange(other.tail_, nullptr);
    size_ = std::exchange(other.size_, 0);
    return *this;
}

void IntQueue::enqueue(int value)
{
    auto node = std::make_unique<IntNode>(value, nullptr);
    IntNode* new_tail = node.get();

    if (tail_)
        tail_->next = std::move(node);
    else
        head_ = std::move(node);

    tail_ = new_tail;
    ++size_;
}

int IntQueue::dequeue()
{
    if (!head_)
        throw std::out_of_range("IntQueue::dequeue: empty queue");

    int value = head_->value;
    head_ = std::move(head_->next);
    if (!head_)
        tail_ = nullptr;
    --size_;
    return value;
}

const IntQueue::IntNode* IntQueue::get_node(int index) const
{
    if (index < 0 || static_cast<std::size_t>(index) >= size_)
        throw std::out_of_range("IntQueue::get_node: invalid index");

    const IntNode* node = head_.get();
    for (int i = 0; i < index; ++i)
        node = node->next.get();
    return node;
}

std::size_t IntQueue::length() const
{
    return size_;
}

void IntQueue::print(std::ostream& os) const
{
    os << '[';
    for (const IntNode* node = head_.get(); node; node = node->next.get())
    {
        os << node->value;
        if (node->next)
            os << ',';
    }
    os << ']';
}