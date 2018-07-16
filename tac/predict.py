import click
from luigi.contrib.s3 import S3Target
from time import sleep
import boto3.s3.transfer  # Luigi's bug workaround


def predict(model_name, data_path, output_path):
    print('Reading data from {}, predicting with model {} and writing to {}'
          .format(data_path, model_name, output_path))
    sleep(1)
    S3Target(output_path).open('w').close()


@click.command()
@click.argument('model-name')
@click.argument('data-path')
@click.argument('output-path')
def cli(model_name, data_path, output_path):
    predict(model_name, data_path, output_path)


if __name__ == '__main__':
    cli()
