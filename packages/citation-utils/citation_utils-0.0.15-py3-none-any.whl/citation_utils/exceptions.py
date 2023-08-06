import re
from enum import Enum
from typing import Pattern


class CitationBasedStatutes(Enum):
    BAR = [
        803,
        1922,
        1645,
        850,
        287,
        1132,
        1755,
        1960,
        209,
        1153,
        411,
        356,
    ]
    ADMIN = [
        r"(?:\d{1,2}-){3}SC\b",
        r"99-10-05-0\b",
    ]

    @property
    def regex(self) -> str:
        return r"(?:" + "|".join(str(i) for i in self.value) + r")"

    @property
    def pattern(self) -> Pattern:
        return re.compile(self.regex)
