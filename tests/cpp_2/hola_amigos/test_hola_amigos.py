from conftest import ROOT
from greeter_suite import GreeterSuite


class TestHolaAmigos(GreeterSuite):
    SRC = ROOT / "cpp_2" / "hola_amigos" / "hola_amigos.cc"
    GREETING = "Hola"
    NONE_MSG = "No amigos provided..."
