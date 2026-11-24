"""python -m mathspeech "x^2 + 3x - 5 = 0" """
import sys

from .core import speak


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print('usage: python -m mathspeech "EXPRESSION" ...', file=sys.stderr)
        return 2
    try:
        for a in args:
            print(speak(a))
    except ValueError as e:
        print(f"Cannot read that: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
