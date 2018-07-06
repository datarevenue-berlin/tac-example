import click
import os
from time import sleep


def fetch_data(input_path, output_path):
    print('Reading from {} and writing to {}'.format(input_path, output_path))
    sleep(1)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    open(output_path, 'w').close()


@click.command()
@click.argument('input-path')
@click.argument('output-path')
def cli(input_path, output_path):
    fetch_data(input_path, output_path)


if __name__ == '__main__':
    cli()
