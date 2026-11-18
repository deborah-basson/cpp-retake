#include "regiment.hh"

void Regiment::join_by(Regiment& other)
{
    if (&other == this)
        return;

    soldiers_.insert(soldiers_.end(), other.soldiers_.begin(),
                     other.soldiers_.end());
    other.soldiers_.clear();
}

std::size_t Regiment::count() const
{
    return soldiers_.size();
}

void Regiment::add_soldier(Soldier* soldier)
{
    if (soldier)
        soldiers_.push_back(soldier);
}

void Regiment::print_state() const
{
    for (const Soldier* soldier : soldiers_)
        soldier->print_state();
}

void Regiment::scream() const
{
    for (const Soldier* soldier : soldiers_)
        soldier->scream();
}
