"""Per-exercise config: files to submit, authorized headers, forbidden symbols.

Keys are exercise paths relative to the repo root.
"""

CXXFLAGS = [
    "-Wall",
    "-Wextra",
    "-Werror",
    "-pedantic",
    "-std=c++20",
    "-Wold-style-cast",
]

NO_NEW_DELETE = [r"\bnew\b", r"\bdelete\b"]


def _container(prefix):
    return {
        "files": [
            "CMakeLists.txt",
            f"generic_{prefix}.hh",
            f"generic_{prefix}.hxx",
            f"int_{prefix}.cc",
            f"int_{prefix}.hh",
        ],
        "allowed_headers": [
            "ostream",
            "iostream",
            "memory",
            "cassert",
            f"int_{prefix}.hh",
            f"generic_{prefix}.hxx",
            f"generic_{prefix}.hh",
            "stdexcept",
            "utility",
            "initializer_list",
        ],
        "extra_forbidden": NO_NEW_DELETE,
    }


EXERCISES = {
    # ---- cpp_1 ----
    "cpp_1/hello_friends": {
        "files": ["hello_friends.cc"],
        "allowed_headers": ["iostream"],
        "extra_forbidden": [],
    },
    "cpp_1/queue": _container("queue"),
    "cpp_1/timer": {
        "files": [
            "auto_timer.cc",
            "auto_timer.hh",
            "time_it.cc",
            "time_it.hh",
            "timer.cc",
            "timer.hh",
            "timer_exception.cc",
            "timer_exception.hh",
        ],
        "allowed_headers": [
            "iostream",
            "exception",
            "string",
            "optional",
            "functional",
            "yakatime/yakatime.hh",
            "timer.hh",
            "timer_exception.hh",
            "auto_timer.hh",
            "time_it.hh",
        ],
        "extra_forbidden": [],
    },
    # ---- cpp_2 ----
    "cpp_2/hola_amigos": {
        "files": ["hola_amigos.cc"],
        "allowed_headers": ["iostream"],
        "extra_forbidden": [],
    },
    "cpp_2/stack": _container("stack"),
    "cpp_2/war": {
        "files": [
            "assassin.cc",
            "assassin.hh",
            "knight.cc",
            "knight.hh",
            "regiment.cc",
            "regiment.hh",
            "soldier.cc",
            "soldier.hh",
        ],
        "allowed_headers": [
            "functional",
            "iostream",
            "string",
            "vector",
            "assassin.hh",
            "knight.hh",
            "regiment.hh",
            "soldier.hh",
            "ostream",
        ],
        "extra_forbidden": NO_NEW_DELETE,
    },
}

# Forbidden everywhere: C-style I/O, C memory management, C idioms.
GLOBAL_FORBIDDEN = {
    r"\b(printf|fprintf|sprintf|snprintf|puts|fputs|putchar|scanf)\s*\(":
        "C-style I/O (use streams)",
    r"\b(malloc|calloc|realloc|free)\s*\(": "C memory management",
    r"\bNULL\b": "NULL (use nullptr)",
    r"\busing\s+namespace\b": "'using namespace'",
    r"\bgoto\b": "goto",
    r"\bexit\s*\(": "exit() (return from main instead)",
}
