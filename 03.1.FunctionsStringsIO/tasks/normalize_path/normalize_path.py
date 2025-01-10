def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """

    parts = path.split('/')
    stack: list[str] = []

    for part in parts:
        if part == '' or part == '.':
            continue
        elif part == '..':
            if stack and stack[-1] != '..':
                stack.pop()
            elif not path.startswith('/'):
                stack.append('..')
        else:
            stack.append(part)

    res_path = '/' + '/'.join(stack) if path.startswith('/') else '/'.join(stack)

    if not res_path:
        return '/' if path.startswith('/') else '.'

    return res_path
