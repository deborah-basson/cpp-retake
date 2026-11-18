#pragma once

class Soldier
{
public:
    virtual ~Soldier() = default;

    void attack(Soldier& other) const;
    void print_state() const;
    virtual void scream() const = 0;

protected:
    Soldier(int health, int damage);

private:
    int health_;
    int damage_;
};
