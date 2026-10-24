# Sources for the practice example

These sources explain API behavior and input semantics.
They do not establish a novel research question or a literature review.
Only the listed sections were inspected on 2026-10-23.

| ID | Source and location | Reading depth | Use and limit |
| --- | --- | --- | --- |
| P001 | [Python 3.14, math.fsum](https://docs.python.org/3.14/library/math.html#math.fsum) | The complete function entry, including its rounding caveat. | Defines the comparison method. It does not guarantee exact sums on every platform. |
| P002 | [Python 3.14, Fraction](https://docs.python.org/3.14/library/fractions.html#fractions.Fraction) and [from_float](https://docs.python.org/3.14/library/fractions.html#fractions.Fraction.from_float) | Constructor semantics, float examples, and the complete from_float entry. | Defines the exact rational value of the binary float input. Decimal strings represent different input semantics. |

The online pages identified themselves as Python 3.14.9 documentation when inspected.
The experiment log records the actual interpreter version separately.
The complete manuals and CPython implementation were not reviewed.
No paper, private library, or downloaded dataset is part of this exercise.
The method choice is retrospective because the coordinator already knew these APIs.
The experiment tests only the fixed cases and does not establish a new general algorithm claim.
