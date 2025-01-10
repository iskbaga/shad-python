import os


def count_util(text: str, flags: str | None = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """
    sample = {'m', 'l', 'L', 'w'}
    real = sample
    if flags:
        real = sample.intersection(set(list(flags)))
    result = {}
    if 'm' in real:
        result["chars"] = len(text)
    if 'l' in real:
        result["lines"] = len([x for x in text if x == os.linesep])
    if 'L' in real:
        result["longest_line"] = len(max(text.split(sep=os.linesep), key=len))
    if 'w' in real:
        result['words'] = len([x for x in text.split()])
    return result
