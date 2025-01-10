import zlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class BlobType(Enum):
    """Helper class for holding blob type"""
    COMMIT = b'commit'
    TREE = b'tree'
    DATA = b'blob'

    @classmethod
    def from_bytes(cls, type_: bytes) -> 'BlobType':
        for member in cls:
            if member.value == type_:
                return member
        assert False, f'Unknown type {type_.decode("utf-8")}'


@dataclass
class Blob:
    """Any blob holder"""
    type_: BlobType
    content: bytes


@dataclass
class Commit:
    """Commit blob holder"""
    tree_hash: str
    parents: list[str]
    author: str
    committer: str
    message: str


@dataclass
class Tree:
    """Tree blob holder"""
    children: dict[str, Blob]


def read_blob(path: Path) -> Blob:
    """
    Read blob-file, decompress and parse header
    :param path: path to blob-file
    :return: blob-file type and content
    """
    with path.open('rb') as f:
        decompressed = zlib.decompress(f.read())

    type_length, _, content = decompressed.partition(b'\x00')
    type_ = type_length.split(b' ')[0]

    return Blob(type_=BlobType.from_bytes(type_), content=content)


def traverse_objects(obj_dir: Path) -> dict[str, Blob]:
    """
    Traverse directory with git objects and load them
    :param obj_dir: path to git "objects" directory
    :return: mapping from hash to blob with every blob found
    """
    blob: dict[str, Blob] = {}
    for obj in obj_dir.iterdir():
        if obj.is_dir():
            for f in obj.iterdir():
                blob[obj.name[0:2] + f.name] = read_blob(f)
    return blob


def parse_commit(blob: Blob) -> Commit:
    """
    Parse commit blob
    :param blob: blob with commit type
    :return: parsed commit
    """
    tree_hash = ''
    parents: list[str] = []
    author = ''
    committer = ''
    message = ''

    lines = blob.content.decode().splitlines()
    for (i, line) in enumerate(lines[:]):
        if not line:
            message = ''.join(lines[j] for j in range(i + 1, len(lines)))
            break
        if line.startswith('tree'):
            tree_hash = line[5:]
        elif line.startswith('parent'):
            parents.append(line[7:])
        elif line.startswith('author'):
            author = line[7:]
        elif line.startswith('committer'):
            committer = line[10:]

    return Commit(
        tree_hash=tree_hash,
        parents=parents,
        author=author,
        committer=committer,
        message=message
    )


def parse_tree(blobs: dict[str, Blob], tree_root: Blob, ignore_missing: bool = True) -> Tree:
    """
    Parse tree blob
    :param blobs: all read blobs (by traverse_objects)
    :param tree_root: tree blob to parse
    :param ignore_missing: ignore blobs which were not found in objects directory
    :return: tree contains children blobs (or only part of them found in objects directory)
    NB. Children blobs are not being parsed according to type.
        Also nested tree blobs are not being traversed.
    """

    result: dict[str, Blob] = {}
    i = 0
    content = tree_root.content
    while i < len(content):
        mode_end = content.find(b' ', i)
        name_end = content.find(b'\0', mode_end)
        name = content[mode_end + 1:name_end].decode('utf-8')
        object_hash = content[name_end + 1:name_end + 21].hex()
        i = name_end + 21

        child = blobs.get(object_hash)
        if child:
            result[name] = child
        elif not ignore_missing:
            result[name] = Blob(type_=BlobType.DATA, content=b'')

    return Tree(children=result)


def find_initial_commit(blobs: dict[str, Blob]) -> Commit:
    """
    Iterate over blobs and find initial commit (without parents)
    :param blobs: blobs read from objects dir
    :return: initial commit
    """
    for _, blob in blobs.items():
        if blob.type_ == BlobType.COMMIT:
            commit = parse_commit(blob)
            if not commit.parents:
                return commit
    raise ValueError("no initial comment")


def search_file(blobs: dict[str, Blob], tree_root: Blob, filename: str) -> Blob:
    """
    Traverse tree blob (can have nested tree blobs) and find requested file,
    check if file was not found (assertion).
    :param blobs: blobs read from objects dir
    :param tree_root: root blob for traversal
    :param filename: requested file
    :return: requested file blob
    """
    tree = parse_tree(blobs, tree_root)

    for hash_, blob in tree.children.items():
        if hash_ == filename:
            return blob
        elif blob.type_ == BlobType.TREE:
            try:
                return search_file(blobs, blob, filename)
            except AssertionError:
                pass

    raise ValueError("no file")
