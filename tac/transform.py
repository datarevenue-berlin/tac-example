import click
from time import sleep
from luigi.contrib.s3 import S3Target
import boto3.s3.transfer  # Luigi's bug workaround


def transform_data(paths):
    print('Transforming data')
    sleep(3)
    return 123


def save_result(data, path):
    print('Saving result')
    sleep(3)
    S3Target(path).open('w').close()


@click.command()
@click.argument('output-path')
@click.argument('input-paths', nargs=-1)
def cli(output_path, input_paths):
    result = transform_data(paths=input_paths)
    save_result(data=result, path=output_path)


if __name__ == '__main__':
    cli()
