from conftest import ROOT
from greeter_suite import GreeterSuite


class TestHelloFriends(GreeterSuite):
    SRC = ROOT / "cpp_1" / "hello_friends" / "hello_friends.cc"
    GREETING = "Hello"
    NONE_MSG = "No friends provided..."
