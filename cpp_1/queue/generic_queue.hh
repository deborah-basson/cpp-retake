#pragma once

#include <initializer_list>
#include <iostream>
#include <memory>

template <typename T>
class GenericQueue
{
public:
    struct GenericNode
    {
        T value;
        std::unique_ptr<GenericNode> next;
    };

    GenericQueue() = default;
    GenericQueue(std::initializer_list<T> values);

    GenericQueue(const GenericQueue&) = delete;
    GenericQueue& operator=(const GenericQueue&) = delete;
    GenericQueue(GenericQueue&& other) noexcept;
    GenericQueue& operator=(GenericQueue&& other) noexcept;

    void enqueue(T value);
    T dequeue();
    const GenericNode* get_node(int index) const;
    std::size_t length() const;
    void print(std::ostream& os = std::cout) const;

private:
    std::unique_ptr<GenericNode> head_;
    GenericNode* tail_ = nullptr;
    std::size_t size_ = 0;
};

#include "generic_queue.hxx"