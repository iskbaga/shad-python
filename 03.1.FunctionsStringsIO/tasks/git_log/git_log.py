import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """
    for line in inp:
        parts = line.strip().split('\t')
        if len(parts) < 5:
            continue

        sha1, date, author, email, message = parts
        formatted_line = f"{sha1[:7]}{'.' * (73 - len(message))}{message}"
        out.write(formatted_line + '\n')
