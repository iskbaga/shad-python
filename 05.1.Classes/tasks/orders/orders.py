from dataclasses import dataclass, field, InitVar
from abc import ABC, abstractmethod

DISCOUNT_PERCENTS = 15


@dataclass(init=True, frozen=True, order=True)
class Item:
    item_id: int = field(compare=False)
    title: str
    cost: int

    def __post_init__(self) -> None:
        assert self.title
        assert self.cost > 0


# You may set `# type: ignore` on this class
# It is [a really old issue](https://github.com/python/mypy/issues/5374)
# But seems to be solved
@dataclass
class Position(ABC):
    item: Item

    @property
    @abstractmethod
    def cost(self) -> int | float:
        pass


@dataclass
class CountedPosition(Position):
    item: Item
    count: int = field(default=1)

    @property
    def cost(self) -> int | float:
        return self.item.cost * self.count


@dataclass
class WeightedPosition(Position):
    item: Item
    weight: float = field(default=1.0)

    @property
    def cost(self) -> int | float:
        return self.item.cost * self.weight


@dataclass
class Order:
    order_id: int
    positions: list[Position] = field(default_factory=list)
    have_promo: InitVar[bool] = False

    @property
    def cost(self) -> int | float:
        return int(self._cost)

    def __post_init__(self, have_promo: bool) -> None:
        self._cost = sum([pos.cost for pos in self.positions])
        if have_promo:
            self._cost *= ((100 - DISCOUNT_PERCENTS) / 100)
