import typing as tp


class ConverterMetaclass(type):
    def __new__(cls, name: str, bases: tp.Any, dct: dict[str, tp.Any]) -> tp.Any:

        getters: dict[str, tp.Any] = {name[4:]: attr_value for (name, attr_value) in dct.items() if
                                      name.startswith("get_")}
        setters: dict[str, tp.Any] = {name[4:]: attr_value for (name, attr_value) in dct.items() if
                                      name.startswith("set_")}

        for base in bases:
            for name, attr_value in base.__dict__.items():
                if name.startswith("get_"):
                    getters[name[4:]] = attr_value
                elif name.startswith("set_"):
                    setters[name[4:]] = attr_value

        props: dict[str, tp.Any] = {name: property(getters.get(name), setters.get(name))
                                    for name in (getters.keys() | setters.keys()) - dct.keys()}

        return super().__new__(cls, name, bases, dct | props)


class PropertyConverter(metaclass=ConverterMetaclass):
    def __setattr__(self, x: str, y: tp.Any) -> None:
        object.__setattr__(self, x, y)

    def __getattr__(self, x: str) -> tp.Any:
        pass
