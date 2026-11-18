#pragma once

#include "soldier.hh"

class Assassin : public Soldier
{
public:
    Assassin();

    void scream() const override;
};
