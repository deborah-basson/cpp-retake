#pragma once

#include <exception>
#include <string>

class TimerException : public std::exception
{
public:
    TimerException(const std::string& action, const std::string& state);

    const char* what() const noexcept override;

private:
    std::string message_;
};
