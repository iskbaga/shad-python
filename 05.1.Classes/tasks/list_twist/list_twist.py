from collections import UserList
import typing as tp


class ListTwist(UserList[tp.Any]):
    """
    List-like class with additional attributes:
        * reversed, R - return reversed list
        * first, F - insert or retrieve first element;
                     Undefined for empty list
        * last, L -  insert or retrieve last element;
                     Undefined for empty list
        * size, S -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """

    def __getattr__(self, name: str) -> tp.Any:
        if name == "reversed" or name == "R":
            return self.data[::-1]
        elif name == "first" or name == "F":
            return self.data[0]
        elif name == "last" or name == "L":
            return self.data[-1]
        elif name == "size" or name == "S":
            return len(self.data)

    def __setattr__(self, name: str, value: tp.Any) -> None:
        if name == "first" or name == "F":
            self.data[0] = value
        elif name == "last" or name == "L":
            self.data[-1] = value
        elif name == "size" or name == "S":
            if value < len(self.data):
                del self.data[value:]
            elif value > len(self.data):
                self.data.extend([None] * (value - len(self.data)))
        else:
            super().__setattr__(name, value)
