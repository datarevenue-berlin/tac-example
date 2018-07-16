import click
from time import sleep
from luigi.contrib.s3 import S3Target
import boto3.s3.transfer  # Luigi's bug workaround


def fetch_data(input_path, output_path):
    print('Reading from {} and writing to {}'.format(input_path, output_path))
    sleep(1)
    S3Target(output_path).open('w').close()


@click.command()
@click.argument('input-path')
@click.argument('output-path')
def cli(input_path, output_path):
    fetch_data(input_path, output_path)


if __name__ == '__main__':
    cli()
