import heapq
from collections import defaultdict


def normalize(
        text: str
) -> str:
    """
    Removes punctuation and digits and convert to lower case
    :param text: text to normalize
    :return: normalized query
    """
    return ''.join(char.lower() for char in text if char.isalpha() or char.isspace())


def get_words(
        query: str
) -> list[str]:
    """
    Split by words and leave only words with letters greater than 3
    :param query: query to split
    :return: filtered and split query by words
    """
    return [word for word in query.split() if len(word) > 3]


def build_index(
        banners: list[str]
) -> dict[str, list[int]]:
    """
    Create index from words to banners ids with preserving order and without repetitions
    :param banners: list of banners for indexation
    :return: mapping from word to banners ids
    """
    index: dict[str, list[int]] = defaultdict(list)

    for banner_id, banner in enumerate(banners):
        normalized_banner = normalize(banner)
        words = get_words(normalized_banner)

        for word in words:
            if banner_id not in index[word]:
                index[word].append(banner_id)

    return index


def get_banner_indices_by_query(
        query: str,
        index: dict[str, list[int]]
) -> list[int]:
    """
    Extract banners indices from index, if all words from query contains in indexed banner
    :param query: query to find banners
    :param index: index to search banners
    :return: list of indices of suitable banners
    """
    words: list[str] = get_words(normalize(query))
    if not words:
        return []
    banner_indices: set[int] = set(index.get(words[0], []))
    for word in words[1:]:
        banner_indices.intersection_update(index.get(word, []))
    heapq.heappush(words, "")
    heapq.heappop(words)
    return list(sorted(banner_indices))


#########################
# Don't change this code
#########################

def get_banners(
        query: str,
        index: dict[str, list[int]],
        banners: list[str]
) -> list[str]:
    """
    Extract banners matched to queries
    :param query: query to match
    :param index: word-banner_ids index
    :param banners: list of banners
    :return: list of matched banners
    """
    indices = get_banner_indices_by_query(query, index)
    return [banners[i] for i in indices]

#########################
