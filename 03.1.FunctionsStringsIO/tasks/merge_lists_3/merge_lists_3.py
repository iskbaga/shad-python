import typing as tp
import heapq


def merge(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    heap: list[tuple[int, bytes, tp.IO[bytes]]] = []
    for stream in input_streams:
        line = stream.readline()
        if line:
            heapq.heappush(heap, (int(line), line, stream))
    while heap:
        _, min_line, stream = heapq.heappop(heap)
        output_stream.write(min_line)
        next_line = stream.readline()
        if next_line:
            heapq.heappush(heap, (int(next_line), next_line, stream))
