"""Turn a plain-text maths expression into words a narrator can read aloud."""
from __future__ import annotations

import re

_TOKEN = re.compile(
    r"\s*(<=|>=|!=|\d+(?:\.\d+)?|sqrt|pi|[A-Za-z]|[-+*/()^=<>%°])"
)

_BINARY = {
    "+": "plus",
    "-": "minus",
    "*": "times",
    "/": "over",
    "=": "equals",
    "<": "is less than",
    ">": "is greater than",
    "<=": "is less than or equal to",
    ">=": "is greater than or equal to",
    "!=": "is not equal to",
}
_ORDINAL_POWER = {"2": "squared", "3": "cubed"}


def tokenise(text: str) -> list[str]:
    toks, pos, text = [], 0, text.strip()
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m:
            raise ValueError(f"cannot read {text[pos:]!r}")
        toks.append(m.group(1))
        pos = m.end()
    return toks


def _number(t: str) -> str:
    return t.replace(".", " point ")


def speak(text: str) -> str:
    toks = tokenise(text)
    out: list[str] = []
    i = 0
    prev_operand = False  # True if the previous token ends an operand
    sqrt_stack: list[int] = []  # bracket depth where a sqrt( opened
    depth = 0
    while i < len(toks):
        t = toks[i]
        if t == "^":
            nxt = toks[i + 1] if i + 1 < len(toks) else None
            if nxt is None:
                raise ValueError("^ needs an exponent")
            if nxt in _ORDINAL_POWER:
                out.append(_ORDINAL_POWER[nxt])
                i += 2
            elif nxt == "(":
                out.append("to the power of")
                i += 1
            elif nxt == "-":
                if i + 2 >= len(toks):
                    raise ValueError("^ needs an exponent")
                out.append("to the power of negative " + _number(toks[i + 2]))
                i += 3
            else:
                out.append("to the power of " + _number(nxt))
                i += 2
            prev_operand = True
            continue
        if t == "sqrt":
            if i + 1 >= len(toks) or toks[i + 1] != "(":
                raise ValueError("sqrt needs brackets, for example sqrt(x+1)")
            out.append("the square root of")
            depth += 1
            sqrt_stack.append(depth)
            # a simple inner (one token) is read without brackets
            if i + 3 < len(toks) and toks[i + 3] == ")":
                out.append(_number(toks[i + 2]) if toks[i + 2][0].isdigit() else toks[i + 2])
                depth -= 1
                sqrt_stack.pop()
                i += 4
                prev_operand = True
                continue
            i += 2
            prev_operand = False
            continue
        if t == "(":
            depth += 1
            out.append("open bracket")
            prev_operand = False
        elif t == ")":
            if depth == 0:
                raise ValueError("unmatched )")
            if sqrt_stack and sqrt_stack[-1] == depth:
                sqrt_stack.pop()
                out.append("end root")
            else:
                out.append("close bracket")
            depth -= 1
            prev_operand = True
        elif t in ("-", "+") and not prev_operand:
            out.append("negative" if t == "-" else "positive")
        elif t in _BINARY:
            out.append(_BINARY[t])
            prev_operand = False
        elif t == "%":
            out.append("percent")
            prev_operand = True
        elif t == "°":
            out.append("degrees")
            prev_operand = True
        elif t[0].isdigit():
            out.append(_number(t))
            prev_operand = True
        else:  # letters, pi
            out.append(t)
            prev_operand = True
        i += 1
    if depth:
        raise ValueError("missing )")
    return " ".join(out)
