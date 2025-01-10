def problem01() -> dict[int, str]:
    return {5: "если a будет None то сумма не определена",
            7: "get возвращает Optional"}


def problem02() -> dict[int, str]:
    return {5: 'для ближайшего типа object сложения нет'}


def problem03() -> dict[int, str]:
    return {9: 'tp.Set[float] а не tp.Set[int]',
            13: 'tp.Set[bool] а не tp.Set[int] так как инвариантность'}


def problem04() -> dict[int, str]:
    return {9: 'tp.Set[float] а не tp.Set[int]'}


def problem05() -> dict[int, str]:
    return {11: 'A не подкласс B'}


def problem06() -> dict[int, str]:
    return {15: "сначала тип сузился а потом расширился"}


def problem07() -> dict[int, str]:
    return {25: "A не могу в B",
            27: "[B] не могу в [A]",
            28: "[B] не могу в [A]"}


def problem08() -> dict[int, str]:
    return {6: "Iterable а не Sized",
            18: "A а не Iterable[str]",
            24: "B а не Iterable[str]"}


def problem09() -> dict[int, str]:
    return {32: "нет in для str и Fooable",
            34: "list а не Fooable",
            37: "C а не  Fooable",
            38: "callable а не Fooable"}


def problem10() -> dict[int, str]:
    return {18: "str не подходит SupportsFloat",
            29: "флоат не кастится в инт"}
