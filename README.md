# CALLIOPE: named after the Muse of eloquence: maths read aloud

Formerly `maths-to-speech`.

Turn a plain-text maths expression into words a narrator or a text-to-speech voice can read.

## What it solves
A voice-over script that contains `x^2 + 3x - 5 = 0` is read badly, or not at all, by a voice tool. This turns it into `x squared plus 3 x minus 5 equals 0`, the same way a teacher would say it, so a narration script can be generated from the board lines. Pure Python 3.10+, standard library only.

## Example
```bash
python -m mathspeech "x^2 + 3x - 5 = 0" "sqrt(x+1)" "2^10" "y = -2x + 1"
```
```
x squared plus 3 x minus 5 equals 0
the square root of x plus 1 end root
2 to the power of 10
y equals negative 2 x plus 1
```

## The maths behind it
The only real decision is whether `-` is a subtraction or a sign. A minus is a sign ("negative") when nothing that ends an operand comes before it (the start of the line, an operator, an opening bracket); otherwise it is "minus". So `a - b` is "a minus b" and `2*(-3)` is "2 times open bracket negative 3 close bracket". Powers 2 and 3 are "squared" and "cubed", other powers are "to the power of n", and a negative power is "to the power of negative n". Decimals are spoken digit by digit after the point ("2.5" becomes "2 point 5"). Brackets inside a square root end with "end root" so the listener knows where the root stops; a bare number or letter needs no marker. The grammar is small on purpose: if something cannot be read, the tool says so instead of guessing.

## Install and run
```bash
python -m pip install -e .
python -m mathspeech "x^2 = 4"
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
