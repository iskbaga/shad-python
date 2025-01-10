import typing as tp


class Kelvin:
    def __init__(self, attr: str) -> None:
        self.attr: str = attr

    def __get__(self, instance: object, owner: tp.Any) -> tp.Union['Kelvin', int | float]:
        if instance is None:
            return self
        return getattr(instance, self.attr)

    def __set__(self, instance: object, value: int) -> None:
        if value <= 0:
            raise ValueError
        elif not hasattr(instance, self.attr):
            raise AttributeError
        else:
            setattr(instance, self.attr, value)

    def __delete__(self, instance: object) -> None:
        raise ValueError


class Celsius:
    def __init__(self, attr: str) -> None:
        self.attr: str = attr

    def __get__(self, instance: object, owner: type[object]) -> int | float:
        if not isinstance(getattr(owner, self.attr), Kelvin):
            raise AttributeError
        return getattr(instance, self.attr) - 273

    def __set__(self, instance: object, value: tp.Any) -> None:
        raise AttributeError

    def __delete__(self, instance: object) -> None:
        raise ValueError
