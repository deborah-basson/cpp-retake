"""Targeted tests for timer.

Most tests build against a fake yakatime (virtual clock: sleep_for advances
time instantly) so outputs are exact and tests are fast. One test uses the
real yakatime header to check compatibility.
"""

import shutil
import textwrap

import pytest
from conftest import ROOT, compile_cxx, require_tool, run

TIMER = ROOT / "timer"
SOURCES = ["timer.cc", "timer_exception.cc", "auto_timer.cc", "time_it.cc"]
SAN = ["-g", "-fsanitize=address,undefined", "-fno-sanitize-recover=all"]

pytestmark = pytest.mark.skipif(
    not all((TIMER / s).exists() for s in SOURCES), reason="not implemented yet"
)

FAKE_YAKATIME = """
#pragma once

namespace yakatime
{
    inline double fake_now = 0.0;

    class TimePoint
    {
    public:
        TimePoint() = default;
        TimePoint(double t)
            : t_(t)
        {}

        double operator-(const TimePoint& other)
        {
            return t_ - other.t_;
        }

    private:
        double t_ = 0.0;
    };

    inline TimePoint now()
    {
        return fake_now;
    }

    inline void sleep_for(double x)
    {
        fake_now += x;
    }
} // namespace yakatime
"""

PART1 = """
#include "timer.hh"

#include <cmath>
#include <iostream>

int main()
{
    auto t = Timer{};
    t.start();
    yakatime::sleep_for(1.5);
    t.pause();
    yakatime::sleep_for(1.0);
    t.resume();
    yakatime::sleep_for(2.0);
    t.pause();
    if (std::abs(t.elapsed() - 3.5f) < 0.001)
        std::cout << "Elapsed time is approximately 3.5!!\\n";
    else
        std::cerr << "Error, elapsed time is incorrect.\\n";
    t.reset();
    double duration = t.elapsed();
    std::cout << "Elapsed time after reset: " << duration << " seconds.\\n";
    return 0;
}
"""
PART1_OUT = (
    "Elapsed time is approximately 3.5!!\n"
    "Elapsed time after reset: 0 seconds.\n"
)

PART2 = """
#include <iostream>

#include "timer.hh"
#include "timer_exception.hh"

int main()
{
    auto t = Timer{};
    try
    {
        t.pause();
    }
    catch (const TimerException& e)
    {
        std::cout << "Error: " << e.what() << "\\n";
    }
}
"""
PART2_OUT = "Error: Cannot pause: Timer is not running.\n"

PART3 = """
#include <iostream>

#include "auto_timer.hh"

int main()
{
    Timer mytimer;
    {
        auto _1 = AutoTimer{"Job A", mytimer};
        yakatime::sleep_for(2.5);
    }
    {
        auto _2 = AutoTimer{"Job B"};
        yakatime::sleep_for(3);
    }
    {
        auto _3 = AutoTimer{"Job C", mytimer};
        yakatime::sleep_for(4.5);
    }
    std::cout << "Job A&C completed in " << mytimer.elapsed() << " seconds.\\n";
}
"""
PART3_OUT = (
    "Job A took 2.5 seconds.\n"
    "Job B took 3 seconds.\n"
    "Job C took 4.5 seconds.\n"
    "Job A&C completed in 7 seconds.\n"
)

PART4 = """
#include <stdexcept>

#include "time_it.hh"
#include "yakatime/yakatime.hh"

void job_1()
{
    yakatime::sleep_for(1.2);
}

void raising_job()
{
    yakatime::sleep_for(0.5);
    throw std::runtime_error("Bang!");
    yakatime::sleep_for(1.0);
}

int main()
{
    time_it(job_1);
    time_it([]() { yakatime::sleep_for(2.3); });
    time_it(raising_job);
}
"""
PART4_OUT = (
    "Function terminated successfully in 1.2 seconds.\n"
    "Function terminated successfully in 2.3 seconds.\n"
    "Function terminated with an error in 0.5 seconds.\n"
)

ERRORS = """
#include <iostream>
#include <type_traits>

#include "timer.hh"
#include "timer_exception.hh"

static_assert(std::is_base_of_v<std::exception, TimerException>);

template <typename F>
void expect(F f)
{
    try
    {
        f();
        std::cout << "no throw\\n";
    }
    catch (const std::exception& e)
    {
        std::cout << e.what() << "\\n";
    }
}

int main()
{
    auto t = Timer{};
    expect([&] { t.pause(); });
    expect([&] { t.resume(); });
    expect([&] { std::cout << t.elapsed() << " "; });
    t.start();
    expect([&] { t.start(); });
    expect([&] { t.resume(); });
    expect([&] { t.elapsed(); });
    t.pause();
    expect([&] { t.start(); });
    expect([&] { t.pause(); });
    t.resume();
    expect([&] { t.reset(); });
    expect([&] { t.resume(); });
    expect([&] { t.start(); });
}
"""
ERRORS_OUT = (
    "Cannot pause: Timer is not running.\n"
    "Cannot resume: Timer is at zero.\n"
    "0 no throw\n"
    "Cannot start: Timer is running.\n"
    "Cannot resume: Timer is running.\n"
    "Cannot elapsed: Timer is running.\n"
    "Cannot start: Timer is not at zero.\n"
    "Cannot pause: Timer is not running.\n"
    "no throw\n"
    "Cannot resume: Timer is at zero.\n"
    "no throw\n"
)

