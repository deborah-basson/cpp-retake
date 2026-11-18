#pragma once

#include <initializer_list>
#include <iostream>
#include <memory>

class IntQueue
{
public:
    struct IntNode
    {
        int value;
        std::unique_ptr<IntNode> next;
    };

    IntQueue() = default;
    IntQueue(std::initializer_list<int> values);

    IntQueue(const IntQueue&) = delete;
    IntQueue& operator=(const IntQueue&) = delete;
    IntQueue(IntQueue&& other) noexcept;
    IntQueue& operator=(IntQueue&& other) noexcept;

    void enqueue(int value);
    int dequeue();
    const IntNode* get_node(int index) const;
    std::size_t length() const;
    void print(std::ostream& os = std::cout) const;

private:
    std::unique_ptr<IntNode> head_;
    IntNode* tail_ = nullptr;
    std::size_t size_ = 0;
};