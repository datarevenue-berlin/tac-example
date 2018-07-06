from datetime import timedelta

import luigi
import docker
import os


def run(cmd):
    client = docker.from_env()
    logs = client.containers.run(
        image='tac-example',
        command=cmd,
        volumes={
            os.environ['DATA_DIR']:
                {'bind': '/data', 'mount': 'rw'}
        }
    )


class SourceData(luigi.ExternalTask):
    date = luigi.DateParameter()

    def output(self):
        return luigi.LocalTarget(
            path='/data/source/{:%Y-%m-%d}.csv'.format(self.date)
        )

    def complete(self):
        """Hack so we don't have to create input files manually."""
        return True


class FetchData(luigi.Task):
    date = luigi.DateParameter()

    def requires(self):
        return SourceData(date=self.date)

    def output(self):
        return luigi.LocalTarget(
            path='/data/raw/{:%Y-%m-%d}.csv'.format(self.date)
        )

    def run(self):
        run(self.cmd())

    def cmd(self):
        command = ['python', '-m', 'tac.fetch',
                   self.input().path, self.output().path]
        return command


class TransformData(luigi.Task):
    date = luigi.DateParameter()

    def requires(self):
        for delta in range(1, 11):
            yield FetchData(date=self.date - timedelta(days=delta))

    def output(self):
        return luigi.LocalTarget(
            path='/data/transformed/{:%Y-%m-%d}.csv'.format(self.date)
        )

    def run(self):
        run(self.cmd())

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
        return luigi.LocalTarget(
            path='/data/predictions/{:%Y-%m-%d}_{}.csv'.format(self.date,
                                                               self.model_name)
        )

    def run(self):
        run(self.cmd())

    def cmd(self):
        command = ['python', '-m', 'tac.predict',
                   self.model_name, self.input().path, self.output().path]
        return command


class MakePredictions(luigi.WrapperTask):
    date = luigi.DateParameter()

    def requires(self):
        for model_name in ['A', 'B']:
            yield Predict(date=self.date, model_name=model_name)
