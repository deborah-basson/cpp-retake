#pragma once

#include "soldier.hh"

class Knight : public Soldier
{
public:
    Knight();

    void scream() const override;
};
