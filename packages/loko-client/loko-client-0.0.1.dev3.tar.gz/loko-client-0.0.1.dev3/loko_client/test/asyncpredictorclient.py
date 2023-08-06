import asyncio

from loko_client.business.base_client import AsyncPredictorClient

pclient = AsyncPredictorClient()

async def test():
    import sys
    sys.path.append('/home/cecilia/loko/projects/loko_explainability/venv/lib/python3.10/site-packages/')

    from sklearn import datasets
    import pandas as pd

    all_predictors = await pclient.predictors.all()

    ### create model ###
    all_models = await pclient.models.all()
    model = 'sgd_classifier_proba'
    if model in all_models:
        await pclient.models.delete(model)
    await pclient.models.save(model, {'__klass__': 'sk.SGDClassifier', 'loss': 'log'})

    datasets_mapping = dict(boston=dict(data=datasets.load_boston(), task='regression'),
                            diabetes=dict(data=datasets.load_diabetes(), task='regression'),
                            breast_cancer=dict(data=datasets.load_breast_cancer(), task='classification'),
                            iris=dict(data=datasets.load_iris(), task='classification'))

    for dataset, info in datasets_mapping.items():
        if dataset in all_predictors:
            print(f'PREDICTOR {dataset} ALREADY EXIST!')
            print(await pclient.predictors.delete(dataset))
        ### create predictor ###
        if info['task'] == 'classification':
            await pclient.predictors.save(dataset, model_id='sgd_classifier_proba')
        else:
            await pclient.predictors.save(dataset, model_id='sgd_regressor')
        ### fit predictor ###
        X = pd.DataFrame(info['data']['data'], columns=info['data']['feature_names']).to_dict(orient='records')
        y = info['data']['target'].tolist()
        await pclient.predictors.fit(dataset, data=dict(data=X, target=y), wait=True)
        info = await pclient.predictors.info(dataset)
        print(info)
        if info['task'] == 'classification':
            print(await pclient.predictors.predict(dataset, data=X, include_probs=True))
        else:
            print(await pclient.predictors.predict(dataset, data=X))
        print(await pclient.predictors.evaluate(dataset, data=dict(data=X, target=y)))

async def test2():
    all_predictors = await pclient.predictors.all()
    print('ALL PREDICTORS:', all_predictors)
    for p in all_predictors:
        print(p, await pclient.predictors.info(p))
    print()
    all_models = await pclient.models.all()
    print('ALL MODELS:', all_models)
    for m in all_models:
        bp = await pclient.models.info(m)
        print(m, bp)
        print(await pclient.models.delete(m))
        print(await pclient.models.save(m, bp))
    print()
    all_transformers = await pclient.transformers.all()
    print('ALL TRANSFORMERS:', all_transformers)
    for t in all_transformers:
        bp = await pclient.transformers.info(t)
        print(t, bp)
        print(await pclient.transformers.delete(t))
        print(await pclient.transformers.save(t, bp))

    ###########################################
    print(await pclient.predictors.delete('iris_copy'))
    print(await pclient.predictors.copy('iris'))
    with open('/home/cecilia/Documenti/Progetti/prove-predictor/iris.zip', 'wb') as f:
        content = await pclient.predictors.download('iris')
        f.write(await content.read())
    print(await pclient.predictors.delete('iris'))
    with open('/home/cecilia/Documenti/Progetti/prove-predictor/iris.zip', 'rb') as f:
        print(await pclient.predictors.upload(f))

    print(await pclient.predictors.release('iris'))
    print(await pclient.predictors.history('iris'))
    print()
    ###########################################
    all_jobs = await pclient.jobs.all()
    all_jobs = all_jobs['alive']+all_jobs['not_alive']
    print('ALL JOBS:', all_jobs)
    for j in all_jobs:
        print(j, await pclient.jobs.info(j))
        print(await pclient.jobs.delete(j))
    print()
    print(await pclient.predictors.predict('prima_prova', data=[dict(text='hello')]))
    print()
    all_containers = await pclient.containers.all()
    print('ALL CONTAINERS:', all_containers)
    for c in all_containers:
        print(await pclient.containers.info(c))
        print(await pclient.containers.delete(c))
    print(await pclient.containers.all())

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = loop.create_task(test2())
r = loop.run_until_complete(task)