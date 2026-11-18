#include "time_it.hh"

#include <iostream>

#include "timer.hh"

void time_it(const std::function<void()>& function)
{
    auto timer = Timer{};
    timer.start();
    try
    {
        function();
    }
    catch (...)
    {
        timer.pause();
        std::cout << "Function terminated with an error in " << timer.elapsed()
                  << " seconds.\n";
        return;
    }
    timer.pause();
    std::cout << "Function terminated successfully in " << timer.elapsed()
              << " seconds.\n";
}