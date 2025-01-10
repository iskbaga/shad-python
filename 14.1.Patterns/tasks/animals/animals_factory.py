import typing as tp

from abc import ABC, abstractmethod

from .animals import Cat, Cow, Dog


class Animal(ABC):
    @abstractmethod
    def say(self) -> str:
        pass


class CatAdapter(Animal):
    def __init__(self, cat: Cat) -> None:
        self.cat: Cat = cat

    def say(self) -> str:
        return self.cat.say()


class DogAdapter(Animal):
    def __init__(self, dog: Dog) -> None:
        self.dog: Dog = dog

    def say(self) -> str:
        return self.dog.say("woof")


class CowAdapter(Animal):
    def __init__(self, cow: Cow) -> None:
        self.cow: Cow = cow

    def say(self) -> str:
        return self.cow.talk()


def animals_factory(animal: tp.Any) -> Animal:
    if isinstance(animal, Cat):
        return CatAdapter(animal)
    elif isinstance(animal, Dog):
        return DogAdapter(animal)
    elif isinstance(animal, Cow):
        return CowAdapter(animal)
    else:
        raise TypeError
