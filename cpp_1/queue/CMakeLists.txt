cmake_minimum_required(VERSION 3.21)
project(queue LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_compile_options(-Wall -Wextra -Werror -pedantic -Wold-style-cast)

add_library(queue SHARED int_queue.cc)
target_include_directories(queue PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(main_int main_int.cc)
target_link_libraries(main_int PRIVATE queue)