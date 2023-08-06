import re

LEGACY_PREFIXED = r"""
    ^ # start
    (?:
        (?:
            No # shorthand for number
            s? # plural option
            \. # period
            \s+ # space/s
        )? # number
        (?:
            (?:
                L
                \s* # L-26353
                -? # L 12271
                \s* # L- 59592
            )|
            (?:
                I\s- # I -5458
            )|
            (?:
                I- # I-19555
            )|
            (?:
                I\.- # I.-12735
            )
        )
    )
    (?=\w+) # excluded alphanumeric character
"""

LEGACY_PREFIXED_LOOKALIKE = r"""
    ^ # start
    (?:
        (?:
            No # shorthand for number
            s? # plural option
            \. # period
            \s+ # space/s
        )? # number
        (?:
            L
            \s* # L-26353
            -? # L 12271
            \s* # L- 59592
        )|
        (?:
            I\s- # I -5458
        )|
        (?:
            I- # I-19555
        )|
        (?:
            I\.- # I.-12735
        )
    )
    [ILl] # necessary after the group
    \s?
"""


def remove_prefix_regex(regex_to_match: str, text: str):
    """Based on the `regex` passed, remove this from the start of the `text`"""
    match = re.search(regex_to_match, text, re.VERBOSE)
    if not match:
        return None
    return text.strip().removeprefix(match.group())


def replace_prefix_regex(regex_to_match: str, text: str, std: str):
    """Based on the `regex` passed, replace this from the start of the `text` with a standardized variant `std`."""
    match = re.search(regex_to_match, text, re.VERBOSE)
    if not match:
        return None
    return std + text.strip().removeprefix(match.group()).strip()


def gr_prefix_clean(text: str):
    # deal with case like L-I9863
    if gr_text := replace_prefix_regex(LEGACY_PREFIXED_LOOKALIKE, text, "L-1"):
        return gr_text
    # deal with improper L- formatted cases
    elif gr_text := replace_prefix_regex(LEGACY_PREFIXED, text, "L-"):
        return gr_text
    return None
