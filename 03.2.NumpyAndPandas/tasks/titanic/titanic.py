import typing as tp

import pandas as pd


def male_age(df: pd.DataFrame) -> float:
    """
    Return mean age of survived men, embarked in Southampton with fare > 30
    :param df: dataframe
    :return: mean age
    """
    return df[(df['Fare'] > 30) & (df['Sex'] == 'male') & (df['Survived'] == 1) & (df['Embarked'] == 'S')]['Age'].mean()


def nan_columns(df: pd.DataFrame) -> tp.Iterable[str]:
    """
    Return list of columns containing nans
    :param df: dataframe
    :return: series of columns
    """
    return df.columns[df.isna().any()]


def class_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Return Pclass distrubution
    :param df: dataframe
    :return: series with ratios
    """
    return df['Pclass'].value_counts(normalize=True)


def families_count(df: pd.DataFrame, k: int) -> int:
    """
    Compute number of families with more than k members
    :param df: dataframe,
    :param k: number of members,
    :return: number of families
    """
    df['Family'] = df['Name'].str.split(', ').str[0]
    df = df.groupby(['Family']).size().reset_index()

    return df[df[0] > k].shape[0]


def mean_price(df: pd.DataFrame, tickets: tp.Iterable[str]) -> float:
    """
    Return mean price for specific tickets list
    :param df: dataframe,
    :param tickets: list of tickets,
    :return: mean fare for this tickets
    """
    return df[df["Ticket"].isin(tickets)]["Fare"].mean()


def max_size_group(df: pd.DataFrame, columns: list[str]) -> tp.Iterable[tp.Any]:
    """
    For given set of columns compute most common combination of values of these columns
    :param df: dataframe,
    :param columns: columns for grouping,
    :return: list of most common combination
    """
    return df.groupby(columns).size().idxmax()


def dead_lucky(df: pd.DataFrame) -> float:
    """
    Compute dead ratio of passengers with lucky tickets.
    A ticket is considered lucky when it contains an even number of digits in it
    and the sum of the first half of digits equals the sum of the second part of digits
    ex:
    lucky: 123222, 2671, 935755
    not lucky: 123456, 62869, 568290
    :param df: dataframe,
    :return: ratio of dead lucky passengers
    """
    df["Lucky"] = df["Ticket"].apply(_is_lucky)
    return df[(df["Lucky"]) & (df["Survived"] == 0)].size / df[(df["Lucky"])].size


def _is_lucky(ticket: str) -> bool:
    sz = len(ticket)
    if not ticket.isnumeric() or sz % 2 != 0:
        return False

    return _sum(ticket[:sz // 2]) == _sum(ticket[sz // 2:])


def _sum(ticket: str) -> int:
    return sum([int(digit) for digit in ticket])
