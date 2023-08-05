LATEST = r"Latest\n-+\n"

LATEST_TEXT = rf"""
            {LATEST}    # Check the latest pattern
            (                   # Capture group 1
                [\s\S]*             # Match any character 0 or more times
            )"""

VERSION = r"""
    (\d+)   # Group 1: Digit (Major) positive number of times
    \.      # literal .
    (\d+)   # Group 2: Digit (Minor) positive number of times
    \.      # literal .
    (\d+)   # Group 3: Digit (Patch) positive number of times
    \n      # newline
    -+"""

CHANGE_LEVEL = r"""
    \*                  # Assert a literal *
    [                   # Create a character class
        \s                 # Assert a whitespace character
        \w                 # Assert a word character
    ]+                  # Close the character class and repeat it one or more times
    :                   # Assert a literal :
    """

CHANGE = rf"""
    ^                       # Assert start of string
    (                       # Capture group 1
        {CHANGE_LEVEL}          # Check the change level pattern
    )                       # End of capture group 1

    (                       # Capture group 2
        [\s\S]*?                # Match any character 0 or more times, non-greedy - "Do not iterate any more than is absolutely necessary"
        (?=                     # Positive lookahead
            ^{CHANGE_LEVEL}          # Check the change level pattern
            |                       # OR
            \Z                      # Assert end of string
        )                       # End of positive lookahead
    )                       # End of capture group 2
    """
