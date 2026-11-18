#include "timer.hh"

#include "timer_exception.hh"

void Timer::start()
{
    if (running_)
    {
        throw TimerException("start", "running");
    }
    if (!at_zero_)
    {
        throw TimerException("start", "not at zero");
    }

    running_ = true;
    at_zero_ = false;
    start_time_ = yakatime::now();
}

void Timer::pause()
{
    if (!running_)
    {
        throw TimerException("pause", "not running");
    }

    elapsed_ += yakatime::now() - start_time_;
    running_ = false;
}

void Timer::resume()
{
    if (running_)
    {
        throw TimerException("resume", "running");
    }
    if (at_zero_)
    {
        throw TimerException("resume", "at zero");
    }

    running_ = true;
    start_time_ = yakatime::now();
}

void Timer::reset()
{
    *this = Timer{};
}

double Timer::elapsed() const
{
    if (running_)
    {
        throw TimerException("elapsed", "running");
    }

    return elapsed_;
}

bool Timer::is_running() const
{
    return running_;
}

bool Timer::is_at_zero() const
{
    return at_zero_;
}
