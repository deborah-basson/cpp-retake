#pragma once

#include <stdexcept>
#include <utility>

#include "generic_queue.hh"

template <typename T>
GenericQueue<T>::GenericQueue(std::initializer_list<T> values)
{
    for (const T& value : values)
        enqueue(value);
}

template <typename T>
GenericQueue<T>::GenericQueue(GenericQueue&& other) noexcept
    : head_(std::move(other.head_))
    , tail_(std::exchange(other.tail_, nullptr))
    , size_(std::exchange(other.size_, 0))
{}

template <typename T>
GenericQueue<T>& GenericQueue<T>::operator=(GenericQueue&& other) noexcept
{
    head_ = std::move(other.head_);
    tail_ = std::exchange(other.tail_, nullptr);
    size_ = std::exchange(other.size_, 0);
    return *this;
}

template <typename T>
void GenericQueue<T>::enqueue(T value)
{
    auto node = std::make_unique<GenericNode>(std::move(value), nullptr);
    GenericNode* new_tail = node.get();

    if (tail_)
        tail_->next = std::move(node);
    else
        head_ = std::move(node);

    tail_ = new_tail;
    ++size_;
}

template <typename T>
T GenericQueue<T>::dequeue()
{
    if (!head_)
        throw std::out_of_range("GenericQueue::dequeue: empty queue");

    T value = std::move(head_->value);
    head_ = std::move(head_->next);
    if (!head_)
        tail_ = nullptr;
    --size_;
    return value;
}

template <typename T>
auto GenericQueue<T>::get_node(int index) const -> const GenericNode*
{
    if (index < 0 || static_cast<std::size_t>(index) >= size_)
        throw std::out_of_range("GenericQueue::get_node: invalid index");

    const GenericNode* node = head_.get();
    for (int i = 0; i < index; ++i)
        node = node->next.get();
    return node;
}

template <typename T>
std::size_t GenericQueue<T>::length() const
{
    return size_;
}

template <typename T>
void GenericQueue<T>::print(std::ostream& os) const
{
    os << '[';
    for (const GenericNode* node = head_.get(); node; node = node->next.get())
    {
        os << node->value;
        if (node->next)
            os << ',';
    }
    os << ']';
}