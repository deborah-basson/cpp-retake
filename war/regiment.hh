#pragma once

#include <vector>

#include "soldier.hh"

class Regiment
{
public:
    void join_by(Regiment& other);
    std::size_t count() const;
    void add_soldier(Soldier* soldier);
    void print_state() const;
    void scream() const;

private:
    std::vector<Soldier*> soldiers_;
};
