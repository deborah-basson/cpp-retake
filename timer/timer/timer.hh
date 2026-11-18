#pragma once

#include "yakatime/yakatime.hh"

class Timer
{
public:
    void start();
    void pause();
    void resume();
    void reset();
    double elapsed() const;

    bool is_running() const;
    bool is_at_zero() const;

private:
    bool running_ = false;
    bool at_zero_ = true;
    double elapsed_ = 0.0;
    yakatime::TimePoint start_time_;
};
