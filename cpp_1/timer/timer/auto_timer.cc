#include "auto_timer.hh"

#include <iostream>

AutoTimer::AutoTimer(const std::string& name)
    : name_(name)
    , own_timer_(Timer{})
    , timer_(*own_timer_)
    , offset_(0.0)
{
    timer_.start();
}

AutoTimer::AutoTimer(const std::string& name, Timer& timer)
    : name_(name)
    , timer_(timer)
    , offset_(timer.is_at_zero() ? 0.0 : timer.elapsed())
{
    if (timer_.is_at_zero())
        timer_.start();
    else
        timer_.resume();
}

AutoTimer::~AutoTimer()
{
    if (timer_.is_running())
        timer_.pause();
    std::cout << name_ << " took " << timer_.elapsed() - offset_
              << " seconds.\n";
}