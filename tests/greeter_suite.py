"""Shared tests for the greeter exercises (hello_friends, hola_amigos).

Subclass GreeterSuite in a Test* class and set SRC, GREETING, NONE_MSG.
"""

import re

import pytest
from conftest import compile_cxx, require_tool, run, strip_comments_and_strings

CASES = {
    "subject_example": ["Alice", "Bob", "Charlie"],
    "single": ["Alice"],
    "empty_string": [""],
    "spaces_in_arg": ["Jean Pierre", "  lead", "trail  "],
    "utf8": ["Zoé", "Ünïcödé", "日本"],
    "format_specifiers": ["%s%d%n", "%%", "{}"],
    "dash_args": ["-n", "--help", "-"],
    "special_chars": ["a\tb", "back\\slash", "$HOME", "*"],
    "duplicates": ["Bob", "Bob", "Bob"],
    "many": [f"f{i}" for i in range(5000)],
    "huge_arg": ["x" * 100_000],
}


class GreeterSuite:
    SRC = None
    GREETING = None
    NONE_MSG = None

    @pytest.fixture(autouse=True)
    def _require_src(self):
        if not self.SRC.exists():
            pytest.skip(f"{self.SRC.name} not implemented yet")

    @pytest.fixture(scope="class")
    @classmethod
    def binary(cls, tmp_path_factory):
        if not cls.SRC.exists():
            pytest.skip("not implemented yet")
        out = tmp_path_factory.mktemp(cls.SRC.stem) / cls.SRC.stem
        return compile_cxx([cls.SRC], out)

    @pytest.fixture(scope="class")
    @classmethod
    def binary_sanitized(cls, tmp_path_factory):
        if not cls.SRC.exists():
            pytest.skip("not implemented yet")
        out = tmp_path_factory.mktemp(cls.SRC.stem + "_san") / cls.SRC.stem
        return compile_cxx(
            [cls.SRC],
            out,
            extra=[
                "-g",
                "-fsanitize=address,undefined",
                "-fno-sanitize-recover=all",
            ],
        )

    def expected(self, args):
        return "".join(f"{self.GREETING} {a}!\n" for a in args)

    def check(self, bin_path, args, prefix=()):
        res = run([*prefix, str(bin_path), *args])
        out = res.stdout.decode("utf-8")
        if args:
            assert res.returncode == 0, f"exit code {res.returncode}, expected 0"
            assert out == self.expected(args)
        else:
            assert res.returncode == 1, f"exit code {res.returncode}, expected 1"
            assert out == self.NONE_MSG + "\n"
        assert res.stderr == b"", f"unexpected stderr: {res.stderr[:200]!r}"

    # --- Compilation -----------------------------------------------------

    @pytest.mark.parametrize("compiler", ["g++", "clang++"])
    def test_compiles(self, compiler, tmp_path):
        require_tool(compiler)
        compile_cxx([self.SRC], tmp_path / "a.out", compiler=compiler)

    # --- Behaviour -------------------------------------------------------

    def test_no_args(self, binary):
        self.check(binary, [])

    @pytest.mark.parametrize("args", CASES.values(), ids=CASES.keys())
    def test_args(self, binary, args):
        self.check(binary, args)

    def test_subject_output_exact(self, binary):
        res = run([str(binary), "Alice", "Bob", "Charlie"])
        g = self.GREETING
        assert res.stdout == (
            f"{g} Alice!\n{g} Bob!\n{g} Charlie!\n".encode()
        )

    def test_no_args_on_stdout_not_stderr(self, binary):
        res = run([str(binary)])
        assert res.stdout == (self.NONE_MSG + "\n").encode()
        assert res.stderr == b""

    def test_output_through_pipe(self, binary):
        res = run(["sh", "-c", f"'{binary}' A B | cat"])
        g = self.GREETING
        assert res.stdout == f"{g} A!\n{g} B!\n".encode()

    # --- Memory / UB -----------------------------------------------------

    @pytest.mark.parametrize(
        "args",
        [[], ["Alice", "Bob"], CASES["many"]],
        ids=["none", "two", "many"],
    )
    def test_sanitizers(self, binary_sanitized, args):
        self.check(binary_sanitized, args)

    @pytest.mark.parametrize("args", [[], ["Alice", "Bob"]], ids=["none", "two"])
    def test_valgrind(self, binary, args):
        require_tool("valgrind")
        prefix = ["valgrind", "-q", "--error-exitcode=42", "--leak-check=full"]
        self.check(binary, args, prefix=prefix)

    # --- Source constraints ----------------------------------------------

    def test_uses_cpp_streams(self):
        code = strip_comments_and_strings(self.SRC.read_text())
        assert re.search(r"\bstd::cout\b", code), "Must print with std::cout"
        assert not re.search(r"\b(write|fwrite)\s*\(", code), "C-style write"

    def test_has_main(self):
        code = strip_comments_and_strings(self.SRC.read_text())
        assert re.search(r"\bint\s+main\s*\(", code), "Main function required"
