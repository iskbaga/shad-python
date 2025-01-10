def get_fizz_buzz(n: int) -> list[int | str]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    result: list[int | str] = list(range(0, n + 1))
    result[::3] = ['Fizz'] * (len(result[::3]))
    result[::5] = ['Buzz'] * (len(result[::5]))
    result[::15] = ['FizzBuzz'] * (len(result[::15]))
    return result[1:]
