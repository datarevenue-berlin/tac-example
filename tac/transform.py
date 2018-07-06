import click
import os
from time import sleep


def transform_data(paths):
    print('Transforming data')
    sleep(1)
    return 123


def save_result(data, path):
    print('Saving result')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').close()


@click.command()
@click.argument('output-path')
@click.argument('input-paths', nargs=-1)
def cli(output_path, input_paths):
    result = transform_data(paths=input_paths)
    save_result(data=result, path=output_path)


if __name__ == '__main__':
    cli()
