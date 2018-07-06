import click
import os
from time import sleep


def predict(model_name, data_path, output_path):
    print('Reading data from {}, predicting with model {} and writing to {}'
          .format(data_path, model_name, output_path))
    sleep(1)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    open(output_path, 'w').close()


@click.command()
@click.argument('model-name')
@click.argument('data-path')
@click.argument('output-path')
def cli(model_name, data_path, output_path):
    predict(model_name, data_path, output_path)


if __name__ == '__main__':
    cli()
