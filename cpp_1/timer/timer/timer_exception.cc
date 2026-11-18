#include "timer_exception.hh"

TimerException::TimerException(const std::string& action,
                               const std::string& state)
    : message_("Cannot " + action + ": Timer is " + state + ".")
{}

const char* TimerException::what() const noexcept
{
    return message_.c_str();
}