import click
from PIL import Image
import numpy as np
from .encode import encode_message
from .decode import decode_message
from .utils import get_base_file, write_file


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument('output_filename')
@click.argument('secret_message')
def encode(output_filename: str, secret_message: str) -> None:
    data = get_base_file()
    encoded_data = encode_message(data, secret_message)
    write_file(encoded_data, output_filename)


@cli.command()
@click.argument('input_filename')
def decode(input_filename: str) -> None:
    image = np.array(Image.open(input_filename))
    decoded_message = decode_message(image)
    click.echo(decoded_message)
