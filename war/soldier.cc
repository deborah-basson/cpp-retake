#include "soldier.hh"

#include <iostream>

Soldier::Soldier(int health, int damage)
    : health_(health)
    , damage_(damage)
{}

void Soldier::attack(Soldier& other) const
{
    other.health_ -= damage_;
}

void Soldier::print_state() const
{
    std::cout << "I have " << health_ << " health points.\n";
}
