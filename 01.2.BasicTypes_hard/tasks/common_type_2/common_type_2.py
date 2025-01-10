import typing as tp


def convert_to_common_type(data: list[tp.Any]) -> list[tp.Any]:
    """
    Takes list of multiple types' elements and convert each element to common type according to given rules
    :param data: list of multiple types' elements
    :return: list with elements converted to common type
    """

    def singleType(data: list[tp.Any]) -> type:
        for x in data:
            if x != "":
                return type(x)
        return str

    def innerFormat(x: tp.Any) -> str:
        if (type(x) is None) or (type(x) is str and not x):
            return "none"
        if type(x) is int:
            return "int"
        if type(x) is float:
            return "float"
        if type(x) is str:
            return "str"
        if type(x) is list:
            return "list"
        if type(x) is tuple:
            return "tuple"
        if type(x) is bool:
            return "bool"
        return "none"

    def noneConvert(typ: type) -> tp.Any:
        if typ is int:
            return 0
        if typ is float:
            return 0.0
        if typ is str:
            return ""
        if typ is list:
            return []
        if typ is tuple:
            return ()
        if typ is bool:
            return False
        return ""

    def toType(x: tp.Any, typ: type) -> tp.Any:
        if typ is list and type(x) is not tuple:
            return [x]
        else:
            return typ(x)

    def outerFormat(data: list[tp.Any], typ: type) -> list[tp.Any]:
        result = []
        for i, x in enumerate(data):
            if x is None or x == "":
                result.append(noneConvert(typ))
            elif type(x) is not typ:
                result.append(toType(x, typ))
            else:
                result.append(x)
        return result

    types = [
        ({"str", "list", "tuple"}, list),
        ({"int", "float"}, float),
        ({"int", "bool"}, bool),
        ({"list", "tuple", "int", "bool"}, list)
    ]

    dataTypes = set()
    for x in data:
        if (innerFormat(x)) != "none":
            dataTypes.add(innerFormat(x))

    if len(dataTypes) <= 1:
        return outerFormat(data, singleType(data))
    for s, x in types:
        if dataTypes.issubset(s):
            return outerFormat(data, x)
    return outerFormat(data, str)
