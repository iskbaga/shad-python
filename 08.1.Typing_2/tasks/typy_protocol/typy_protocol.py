from typing import Protocol


class Gettable(Protocol):

    def __getitem__(self, item: int) -> str | int:
        pass

    def __len__(self) -> int:
        pass


def get(container: Gettable, index: int) -> str | int | None:
    if container:
        return container[index]

    return None
