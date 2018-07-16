from datetime import timedelta
from time import sleep
import luigi
import os

from luigi.contrib.kubernetes import KubernetesJobTask
from luigi.contrib.s3 import S3Target


IMAGE = 'tac-example:v1'
BUCKET = os.environ['S3_BUCKET']


class SourceData(luigi.ExternalTask):
    date = luigi.DateParameter()

    def output(self):
        return S3Target(
            path='s3://{bucket}/tac-example/data/source/{date:%Y-%m-%d}.csv'
                 .format(bucket=BUCKET, date=self.date)
        )

    def complete(self):
        """Hack so we don't have to create input files manually.

        Luigi will always think that this task is done, without checking for
        presence of source files.
        """
        return True


class FetchData(luigi.Task):
    date = luigi.DateParameter()

    def requires(self):
        return SourceData(date=self.date)

    def output(self):
        return S3Target(
            path='s3://{bucket}/tac-example/data/raw/{date:%Y-%m-%d}.csv'
                 .format(bucket=BUCKET, date=self.date)
        )

    def run(self):
        print('Reading from {} and writing to {}'
              .format(self.input().path, self.output().path))
        sleep(1)
        # self.output().makedirs()
        self.output().open('w').close()


class TransformData(KubernetesJobTask):
    date = luigi.DateParameter()

    @property
    def name(self):
        return 'transform-data'

    @property
    def spec_schema(self):
        return {
            "containers": [{
                "name": self.name,
                "image": 'tac-example:v1',
                "command": self.cmd
            }],
        }

    def requires(self):
        for delta in range(1, 11):
            yield FetchData(date=self.date - timedelta(days=delta))

    def output(self):
        return S3Target(
            path='s3://{bucket}/tac-example/data/transformed/{date:%Y-%m-%d}.csv'
                 .format(bucket=BUCKET, date=self.date)
        )

    @property
    def cmd(self):
        command = ['python', '-m', 'tac.transform', self.output().path]
        command += [item.path for item in self.input()]
        return command


class Predict(luigi.Task):
    date = luigi.DateParameter()
    model_name = luigi.Parameter()

    def requires(self):
        return TransformData(date=self.date)

    def output(self):
        return S3Target(
            path='s3://{bucket}/tac-example/data/predictions/{date:%Y-%m-%d}_{model}.csv'
                 .format(bucket=BUCKET, date=self.date, model=self.model_name)
        )

    def run(self):
        print('Predicting with model {} and saving to {}'
              .format(self.model_name, self.output().path))
        sleep(1)
        # self.output().makedirs()
        self.output().open('w').close()


class MakePredictions(luigi.WrapperTask):
    date = luigi.DateParameter()

    def requires(self):
        for model_name in ['A', 'B']:
            yield Predict(date=self.date, model_name=model_name)
