# -*- coding: utf-8 -*-
"""
.. _Sass Reference:
    http://sass-lang.com/documentation/file.SASS_REFERENCE.html#import

Parser
======

Parser is in charge to find every ``@import`` rules in given Sass content.

It has been built following `Sass Reference`_ about ``@import`` rule.

Note:
    Sass indented syntax parser has a flaw which cause multiline comments are
    not catched. If you have commented ``@import`` in multiline comments they
    will be matched as true importations to resolve and inspect, it can leads
    to some errors.

    The only way is to not use multiline comments when you use the Sass index
    syntax.
"""
from __future__ import unicode_literals

import re

from six.moves import filter

from boussole.exceptions import InvalidImportRule


class ScssImportsParser(object):
    """
    SCSS parser to find ``@import`` rules.

    This does not support the old Sass syntax (also known as "indented
    syntax").

    It's a mixin, meaning without own ``__init__`` method so it's should be
    safe enough to inherit it from another class.

    Attributes:
        REGEX_IMPORT_RULE: Compiled regex used to find ``@import`` rules.
        REGEX_COMMENTS: Compiled regex used to find and remove comments.
    """
    syntax = "scss"
    REGEX_IMPORT_RULE = re.compile(r'@import\s*(url)?\s*\(?([^;]+?)\)?;',
                                   re.IGNORECASE)
    # Second part (for singleline comment) contain a negative lookbehind
    # assertion to avoid to match on url protocole (http://) which cause issues
    # in parsing
    REGEX_COMMENTS = re.compile(r'(/\*.*?\*/)|((?<!(:))//.*?(\n|$))',
                                re.IGNORECASE | re.DOTALL)

    def strip_quotes(self, content):
        """
        Unquote given rule.

        Args:
            content (str): An import rule.

        Raises:
            InvalidImportRule: Raise exception if the rule is badly quoted
            (not started or not ended quotes).

        Returns:
            string: The given rule unquoted.
        """
        error_msg = "Following rule is badly quoted: {}"
        if (content.startswith('"') and content.endswith('"')) or \
           (content.startswith("'") and content.endswith("'")):
            return content[1:-1]
        # Quote starting but not ended
        elif (content.startswith('"') and not content.endswith('"')) or \
             (content.startswith("'") and not content.endswith("'")):
            raise InvalidImportRule(error_msg.format(content))
        # Quote ending but not started
        elif (not content.startswith('"') and content.endswith('"')) or \
             (not content.startswith("'") and content.endswith("'")):
            raise InvalidImportRule(error_msg.format(content))

        return content

    def remove_comments(self, content):
        """
        Remove all comment kind (inline and multiline) from given content.

        Args:
            content (str): A SCSS source.

        Returns:
            string: Given SCSS source with all comments removed.
        """
        return self.REGEX_COMMENTS.sub("", content)

    def filter_rules(self, path):
        """
        Lambda to filter items that:
        * Starts with http:// or https:// (this for external load only)
        * Ends with ".css" (they are not intended to be compiled)
        """
        return not(path.startswith('http://') or
                   path.startswith('https://') or path.endswith('.css'))

    def flatten_rules(self, declarations):
        """
        Flatten returned import rules from regex.

        Because import rules can contains multiple items in the same rule
        (called multiline import rule), the regex ``REGEX_IMPORT_RULE``
        return a list of unquoted items for each rule.

        Args:
            declarations (list): A SCSS source.

        Returns:
            list: Given SCSS source with all comments removed.
        """
        rules = []

        for protocole, paths in declarations:
            # If there is a protocole (like 'url), drop it
            if protocole:
                continue
            # Unquote and possibly split multiple rule in the same declaration
            rules.extend([self.strip_quotes(v.strip())
                          for v in paths.split(',')])

        return list(filter(self.filter_rules, rules))

    def parse(self, content):
        """
        Parse a stylesheet document with a regex (``REGEX_IMPORT_RULE``)
        to extract all import rules and return them.

        Args:
            content (str): A SCSS source.

        Returns:
            list: Finded paths in import rules.
        """
        # Remove all comments before searching for import rules, to not catch
        # commented breaked import rules
        declarations = self.REGEX_IMPORT_RULE.findall(
            self.remove_comments(content)
        )
        return self.flatten_rules(declarations)


class SassImportsParser(ScssImportsParser):
    """
    Sass indented syntax parser to find ``@import`` rules.

    Multiline comments are not supported, it is actually too difficult to
    manage since they don't have a closing pattern ``*/`` and depend only
    on indentation continuation.

    Attributes:
        REGEX_IMPORT_RULE: Compiled regex used to find ``@import`` rules.
    """
    syntax = "sass"
    REGEX_IMPORT_RULE = re.compile(r'@import\s*(url)?\s*\(?([^;]+?)\)?(?:\n|$)',
                                   re.IGNORECASE)
