def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    iterSubclassMap = {
        range: (tuple, 4),
        tuple: (list, 3),
        list: (bool, 2),
        bool: (bool, 1)
    }
    nonIterSubclassMap = {
        int: (float, 4),
        float: (complex, 3),
        complex: (bool, 2),
        bool: (bool, 1)
    }
    commonTypes = [bool, str]
    nonTerminalTypes = [range]

    def get_parent(typ1: type, typ2: type, mapp: dict[type, tuple[type, int]]) -> type:
        a, b = typ1, typ2
        while a != b:
            x = mapp[a]
            y = mapp[b]
            if x[1] > y[1]:
                a = x[0]
            if x[1] < y[1]:
                b = y[0]
        while a in nonTerminalTypes:
            a = iterSubclassMap[a][0]
        return a

    if type1 in commonTypes and type2 in commonTypes:
        return str if type1 == str or type2 == str else bool
    if type1 is bool and type2 in nonIterSubclassMap:
        return type2
    if type2 is bool and type1 in nonIterSubclassMap:
        return type1
    if type1 is bool and type2 in iterSubclassMap:
        return str
    if type2 is bool and type1 in iterSubclassMap:
        return str
    if type1 is str and (type2 in nonIterSubclassMap or type2 in iterSubclassMap):
        return str
    if type2 is str and (type1 in nonIterSubclassMap or type1 in iterSubclassMap):
        return str
    elif type1 in nonIterSubclassMap and type2 in iterSubclassMap:
        return str
    elif type2 in nonIterSubclassMap and type1 in iterSubclassMap:
        return str
    elif type1 in nonIterSubclassMap:
        return get_parent(type1, type2, nonIterSubclassMap)
    else:
        return get_parent(type1, type2, iterSubclassMap)
