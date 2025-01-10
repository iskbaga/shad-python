import sys
import typing as tp
from pathlib import Path


def tail(filename: Path, lines_amount: int = 10, output: tp.IO[bytes] | None = None) -> None:
    """
    :param filename: file to read lines from (the file can be very large)
    :param lines_amount: number of lines to read
    :param output: stream to write requested amount of last lines from file
                   (if nothing specified stdout will be used)
    """
    if not output:
        output = sys.stdout.buffer
    buf_size = 1024 * 228

    with filename.open('rb') as f:
        f.seek(0, 2)
        pos = f.tell()
        amount = lines_amount
        res = bytearray()
        while pos > 0 and amount > 0:
            sz = min(pos, buf_size)
            pos -= sz
            f.seek(pos)
            chunk = f.read(sz)
            res = bytearray(chunk) + res
            amount -= chunk.count(b'\n')
        res_lines = res.splitlines(keepends=True)
        output.write(b''.join(res_lines[-lines_amount:]))
