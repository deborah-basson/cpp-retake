"""General coding-style checks, applied to every submitted C++ file."""

import re

import pytest
from conftest import (
    ROOT,
    run,
    strip_comments_and_strings,
    submitted_sources,
)
from exercises import EXERCISES, GLOBAL_FORBIDDEN

MAX_COLUMNS = 80
SOURCES = submitted_sources()
IDS = [f"{ex}/{p.name}" for ex, p in SOURCES]

params = pytest.mark.parametrize("ex,path", SOURCES, ids=IDS)


def read(path):
    return path.read_bytes().decode("utf-8")


@params
def test_clang_format(ex, path):
    res = run(["clang-format", "--style=file", str(path)], text=True)
    assert res.returncode == 0, res.stderr
    original = read(path)
    if res.stdout != original:
        diff = run(
            ["diff", "-u", str(path), "-"], input=res.stdout, text=True
        ).stdout
        pytest.fail(f"Not clang-formatted. Run: clang-format -i {path}\n{diff}")


@params
def test_filename(ex, path):
    assert re.fullmatch(r"[a-z][a-z0-9_]*\.(cc|hh|hxx)", path.name), (
        "File names must be snake_case with .cc/.hh/.hxx extension"
    )


@params
def test_whitespace(ex, path):
    raw = path.read_bytes()
    assert b"\r" not in raw, "CRLF line endings"
    assert b"\t" not in raw, "Tabulation found (use spaces)"
    assert raw.endswith(b"\n"), "File must end with a newline"
    assert not raw.endswith(b"\n\n"), "Trailing empty lines at end of file"
    assert not raw.startswith(b"\n"), "Leading empty line"
    bad = [
        i + 1
        for i, line in enumerate(read(path).split("\n"))
        if line != line.rstrip()
    ]
    assert not bad, f"Trailing whitespace on lines {bad}"


@params
def test_line_length(ex, path):
    too_long = [
        (i + 1, len(line))
        for i, line in enumerate(read(path).split("\n"))
        if len(line) > MAX_COLUMNS
    ]
    assert not too_long, f"Lines > {MAX_COLUMNS} columns (line, len): {too_long}"


@params
def test_pragma_once(ex, path):
    if path.suffix not in (".hh", ".hxx"):
        pytest.skip("not a header")
    code = strip_comments_and_strings(read(path))
    first = next((ln.strip() for ln in code.split("\n") if ln.strip()), "")
    assert first == "#pragma once", "Headers must start with '#pragma once'"
    assert not re.search(r"#\s*(ifndef|define)\s+\w+_(HH|HXX|H)\b", code), (
        "Use '#pragma once', not include guards"
    )


@params
def test_hxx_included_at_end_of_hh(ex, path):
    if path.suffix != ".hxx":
        pytest.skip("not a .hxx")
    hh = path.with_suffix(".hh")
    assert hh.exists(), f"{path.name} has no matching {hh.name}"
    lines = [
        ln.strip()
        for ln in strip_comments_and_strings(read(hh), True).split("\n")
        if ln.strip()
    ]
    assert lines and lines[-1] == f'#include "{path.name}"', (
        f'{hh.name} must end with #include "{path.name}"'
    )


@params
def test_authorized_headers(ex, path):
    allowed = set(EXERCISES[ex]["allowed_headers"])
    code = strip_comments_and_strings(read(path), keep_strings=True)
    includes = re.findall(r'^\s*#\s*include\s*[<"]([^>"]+)[>"]', code, re.M)
    forbidden = sorted(h for h in includes if h not in allowed)
    assert not forbidden, f"Unauthorized headers: {forbidden}"


@params
def test_no_c_style_includes(ex, path):
    code = strip_comments_and_strings(read(path))
    c_headers = re.findall(r'#\s*include\s*<(\w+)\.h>', code)
    assert not c_headers, f"C headers (use <cxxx>): {c_headers}"


@params
def test_forbidden_constructs(ex, path):
    code = strip_comments_and_strings(read(path))
    rules = dict(GLOBAL_FORBIDDEN)
    rules.update({p: p for p in EXERCISES[ex]["extra_forbidden"]})
    found = []
    for pattern, label in rules.items():
        for m in re.finditer(pattern, code):
            line = code.count("\n", 0, m.start()) + 1
            found.append(f"line {line}: {label}")
    assert not found, "Forbidden constructs:\n" + "\n".join(found)


@params
def test_no_define_constants(ex, path):
    code = strip_comments_and_strings(read(path))
    defines = re.findall(r"^\s*#\s*define\s+(\w+)", code, re.M)
    assert not defines, f"Use constexpr instead of #define: {defines}"


@params
def test_clang_tidy(ex, path):
    flags = ["-std=c++20", f"-I{ROOT / ex}"]
    if path.suffix in (".hh", ".hxx"):
        flags = ["-x", "c++-header", *flags, "-Wno-pragma-once-outside-header"]
    res = run(
        ["clang-tidy", "--quiet", str(path), "--", *flags],
        text=True,
        timeout=120,
    )
    assert res.returncode == 0, f"clang-tidy:\n{res.stdout}\n{res.stderr}"
