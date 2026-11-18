#pragma once

#include <optional>
#include <string>

#include "timer.hh"

class AutoTimer
{
public:
    explicit AutoTimer(const std::string& name);
    AutoTimer(const std::string& name, Timer& timer);
    ~AutoTimer();

    AutoTimer(const AutoTimer&) = delete;
    AutoTimer& operator=(const AutoTimer&) = delete;

private:
    std::string name_;
    std::optional<Timer> own_timer_;
    Timer& timer_;
    double offset_;
};
