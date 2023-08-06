import json
import time

from loko_client.utils.logger_utils import stream_logger

logger = stream_logger(__name__)

class JobsClient:
    def __init__(self, u):
        self.u = u.jobs

    def all(self):

        r = self.u.get()
        return r.json()

    def delete(self, job):

        r = self.u[job].delete()
        return r.json()

    def info(self, job):

        r = self.u[job].get()
        return r.json()

class ContainersClient:
    def __init__(self, u):
        self.u = u.containers

    def all(self):
        r = self.u.get()
        return r.json()

    def info(self, container):
        r = self.u[container].get()
        return r.json()

    def delete(self, container):
        r = self.u[container].delete()
        return r.json()

class PredictorsClient:
    """
        Predictors client used to manage Loko predictors.
    """
    def __init__(self, u):
        self.u = u.predictors
        self.jobs = JobsClient(u=u)

    def all(self):
        """
            List all predictors.
        """
        r = self.u.get()
        return r.json()

    def info(self, predictor, details=True, branch='development'):
        """
            Display predictor info.
        """
        details = json.dumps(details)
        r = self.u[predictor].get(params=dict(details=details, branch=branch))
        return r.json()

    def save(self, predictor, description='', model_id='auto', transformer_id='auto', blueprint=None):
        """
            Save a new predictor.
        """
        blueprint = blueprint or {}
        r = self.u[predictor].post(json=blueprint,
                                   params=dict(description=description, model_id=model_id,
                                               transformer_id=transformer_id))
        return r.json()

    def delete(self, predictor):
        """
            Delete an existing predictor.
        """
        r = self.u[predictor].delete()
        return r.json()

    def fit(self, predictor, data, partial=False, fit_params=None, cv=0, report=True, history_limit=0,
            test_size=.2, task=None, save_dataset=False, wait=False):
        """
            Fit an existing predictor.
        """
        report = json.dumps(report)
        partial = json.dumps(partial)
        save_dataset = json.dumps(save_dataset)
        task = task or 'null'
        fit_params = fit_params or {}
        fit_params = json.dumps(fit_params)
        params = dict(partial=partial, fit_params=fit_params, cv=cv, report=report, history_limit=history_limit,
                      test_size=test_size, task=task, save_dataset=save_dataset)
        r = self.u[predictor].fit.post(params=params, json=data)

        if not wait:
            return r.json()
        else:
            logger.debug('WAIT FOR JOB')
            last_msg = ''
            while True:
                time.sleep(2)
                res = self.jobs.info(predictor)
                if res:
                    new_msg = res[-1]['status']
                    if last_msg != new_msg:
                        logger.debug(f'STATUS: {new_msg}')
                        last_msg = new_msg
                        if res[-1]['status'] == 'Pipeline END':
                            return 'OK'
                        if any([el['status'].startswith('ERROR') for el in res]):
                            return 'ERROR'

    def predict(self, predictor, data, include_probs=False, branch='development'):
        """
            Get predictions from an existing predictor.
        """
        include_probs = json.dumps(include_probs)
        r = self.u[predictor].predict.post(json=data, params=dict(include_probs=include_probs, branch=branch))
        return r.json()

    def evaluate(self, predictor, data, branch='development', limit=0, pretty=False):
        """
            Evaluate existing predictor.
        """
        pretty = json.dumps(pretty)
        r = self.u[predictor].evaluate.post(json=data, params=dict(branch=branch, limit=limit, pretty=pretty))
        return r.json()

    def upload(self, predictor_file):
        """
            Import a new predictor.
        """
        r = self.u['import'].post(files={'f': predictor_file})
        return r.json()

    def download(self, predictor):
        """
            Export an existing predictor.
        """
        r = self.u[predictor].export.get()
        return r.content

    def release(self, predictor, history_limit=0):
        """
            Copy predictor into master branch.
        """
        r = self.u[predictor].release.get(params=dict(history_limit=history_limit))
        return r.json()

    def rollback(self, predictor, branch='development'):
        r = self.u[predictor].rollback.get(params=dict(branch=branch))
        pass

    def copy(self, predictor, new_name=None):
        """
            Copy an existing predictor.
        """
        new_name = new_name or 'null'
        r = self.u[predictor].copy.get(params=dict(new_name=new_name))
        return r.json()

    def history(self, predictor, pretty=False):
        """
            Get all performance report of a predictor.
        """
        pretty = json.dumps(pretty)
        r = self.u[predictor].history.get(params=dict(pretty=pretty))
        return r.json()


class ModelsClient:
    def __init__(self, u):
        self.u = u.models

    def all(self):
        r = self.u.get()
        return r.json()

    def save(self, model, blueprint):
        r = self.u[model].post(json=blueprint)
        return r.json()

    def delete(self, model):
        r = self.u[model].delete()
        return r.json()

    def info(self, model):
        r = self.u[model].get()
        return r.json()

class TransformersClient:
    def __init__(self, u):
        self.u = u.transformers

    def all(self):
        r = self.u.get()
        return r.json()

    def save(self, transformer, blueprint):
        r = self.u[transformer].post(json=blueprint)
        return r.json()

    def delete(self, transformer):
        r = self.u[transformer].delete()
        return r.json()

    def info(self, transformer):
        r = self.u[transformer].get()
        return r.json()

class DatasetsClient:
    def __init__(self, u):
        self.u = u.datasets

    def all(self):
        r = self.u.get()
        return r.json()

    def info(self, dataset):
        r = self.u[dataset].get()
        return r.json()

    def delete(self, dataset):
        r = self.u[dataset].delete()
        return r.json()

    def upload(self, dataset_file):
        r = self.u['import'].post(files={'f': dataset_file})
        return r.json()

    def download(self, dataset):
        r = self.u[dataset].export.get()
        return r.content


