import enum
from collections import defaultdict, deque


class Status(enum.Enum):
    NEW = 0
    EXTRACTED = 1
    FINISHED = 2


def extract_alphabet(
        graph: dict[str, set[str]]
) -> list[str]:
    """
    Extract alphabet from graph
    :param graph: graph with partial order
    :return: alphabet
    """
    degrees = {char: 0 for char in graph.keys()}

    for char in degrees:
        for neighbor in graph[char]:
            degrees[neighbor] += 1

    char_queue = deque([char for char in degrees if degrees[char] == 0])
    res_order = []

    while char_queue:
        char = char_queue.popleft()
        res_order.append(char)
        for x in graph[char]:
            degrees[x] -= 1
            if degrees[x] == 0:
                char_queue.append(x)
    return res_order


def build_graph(
        words: list[str]
) -> dict[str, set[str]]:
    """
    Build graph from ordered words. Graph should contain all letters from words
    :param words: ordered words
    :return: graph
    """
    res = defaultdict(set)
    for first, second in zip(words, words[1:]):
        for i in range(min(len(first), len(second))):
            if first[i] != second[i]:
                res[first[i]].add(second[i])
                break
    for word in words:
        for char in word:
            if char not in res:
                res[char] = set()

    return dict(res)


#########################
# Don't change this code
#########################

def get_alphabet(
        words: list[str]
) -> list[str]:
    """
    Extract alphabet from sorted words
    :param words: sorted words
    :return: alphabet
    """
    graph = build_graph(words)
    return extract_alphabet(graph)

#########################
