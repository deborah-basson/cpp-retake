#pragma once

#include <chrono>
#include <thread>

namespace yakatime
{

    class TimePoint
    {
    public:
        TimePoint() = default;

        TimePoint(std::chrono::time_point<std::chrono::system_clock> tp)
            : tp_(tp)
        {}

        double operator-(const TimePoint& other)
        {
            std::chrono::duration<double> elapsed_seconds = tp_ - other.tp_;
            return elapsed_seconds.count();
        }

    private:
        std::chrono::time_point<std::chrono::system_clock> tp_;
    };

    inline TimePoint now()
    {
        return std::chrono::system_clock::now();
    }

    inline void sleep_for(double x)
    {
        std::this_thread::sleep_for(
            std::chrono::milliseconds(static_cast<int>(x * 1000)));
    }
} // namespace yakatime
