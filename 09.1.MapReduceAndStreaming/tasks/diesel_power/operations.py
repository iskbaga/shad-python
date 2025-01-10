import heapq
import string
from abc import abstractmethod, ABC
import typing as tp
from collections import defaultdict
from itertools import groupby

TRow = dict[str, tp.Any]
TRowsIterable = tp.Iterable[TRow]
TRowsGenerator = tp.Generator[TRow, None, None]


class Operation(ABC):
    @abstractmethod
    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        pass


class Read(Operation):
    def __init__(self, filename: str, parser: tp.Callable[[str], TRow]) -> None:
        self.filename = filename
        self.parser = parser

    def __call__(self, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        with open(self.filename) as f:
            for line in f:
                yield self.parser(line)


class ReadIterFactory(Operation):
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        for row in kwargs[self.name]():
            yield row


# Operations


class Mapper(ABC):
    """Base class for mappers"""

    @abstractmethod
    def __call__(self, row: TRow) -> TRowsGenerator:
        """
        :param row: one table row
        """
        pass


class Map(Operation):
    def __init__(self, mapper: Mapper) -> None:
        self.mapper = mapper

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        for row in rows:
            yield from self.mapper(row)


class Reducer(ABC):
    """Base class for reducers"""

    @abstractmethod
    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        """
        :param rows: table rows
        """
        pass


class Reduce(Operation):
    def __init__(self, reducer: Reducer, keys: tp.Sequence[str]) -> None:
        self.reducer = reducer
        self.keys = keys

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        for _, grouped_rows in groupby(rows, key=lambda row: row[self.keys[0]]):
            yield from self.reducer(tuple(self.keys), grouped_rows)


def _left_join(rows_a: tp.Iterable[dict[str, tp.Any]], rows_b: tp.Sequence[dict[str, tp.Any]]) -> TRowsGenerator:
    for row in rows_a:
        if len(rows_b) == 0:
            yield row
        for row_b in rows_b:
            joined = row.copy()
            joined.update(row_b)
            yield joined


class Joiner(ABC):
    """Base class for joiners"""

    def __init__(self, suffix_a: str = '_1', suffix_b: str = '_2') -> None:
        self._a_suffix = suffix_a
        self._b_suffix = suffix_b

    @abstractmethod
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        """
        :param keys: join keys
        :param rows_a: left table rows
        :param rows_b: right table rows
        """
        pass


class Join(Operation):
    def __init__(self, joiner: Joiner, keys: tp.Sequence[str]):
        self.keys = keys
        self.joiner = joiner

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        empty: list[tp.Any] = []
        empty_iter: tp.Iterator[tp.Any] = iter(empty)

        groups_a: tp.Iterator[tuple[list[tp.Any], tp.Iterator[dict[str, tp.Any]]]] = groupby(rows,
                                                                                             lambda x: [x[i] for i in
                                                                                                        self.keys])
        groups_b: tp.Iterator[tuple[list[tp.Any], tp.Iterator[dict[str, tp.Any]]]] = groupby(args[0],
                                                                                             lambda x: [x[i] for i in
                                                                                                        self.keys])

        a, g_a = next(groups_a, (empty, empty_iter))
        b, g_b = next(groups_b, (empty, empty_iter))
        while g_a != empty_iter and g_b != empty_iter:
            if a < b:
                yield from self.joiner(self.keys, g_a, empty_iter)
                a, g_a = next(groups_a, (empty, empty_iter))
            elif a == b:
                yield from self.joiner(self.keys, g_a, g_b)
                a, g_a = next(groups_a, (empty, empty_iter))
                b, g_b = next(groups_b, (empty, empty_iter))
            else:
                yield from self.joiner(self.keys, empty_iter, g_b)
                b, g_b = next(groups_b, (empty, empty_iter))
        while g_a != empty_iter:
            yield from self.joiner(self.keys, g_a, empty_iter)
            a, g_a = next(groups_a, (empty, empty_iter))
        while g_b != empty_iter:
            yield from self.joiner(self.keys, empty_iter, g_b)
            b, g_b = next(groups_b, (empty, empty_iter))


# Dummy operators


class DummyMapper(Mapper):
    """Yield exactly the row passed"""

    def __call__(self, row: TRow) -> TRowsGenerator:
        if row is not None:
            yield row


class FirstReducer(Reducer):
    """Yield only first row from passed ones"""

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        for row in rows:
            yield row
            break


# Mappers


class FilterPunctuation(Mapper):
    """Left only non-punctuation symbols"""

    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    def __call__(self, row: TRow) -> TRowsGenerator:
        row[self.column] = ''.join(char for char in row[self.column] if char not in string.punctuation)
        yield row


class LowerCase(Mapper):
    """Replace column value with value in lower case"""

    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    @staticmethod
    def _lower_case(txt: str) -> str:
        return txt.lower()

    def __call__(self, row: TRow) -> TRowsGenerator:
        if self.column in row:
            row[self.column] = self._lower_case(row[self.column])
        yield row


class Split(Mapper):
    """Split row on multiple rows by separator"""

    def __init__(self, column: str, separator: str | None = None) -> None:
        """
        :param column: name of column to split
        :param separator: string to separate by
        """
        self.column = column
        self.separator = separator

    def __call__(self, row: TRow) -> TRowsGenerator:
        start = 0
        col = row[self.column]
        for i in range(len(col)):
            if ((self.separator is not None and col[i] == self.separator) or
                    (self.separator is None and col[i].isspace())):
                yield {**row, self.column: col[start:i]}
                start = i + 1
        if start != len(col):
            yield {**row, self.column: col[start:]}


class Product(Mapper):
    """Calculates product of multiple columns"""

    def __init__(self, columns: tp.Sequence[str], result_column: str = 'product') -> None:
        """
        :param columns: column names to product
        :param result_column: column name to save product in
        """
        self.columns = columns
        self.result_column = result_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        prod = 1
        for column in self.columns:
            if column in row:
                prod *= row[column]
        row[self.result_column] = prod
        yield row


class Filter(Mapper):
    """Remove records that don't satisfy some condition"""

    def __init__(self, condition: tp.Callable[[TRow], bool]) -> None:
        """
        :param condition: if condition is not true - remove record
        """
        self.condition = condition

    def __call__(self, row: TRow) -> TRowsGenerator:
        if self.condition(row):
            yield row


class Project(Mapper):
    """Leave only mentioned columns"""

    def __init__(self, columns: tp.Sequence[str]) -> None:
        """
        :param columns: names of columns
        """
        self.columns = columns

    def __call__(self, row: TRow) -> TRowsGenerator:
        for column in row.keys() - self.columns:
            if column in row:
                del row[column]
        yield row


# Reducers


class TopN(Reducer):
    """Calculate top N by value"""

    def __init__(self, column: str, n: int) -> None:
        """
        :param column: column name to get top by
        :param n: number of top values to extract
        """
        self.column_max = column
        self.n = n

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        largest_n = heapq.nlargest(self.n, rows, key=lambda row: row[self.column_max])
        for i in range(self.n):
            yield largest_n[len(list(rows)) - (i + 1)]


class TermFrequency(Reducer):
    """Calculate frequency of values in column"""

    def __init__(self, words_column: str, result_column: str = 'tf') -> None:
        """
        :param words_column: name for column with words
        :param result_column: name for result column
        """
        self.words_column = words_column
        self.result_column = result_column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        count = 0
        res: tp.Dict[str, int] = defaultdict(int)
        for row in rows:
            res[row[self.words_column]] += 1
            count += 1

        for w, r in res.items():
            yield {**{key: row[key] for key in group_key},
                   self.words_column: w,
                   self.result_column: r / count}


class Count(Reducer):
    """
    Count records by key
    Example for group_key=('a',) and column='d'
        {'a': 1, 'b': 5, 'c': 2}
        {'a': 1, 'b': 6, 'c': 1}
        =>
        {'a': 1, 'd': 2}
    """

    def __init__(self, column: str) -> None:
        """
        :param column: name for result column
        """
        self.column = column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        summ = 0
        for row in rows:
            summ += 1
        yield {**{key: row[key] for key in row if key in group_key}, self.column: summ}


class Sum(Reducer):
    """
    Sum values aggregated by key
    Example for key=('a',) and column='b'
        {'a': 1, 'b': 2, 'c': 4}
        {'a': 1, 'b': 3, 'c': 5}
        =>
        {'a': 1, 'b': 5}
    """

    def __init__(self, column: str) -> None:
        """
        :param column: name for sum column
        """
        self.column = column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        summ = 0
        for row in rows:
            summ += row[self.column]
        yield {**{key: row[key] for key in row if key in group_key}, self.column: summ}


# Joiners


class InnerJoiner(Joiner):
    """Join with inner strategy"""

    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        b = list(rows_b)
        for row_a in rows_a:
            for row_b in b:

                inner_keys = row_a.keys() & row_b.keys()
                joined: tp.Dict[str, tp.Any] = {}

                for x in row_a.keys() - inner_keys:
                    joined[x] = row_a[x]
                for x in keys:
                    joined[x] = row_a[x]

                for x in row_b.keys() - inner_keys:
                    joined[x] = row_b[x]
                for x in inner_keys - set(keys):
                    joined[x + self._a_suffix] = row_a[x]
                    joined[x + self._b_suffix] = row_b[x]

                yield joined


class OuterJoiner(Joiner):
    """Join with outer strategy"""

    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        a = list(rows_a)
        b = list(rows_b)
        yield from _left_join(a, b)
        if len(a) == 0:
            for row in b:
                yield row


class LeftJoiner(Joiner):
    """Join with left strategy"""

    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        yield from _left_join(rows_a, list(rows_b))


class RightJoiner(Joiner):
    """Join with right strategy"""

    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        yield from _left_join(rows_b, list(rows_a))
