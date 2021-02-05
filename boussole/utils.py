# -*- coding: utf-8 -*-
"""
Utils
=====

"""
from pathlib import PureWindowsPath, PurePosixPath


def match_path(path, included_patterns, excluded_patterns, case_sensitive):
    """
    Matches a pathname against a set of acceptable and ignored patterns.

    Inspired from ``watchdog.utils.patterns_match_path`` which was inspired from
    deprecated ``pathtools.patterns.match_path``.

    Arguments:
        path (string): A pathname which will be matched against a pattern.
        included_patterns (set): Allow filenames matching wildcard patterns
            specified in this list. If no pattern is specified, the function
            treats the pathname as a match_path.
        excluded_patterns (set): Ignores filenames matching wildcard patterns
            specified in this list. If no pattern is specified, the function
            treats the pathname as a match_path.
        case_sensitive (boolean): ``True`` if matching should be
            case-sensitive; ``False`` otherwise.

    Raises:
        ValueError: if included patterns and excluded patterns contain the
            same pattern.
    Returns:
        boolean: ``True`` if the pathname matches; ``False`` otherwise.
    """
    if case_sensitive:
        path = PurePosixPath(path)
    else:
        included_patterns = {pattern.lower() for pattern in included_patterns}
        excluded_patterns = {pattern.lower() for pattern in excluded_patterns}
        path = PureWindowsPath(path)

    common_patterns = included_patterns & excluded_patterns

    if common_patterns:
        msg = "conflicting patterns '{}' included and excluded"
        raise ValueError(msg.format(common_patterns))

    return (
        any(path.match(p) for p in included_patterns) and
        not any(path.match(p) for p in excluded_patterns)
    )
