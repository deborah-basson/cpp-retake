import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from exercises import CXXFLAGS, EXERCISES  # noqa: E402

SOURCE_SUFFIXES = {".cc", ".hh", ".hxx"}


def submitted_sources():
    """(exercise, path) for every C++ file to submit that exists."""
    out = []
    for ex, cfg in EXERCISES.items():
        for name in cfg["files"]:
            path = ROOT / ex / name
            if path.suffix in SOURCE_SUFFIXES and path.exists():
                out.append((ex, path))
    return out


def strip_comments_and_strings(code, keep_strings=False):
    """Blank out comments (and literals unless keep_strings), keep layout."""
    pattern = re.compile(
        r'R"(?P<d>[^(\s]*)\(.*?\)(?P=d)"'
        r"|//[^\n]*"
        r"|/\*.*?\*/"
        r'|"(?:\\.|[^"\\\n])*"'
        r"|'(?:\\.|[^'\\\n])*'",
        re.DOTALL,
    )

    def blank(m):
        text = m.group(0)
        if keep_strings and not text.startswith(("//", "/*")):
            return text
        return re.sub(r"[^\n]", " ", text)

    return pattern.sub(blank, code)


def run(cmd, **kw):
    kw.setdefault("capture_output", True)
    kw.setdefault("timeout", 30)
    return subprocess.run(cmd, **kw)


def compile_cxx(sources, output, compiler="g++", extra=(), include=()):
    cmd = [compiler, *CXXFLAGS, *extra]
    cmd += [f"-I{d}" for d in include]
    cmd += [str(s) for s in sources] + ["-o", str(output)]
    res = run(cmd, timeout=120, text=True)
    assert res.returncode == 0, (
        f"Compilation failed:\n$ {' '.join(cmd)}\n{res.stderr}"
    )
    return output


def require_tool(name):
    if shutil.which(name) is None:
        pytest.skip(f"{name} not installed")
