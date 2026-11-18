#include <iostream>

int main(int argc, char* argv[])
{
    if (argc < 2)
    {
        std::cout << "No friends provided...\n";
        return 1;
    }

    for (int i = 1; i < argc; ++i)
        std::cout << "Hello " << argv[i] << "!\n";

    return 0;
}
