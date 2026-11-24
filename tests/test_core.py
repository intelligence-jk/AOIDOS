import pytest

from mathspeech import speak
from mathspeech.__main__ import main


@pytest.mark.parametrize(
    "text,words",
    [
        ("x^2 + 3x - 5 = 0", "x squared plus 3 x minus 5 equals 0"),
        ("y = -2x + 1", "y equals negative 2 x plus 1"),
        ("a^3", "a cubed"),
        ("2^10", "2 to the power of 10"),
        ("x^-1", "x to the power of negative 1"),
        ("3/4", "3 over 4"),
        ("2.5 * 4", "2 point 5 times 4"),
        ("(x+1)(x-1)", "open bracket x plus 1 close bracket open bracket x minus 1 close bracket"),
        ("sqrt(2)", "the square root of 2"),
        ("sqrt(x+1)", "the square root of x plus 1 end root"),
        ("x <= 5", "x is less than or equal to 5"),
        ("30°", "30 degrees"),
        ("15%", "15 percent"),
        ("2*(-3)", "2 times open bracket negative 3 close bracket"),
        ("pi r^2", "pi r squared"),
        ("e^(2x)", "e to the power of open bracket 2 x close bracket"),
    ],
)
def test_speak(text, words):
    assert speak(text) == words


def test_no_symbols_left():
    out = speak("(a+b)^2 = a^2 + 2ab + b^2")
    assert not any(c in out for c in "+-*/^=()")


@pytest.mark.parametrize("bad", ["x^", "sqrt x", "(x+1", "x+1)", "x # 2"])
def test_errors(bad):
    with pytest.raises(ValueError):
        speak(bad)


def test_cli(capsys):
    assert main(["x^2=4"]) == 0
    assert capsys.readouterr().out.strip() == "x squared equals 4"
    assert main(["x^"]) == 1
