def wins_correlation() -> str:
    """
    Return column with maximum correlation with number of wins
    """
    return "nrOfNominations"


def imdb_rating_by_time() -> tuple[str, int]:
    """
    Return tuple with trend ("ascending" or "descending") and start of 10 year period with maximum mean rating.
    """
    return 'descending', 1920


def genre_ratings() -> tuple[str, str]:
    """
    Return tuple with 2 genres: genre with maximum median rating and genre with broadest IQR.
    """
    return "Documentary", "Family"


def number_of_words_mode() -> int:
    """
    Return mode for number of words in movie title (as integer)
    """
    return 4


def short_movie_year() -> int:
    """
    Return start of 10 year period with maximum share of short movies (< 1 hour)
    """
    return 2010


def movie_reviews() -> str:
    """
    Return most popular genre by user reviews. Think about the correct metric.
    """
    return 'Thriller'
