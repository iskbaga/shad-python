class LifeGame(object):
    """
    Class for Game life
    """

    def __init__(self, ocean: list[list[int]]):
        self.ocean = ocean

    def _calc(self, i: int, j: int) -> int:
        cell: int = self.ocean[i][j]
        cells: list[int] = []
        for k in range(max(i - 1, 0), min(len(self.ocean), i + 2)):
            for m in range(max(j - 1, 0), min(len(self.ocean[0]), j + 2)):
                if not (k == i and m == j):
                    cells.append(self.ocean[k][m])

        if cell == 2 or cell == 3:
            if 2 <= sum(1 for n in cells if n == cell) <= 3:
                return cell
            return 0
        elif cell == 0:
            if sum(1 for n in cells if n == 2) == 3:
                return 2
            elif sum(1 for n in cells if n == 3) == 3:
                return 3
        return cell

    def get_next_generation(self) -> list[list[int]]:
        next_iter: list[list[int]] = [row[:] for row in self.ocean]
        for i in range(len(self.ocean)):
            for j in range(len(self.ocean[0])):
                next_iter[i][j] = self._calc(i, j)
        self.ocean = next_iter
        return self.ocean
