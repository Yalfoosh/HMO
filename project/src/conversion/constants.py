import re

WHITESPACE_PATTERN = r"\s+"
WHITESPACE_REGEX = re.compile(WHITESPACE_PATTERN)

COLUMN_SEPARATOR_PATTERN = r"\s{2,}"
COLUMN_SEPARATOR_REGEX = re.compile(COLUMN_SEPARATOR_PATTERN)
