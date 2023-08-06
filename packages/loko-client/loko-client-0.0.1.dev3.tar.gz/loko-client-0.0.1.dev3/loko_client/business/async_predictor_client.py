import asyncio
import json

from loko_client.utils.logger_utils import stream_logger

logger = stream_logger(__name__)

class AsyncJobsClient:
    def __init__(self, u):
        self.u = u.jobs

    async def all(self):
        r = await self.u.request('GET')
        return await r.json()

    async def delete(self, job):
        r = await self.u[job].request('DELETE')
        return await r.json()

    async def info(self, job):
        r = await self.u[job].request('GET')
        return await r.json()

class AsyncContainersClient:
    def __init__(self, u):
        self.u = u.containers

    async def all(self):
        r = await self.u.request('GET')
        return await r.json()

    async def info(self, container):
        r = await self.u[container].request('GET')
        return await r.json()

    async def delete(self, container):
        r = await self.u[container].request('DELETE')
        return await r.json()

class AsyncPredictorsClient:
    def __init__(self, u):
        self.u = u.predictors
        self.jobs = AsyncJobsClient(u=u)

    async def all(self):
        r = await self.u.request('GET')
        return await r.json()

    async def info(self, predictor, details=True, branch='development'):
        details = json.dumps(details)
        r = await self.u[predictor].request('GET', params=dict(details=details, branch=branch))
        return await r.json()

    async def save(self, predictor, description='', model_id='auto', transformer_id='auto', blueprint=None):
        blueprint = blueprint or {}
        r = await self.u[predictor].request('POST', json=blueprint,
                                            params=dict(description=description, model_id=model_id,
                                                        transformer_id=transformer_id))
        return await r.json()

    async def delete(self, predictor):
        r = await self.u[predictor].request('DELETE')
        return await r.json()

    async def fit(self, predictor, data, partial=False, fit_params=None, cv=0, report=True, history_limit=0,
            test_size=.2, task=None, save_dataset=False, wait=False):
        report = json.dumps(report)
        partial = json.dumps(partial)
        save_dataset = json.dumps(save_dataset)
        task = task or 'null'
        fit_params = fit_params or {}
        fit_params = json.dumps(fit_params)
        params = dict(partial=partial, fit_params=fit_params, cv=cv, report=report, history_limit=history_limit,
                      test_size=test_size, task=task, save_dataset=save_dataset)
        r = await self.u[predictor].fit.request('POST', params=params, json=data)

        if not wait:
            return await r.json()
        else:
            logger.debug('WAIT FOR JOB')
            last_msg = ''
            while True:
                await asyncio.sleep(2)
                res = await self.jobs.info(predictor)
                if res:
                    new_msg = res[-1]['status']
                    if last_msg != new_msg:
                        logger.debug(f'STATUS: {new_msg}')
                        last_msg = new_msg
                        if res[-1]['status'] == 'Pipeline END':
                            return 'OK'
                        if any([el['status'].startswith('ERROR') for el in res]):
                            return 'ERROR'

    async def predict(self, predictor, data, include_probs=False, branch='development'):
        include_probs = json.dumps(include_probs)
        r = await self.u[predictor].predict.request('POST', json=data,
                                                    params=dict(include_probs=include_probs, branch=branch))
        return await r.json()

    async def evaluate(self, predictor, data, branch='development', limit=0, pretty=False):
        pretty = json.dumps(pretty)
        r = await self.u[predictor].evaluate.request('POST', json=data,
                                                     params=dict(branch=branch, limit=limit, pretty=pretty))
        return await r.json()

    async def upload(self, predictor_file):
        r = await self.u['import'].request('POST', data={'f': predictor_file})
        return await r.json()

    async def download(self, predictor):
        r = await self.u[predictor].export.request('GET')
        return r.content

    async def release(self, predictor, history_limit=0):
        r = await self.u[predictor].release.request('GET', params=dict(history_limit=history_limit))
        return await r.json()

    async def rollback(self, predictor, branch='development'):
        r = await self.u[predictor].rollback.request('GET', params=dict(branch=branch))
        pass

    async def copy(self, predictor, new_name=None):
        new_name = new_name or 'null'
        r = await self.u[predictor].copy.request('GET', params=dict(new_name=new_name))
        return await r.json()

    async def history(self, predictor, pretty=False):
        pretty = json.dumps(pretty)
        r = await self.u[predictor].history.request('GET', params=dict(pretty=pretty))
        return await r.json()


class AsyncModelsClient:
    def __init__(self, u):
        self.u = u.models

    async def all(self):
        r = await self.u.request('GET')
        return await r.json()

    async def save(self, model, blueprint):
        r = await self.u[model].request('POST', json=blueprint)
        return await r.json()

    async def delete(self, model):
        r = await self.u[model].request('DELETE')
        return await r.json()

    async def info(self, model):
        r = await self.u[model].request('GET')
        return await r.json()

class AsyncTransformersClient:
    def __init__(self, u):
        self.u = u.transformers

    async def all(self):
        r = await self.u.request('GET')
        return await r.json()

    async def save(self, transformer, blueprint):
        r = await self.u[transformer].request('POST', json=blueprint)
        return await r.json()

    async def delete(self, transformer):
        r = await self.u[transformer].request('DELETE')
        return await r.json()

    async def info(self, transformer):
        r = await self.u[transformer].request('GET')
        return await r.json()

class AsyncDatasetsClient:
    def __init__(self, u):
        self.u = u.datasets

    async def all(self):
        r = await self.u.request('GET')
        return await r.json()

    async def info(self, dataset):
        r = await self.u[dataset].request('GET')
        return await r.json()

    async def delete(self, dataset):
        r = await self.u[dataset].request('DELETE')
        return await r.json()

    async def upload(self, dataset_file):
        r = await self.u['import'].request('POST', data={'f': dataset_file})
        return await r.json()

    async def download(self, dataset):
        r = await self.u[dataset].export.request('GET')
        return r.content