BEHAVIOUR = """
#include <functional>
#include <iostream>

#include "auto_timer.hh"
#include "time_it.hh"
#include "timer.hh"

void const_elapsed(const Timer& t)
{
    std::cout << "const elapsed " << t.elapsed() << "\\n";
}

int main()
{
    auto t = Timer{};
    for (int i = 0; i < 3; ++i)
    {
        if (i == 0)
            t.start();
        else
            t.resume();
        yakatime::sleep_for(1.0);
        t.pause();
        yakatime::sleep_for(10.0);
    }
    const_elapsed(t);

    t.resume();
    yakatime::sleep_for(5.0);
    t.reset();
    t.start();
    yakatime::sleep_for(0.25);
    t.pause();
    std::cout << "after reset " << t.elapsed() << "\\n";

    try
    {
        auto guard = AutoTimer{"Throwing job"};
        yakatime::sleep_for(0.75);
        throw 42;
    }
    catch (int)
    {
        std::cout << "caught\\n";
    }

    time_it([] { throw 42; });
    std::function<void()> f = [] { yakatime::sleep_for(2.0); };
    time_it(f);
    std::cout << "time_it did not propagate\\n";

    auto z = Timer{};
    z.start();
    z.pause();
    z.resume();
    z.pause();
    std::cout << "zero-length run " << z.elapsed() << "\\n";
}
"""
BEHAVIOUR_OUT = (
    "const elapsed 3\n"
    "after reset 0.25\n"
    "Throwing job took 0.75 seconds.\n"
    "caught\n"
    "Function terminated with an error in 0 seconds.\n"
    "Function terminated successfully in 2 seconds.\n"
    "time_it did not propagate\n"
    "zero-length run 0\n"
)

PROGRAMS = {
    "part1": (PART1, PART1_OUT),
    "part2": (PART2, PART2_OUT),
    "part3": (PART3, PART3_OUT),
    "part4": (PART4, PART4_OUT),
    "errors": (ERRORS, ERRORS_OUT),
    "behaviour": (BEHAVIOUR, BEHAVIOUR_OUT),
}


@pytest.fixture(scope="module")
def fake_timer_dir(tmp_path_factory):
    """Copy of the student sources with yakatime replaced by a fake clock."""
    d = tmp_path_factory.mktemp("timer_fake")
    for f in TIMER.iterdir():
        if f.is_file():
            shutil.copy(f, d / f.name)
    (d / "yakatime").mkdir()
    (d / "yakatime" / "yakatime.hh").write_text(textwrap.dedent(FAKE_YAKATIME))
    return d


def build(src_dir, out_dir, name, code, compiler="g++", extra=()):
    main = out_dir / f"{name}.cc"
    main.write_text(textwrap.dedent(code))
    sources = [src_dir / s for s in SOURCES] + [main]
    return compile_cxx(
        sources,
        out_dir / name,
        compiler=compiler,
        extra=extra,
        include=[src_dir],
    )


def run_exact(binary, expected, prefix=()):
    res = run([*prefix, str(binary)], text=True)
    assert res.returncode == 0, res.stderr
    assert res.stdout == expected
    assert res.stderr == ""


@pytest.mark.parametrize("compiler", ["g++", "clang++"])
def test_real_yakatime_part1(tmp_path, compiler):
    require_tool(compiler)
    run_exact(build(TIMER, tmp_path, "part1", PART1, compiler), PART1_OUT)


@pytest.mark.parametrize("name", PROGRAMS.keys())
@pytest.mark.parametrize("compiler", ["g++", "clang++"])
def test_fake_clock(fake_timer_dir, tmp_path, compiler, name):
    require_tool(compiler)
    code, out = PROGRAMS[name]
    run_exact(build(fake_timer_dir, tmp_path, name, code, compiler), out)


@pytest.mark.parametrize("name", PROGRAMS.keys())
def test_sanitizers(fake_timer_dir, tmp_path, name):
    code, out = PROGRAMS[name]
    run_exact(build(fake_timer_dir, tmp_path, name, code, extra=SAN), out)


@pytest.mark.parametrize("name", ["errors", "behaviour"])
def test_valgrind(fake_timer_dir, tmp_path, name):
    require_tool("valgrind")
    code, out = PROGRAMS[name]
    binary = build(fake_timer_dir, tmp_path, name, code)
    prefix = ["valgrind", "-q", "--error-exitcode=42", "--leak-check=full"]
    run_exact(binary, out, prefix)